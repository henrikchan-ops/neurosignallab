### Imports and paths
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

CHECKPOINT_PATH = (
    ROOT
    / "models"
    / "config_d_seed42_best.pt"
)

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

st.caption(
    f"Model: {checkpoint['model_name']} | "
    f"Device: {device}"
)

### Plotting

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