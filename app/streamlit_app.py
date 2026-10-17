### Setup
import streamlit as st
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path.cwd()
SPLIT_PATH = ROOT / "results" / "week9_subject_split.csv"
DATA_PATH = ROOT / "data" / "processed"

sys.path.insert(0, str(ROOT/"src"))

from neurosignallab.inference import load_eegnet, predict_trial
from neurosignallab.interpretability import compute_channel_occlusion

CHECKPOINT_PATH = (
    ROOT
    / "models"
    / "config_d_seed42_best.pt"
)

CHANNEL_NAMES = [
    "FC5", "FC3", "FC1", "FCz", "FC2", "FC4", "FC6",
    "C5", "C3", "C1", "Cz", "C2", "C4", "C6",
    "CP5", "CP3", "CP1", "CPz", "CP2", "CP4", "CP6",
    "Fp1", "Fpz", "Fp2",
    "AF7", "AF3", "AFz", "AF4", "AF8",
    "F7", "F5", "F3", "F1", "Fz", "F2", "F4", "F6", "F8",
    "FT7", "FT8", "T7", "T8", "T9", "T10",
    "TP7", "TP8",
    "P7", "P5", "P3", "P1", "Pz", "P2", "P4", "P6", "P8",
    "PO7", "PO3", "POz", "PO4", "PO8",
    "O1", "Oz", "O2", "Iz"
]

### Cache models + data
@st.cache_resource
def get_model():
    return load_eegnet(CHECKPOINT_PATH)

@st.cache_data
def load_validation_data():
    split_df = pd.read_csv(SPLIT_PATH)

    validation_subjects = split_df.loc[
        split_df["split"] == "validation",
        "subject"
    ].to_numpy()

    subjects = np.load(
        DATA_PATH / "subjects.npy"
    )

    validation_mask = np.isin(
        subjects,
        validation_subjects
    )

    X = np.load(
        DATA_PATH / "X_motor_imagery.npy",
        mmap_mode="r"
    )[validation_mask]

    y = np.load(
        DATA_PATH / "y_motor_imagery.npy"
    )[validation_mask]

    subjects = subjects[validation_mask]

    runs = np.load(
        DATA_PATH / "runs.npy"
    )[validation_mask]

    return X, y, subjects, runs

### Setup
st.set_page_config(
    page_title="NeuroSignalLab",
    page_icon="🧠")

model, checkpoint, device = get_model()

X_val, y_val, subjects_val, runs_val = load_validation_data()

st.title("NeuroSignalLab")

st.subheader("Motor-imagery EEG decoding research prototype.")

st.write("Interactive research prototype for cross-subject "
    "motor-imagery EEG decoding.")

selected_index = st.selectbox(
    "Select a validation EEG trial",
    range(len(X_val))
)

### Metadata
selected_trial = X_val[selected_index]
selected_subject = subjects_val[selected_index]
selected_run = runs_val[selected_index]
true_label = y_val[selected_index]
true_class = checkpoint["class_names"][int(true_label)]

st.subheader("Trial information")

st.write(f"Subject: {selected_subject}")
st.write(f"Run: {selected_run}")
st.write(f"True class: {true_class}")

### Run model
run_model = st.button("Run EEGNet")

if run_model:
    result = predict_trial(
        model,
        selected_trial,
        checkpoint,
        device
    )

    st.subheader("Prediction")

    st.write(
        result["predicted_class"].capitalize()
    )

    st.subheader("Model output")

    st.write(
        f"Left: {result['probabilities'][0] * 100:.1f}%"
    )

    st.write(
        f"Right: {result['probabilities'][1] * 100:.1f}%"
    )

    ### Interpretability
    st.subheader("Interpretability")

    st.write(
        "Channel occlusion asks: which EEG channels most supported "
        "the model's predicted class for this trial?"
    )

    channel_occlusion = compute_channel_occlusion(
        model,
        selected_trial,
        checkpoint,
        device,
        result["prediction"]
    )

    top_channels = np.argsort(
        channel_occlusion
    )[::-1][:5]

    st.write("Top 5 channels supporting this prediction:")

    for channel_index in top_channels:
        channel_name = CHANNEL_NAMES[channel_index]
        effect = channel_occlusion[channel_index]

        st.write(f"{channel_name} (index {channel_index}): "f"{effect:.3f}")

    ### Bar plot 

    top_10 = np.argsort(
        channel_occlusion
    )[::-1][:10]

    top_10_names = [
        CHANNEL_NAMES[index]
        for index in top_10
    ]

    top_10_effects = channel_occlusion[
        top_10
    ]

    fig, ax = plt.subplots()

    ax.bar(
        top_10_names,
        top_10_effects
    )

    ax.set_xlabel("EEG channel")
    ax.set_ylabel("Drop in predicted class logit")
    ax.set_title(
        "Channels supporting the prediction"
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)

### Wave plot

st.subheader("EEG signal")

channel_index = st.slider(
    "Select EEG channel",
    0,
    63,
    0
)

#Time axis, 380/160 sampling rate Hz = seconds, add 1s to give the model window
time = (
    np.arange(selected_trial.shape[1])
    / checkpoint["sampling_rate_hz"]
    + 1
)

fig, ax = plt.subplots()

ax.plot(
    time,
    selected_trial[channel_index] * 1e6
)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude (µV)")
ax.set_title(
    f"EEG channel {channel_index}"
)

st.pyplot(fig)

plt.close(fig)

st.caption(
    "Research prototype | Configuration D EEGNet | "
    "Validation BA ≈ 0.628"
)