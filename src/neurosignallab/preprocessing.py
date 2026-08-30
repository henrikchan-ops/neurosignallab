from pathlib import Path

import mne
import numpy as np
import pandas as pd
from mne.datasets import eegbci


def preprocess_subject(subject, data_dir, runs=(4, 8, 12)):

    # Load recordings
    raw_fnames = eegbci.load_data(
        subjects=subject,
        runs=list(runs),
        path=Path(data_dir)
    )

    raws = []
    metadata_rows = []

    for run, raw_fname in zip(runs, raw_fnames):

        raw_run = mne.io.read_raw_edf(
            raw_fname,
            preload=True
        )

        # Standardize EEG channel information
        eegbci.standardize(raw_run)
        raw_run.set_montage("standard_1005")

        # Extract motor-imagery events for metadata
        run_events, run_event_id = (
            mne.events_from_annotations(raw_run)
        )

        motor_events_run = run_events[
            (run_events[:, 2] == run_event_id["T1"])
            |
            (run_events[:, 2] == run_event_id["T2"])
        ]

        for trial_in_run, event in enumerate(
            motor_events_run,
            start=1
        ):

            event_code = event[2]

            if event_code == run_event_id["T1"]:
                annotation = "T1"
                class_label = "left"

            else:
                annotation = "T2"
                class_label = "right"

            metadata_rows.append({
                "subject": subject,
                "run": run,
                "trial_in_run": trial_in_run,
                "annotation": annotation,
                "class_label": class_label
            })

        raws.append(raw_run)

    # Runs must use identical EEG channels
    reference_channels = raws[0].ch_names

    if not all(
        raw_run.ch_names == reference_channels
        for raw_run in raws[1:]
    ):
        raise ValueError(
            f"Channel mismatch for subject {subject}"
        )

    # Concatenate runs
    raw = mne.concatenate_raws(
        [raw_run.copy() for raw_run in raws]
    )

    # Average reference
    raw.set_eeg_reference(
        "average",
        projection=True
    )

    # Motor-imagery frequency range
    raw.filter(
        l_freq=7.0,
        h_freq=30.0,
        fir_design="firwin",
        skip_by_annotation="edge"
    )

    # Extract events from concatenated recording
    events, event_id = (
        mne.events_from_annotations(raw)
    )

    motor_event_id = {
        "left": event_id["T1"],
        "right": event_id["T2"]
    }

    motor_events = events[
        (events[:, 2] == motor_event_id["left"])
        |
        (events[:, 2] == motor_event_id["right"])
    ]

    metadata = pd.DataFrame(metadata_rows)

    if len(metadata) != len(motor_events):
        raise ValueError(
            f"Metadata/event mismatch for subject {subject}: "
            f"{len(metadata)} metadata rows vs "
            f"{len(motor_events)} events"
        )

    # Full -1 to +4 s epochs
    epochs = mne.Epochs(
        raw,
        motor_events,
        event_id=motor_event_id,
        tmin=-1.0,
        tmax=4.0,
        baseline=None,
        preload=True,
        proj=True,
        metadata=metadata
    )

    # Machine-learning window: +1 to +4 s
    epochs_ml = epochs.copy().crop(
        tmin=1.0,
        tmax=4.0
    )

    X = epochs_ml.get_data()

    y = (
        epochs_ml.metadata["class_label"]
        .map({
            "left": 0,
            "right": 1
        })
        .to_numpy()
    )

    return X, y, epochs_ml.metadata.copy()
