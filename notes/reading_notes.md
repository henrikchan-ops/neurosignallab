# Reading Notes

## 1. MNE-Python: Raw, Events, Annotations, Epochs

### Source
MNE-Python documentation: Parsing events from raw data.

### Key points
- MNE distinguishes between `Annotations` objects and `Events` arrays.
- An annotation has an onset, duration, and description.
- `mne.events_from_annotations(raw)` can convert annotations into events.
- By default, MNE creates one event at the onset of each annotation.
- The resulting event dictionary can be used when creating Epochs.

### How this affects NeuroSignalLab
- I need to inspect `raw.annotations` after loading PhysioNet EDF files.
- I need to convert annotations into events before creating epochs.
- I need to understand the meaning of each event code before using it as a label.
- The first real notebook should load a Raw object, inspect annotations, convert events, and only then create epochs.

- ## 2. PhysioNet EEG Motor Movement/Imagery Dataset

### Source
PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0.

### Key points
- The dataset contains EEG recordings from motor execution and motor imagery tasks.
- Recordings use 64 EEG channels.
- The sampling frequency is 160 Hz.
- Files are provided in EDF+ format with annotation channels.
- Event codes are `T0`, `T1`, and `T2`.
- `T0` means rest.
- The meanings of `T1` and `T2` depend on the run type.
- In runs 4, 8, and 12, `T1` corresponds to imagined left fist and `T2` corresponds to imagined right fist.

### How this affects NeuroSignalLab
- I should begin with runs 4, 8, and 12 because they give a clean imagined left/right fist task.
- I should not mix all runs before defining run-specific label meanings.
- My first classification problem should probably be `T1` versus `T2` for imagined left/right fist.
- A 4-second epoch at 160 Hz gives 640 time samples.

- ## 3. MOABB Evaluation Concepts

### Source
MOABB documentation.

### Key points
- MOABB stands for Mother of All BCI Benchmarks.
- It is used to benchmark EEG-based BCI algorithms across datasets and evaluation schemes.
- MOABB distinguishes within-session, cross-session, and cross-subject evaluation.
- Careful data splitting is critical in BCI research.
- A model can look stronger if the train/test split is too easy.

### How this affects NeuroSignalLab
- I should not only report naive random-split accuracy.
- I should eventually compare random split, session-wise split, and subject-wise split.
- Each split tests a different kind of generalization.
- My final report should explain what the model was actually tested on.

- ## 4. EEGNet

### Source
EEGNet paper.

### Key points
- EEGNet is a compact convolutional neural network for EEG-based brain-computer interfaces.
- It was designed for EEG-based BCI tasks.
- It is relevant to motor-imagery-style EEG classification.
- It is a later comparison model, not the first model I should build.

### How this affects NeuroSignalLab
- I should first build classical baselines.
- I should then build a simple CNN.
- EEGNet can be added later as a stronger EEG-specific deep-learning comparison.
- EEGNet results still depend on preprocessing, labels, and evaluation design.
