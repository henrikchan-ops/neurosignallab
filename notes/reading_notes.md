# Reading Notes

## Week 2

### 1. Mike X Cohen / Neural Signal Processing Notes

#### Key points
- EEG can be understood partly as a source-separation problem: sensors measure mixtures of hidden sources.
- EEG measures large-scale synchronous electrical activity, not individual neurons.
- Preprocessing is dataset- and study-specific.
- Common preprocessing steps include filtering, epoching, marker adjustment, bad-electrode marking, rereferencing, and ICA.
- Artifact handling depends on whether the artifact can be separated or whether the trial/channel must be rejected.

#### How this affects NeuroSignalLab
- I should treat raw EEG as noisy sensor data, not direct access to a single neural source.
- I need to document preprocessing decisions clearly.
- I should distinguish preprocessing from modeling.
- 
### 2. MNE-Python: Raw, Events, Annotations, Epochs

#### Source
MNE-Python documentation: Parsing events from raw data.

#### Key points
- MNE distinguishes between `Annotations` objects and `Events` arrays.
- An annotation has an onset, duration, and description.
- `mne.events_from_annotations(raw)` can convert annotations into events.
- By default, MNE creates one event at the onset of each annotation.
- The resulting event dictionary can be used when creating Epochs.

#### How this affects NeuroSignalLab
- I need to inspect `raw.annotations` after loading PhysioNet EDF files.
- I need to convert annotations into events before creating epochs.
- I need to understand the meaning of each event code before using it as a label.
- The first real notebook should load a Raw object, inspect annotations, convert events, and only then create epochs.

- ### 3. PhysioNet EEG Motor Movement/Imagery Dataset

#### Source
PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0.

#### Key points
- The dataset contains EEG recordings from motor execution and motor imagery tasks.
- Recordings use 64 EEG channels.
- The sampling frequency is 160 Hz.
- Files are provided in EDF+ format with annotation channels.
- Event codes are `T0`, `T1`, and `T2`.
- `T0` means rest.
- The meanings of `T1` and `T2` depend on the run type.
- In runs 4, 8, and 12, `T1` corresponds to imagined left fist and `T2` corresponds to imagined right fist.

#### How this affects NeuroSignalLab
- I should begin with runs 4, 8, and 12 because they give a clean imagined left/right fist task.
- I should not mix all runs before defining run-specific label meanings.
- My first classification problem should probably be `T1` versus `T2` for imagined left/right fist.
- A 4-second epoch at 160 Hz gives 640 time samples.

- ### 4. MOABB Evaluation Concepts

#### Source
MOABB documentation.

#### Key points
- MOABB stands for Mother of All BCI Benchmarks.
- It is used to benchmark EEG-based BCI algorithms across datasets and evaluation schemes.
- MOABB distinguishes within-session, cross-session, and cross-subject evaluation.
- Careful data splitting is critical in BCI research.
- A model can look stronger if the train/test split is too easy.

#### How this affects NeuroSignalLab
- I should not only report naive random-split accuracy.
- I should eventually compare random split, session-wise split, and subject-wise split.
- Each split tests a different kind of generalization.
- My final report should explain what the model was actually tested on.

- ### 5. EEGNet

#### Source
EEGNet paper.

#### Key points
- EEGNet is a compact convolutional neural network for EEG-based brain-computer interfaces.
- It was designed for EEG-based BCI tasks.
- It is relevant to motor-imagery-style EEG classification.
- It is a later comparison model, not the first model I should build.

#### How this affects NeuroSignalLab
- I should first build classical baselines.
- I should then build a simple CNN.
- EEGNet can be added later as a stronger EEG-specific deep-learning comparison.
- EEGNet results still depend on preprocessing, labels, and evaluation design.

## Week 3 

### 1. The MNE `Raw` object

MNE represents continuous EEG recordings using a `Raw` object.[^mne-raw]

The underlying EEG data can be thought of as:

`channels × time samples`

For the PhysioNet recording used this week, the data contained 64 EEG channels sampled continuously over time.

The `Raw` object contains both the signal itself and information about the recording, including:

- channel names
- channel types
- sampling frequency
- recording duration
- annotations
- measurement information

MNE represents EEG amplitudes internally using SI units, meaning EEG values are stored in volts.[^mne-raw]

Because EEG amplitudes are commonly visualized in microvolts, values can be converted using:

`microvolts = volts × 1e6`

This conversion changes only the unit used for visualization and does not change the underlying signal.

---

### 2. Annotations

Annotations are time-based labels attached to a continuous EEG recording.[^mne-annotations]

An annotation contains three important pieces of information:

- `onset` — when the annotation begins
- `duration` — how long the annotated interval lasts
- `description` — the label assigned to that interval

In the EEG Motor Movement/Imagery recording used this week, the annotation descriptions were:

- `T0`
- `T1`
- `T2`

Annotations remain attached to the continuous `Raw` recording and describe when different experimental conditions occur.

Annotations should not be confused with MNE event arrays. They represent related information, but in different formats.

---

### 3. Converting annotations into events

MNE can convert annotations into a numerical event representation using:

`mne.events_from_annotations()`[^mne-events]

This produces two outputs:

1. an `events` array
2. an `event_id` dictionary

The event array has the general structure:

`n_events × 3`

Each event is represented by a row containing:

`[sample_index, previous_event_value, event_code]`

The first column identifies when the event occurs using a sample index.

The third column identifies the numerical event code.

For example:

`[2000, 0, 2]`

means that an event with code `2` occurs at sample `2000`.

The middle column is part of MNE's standard event-array structure and is normally `0` for events created from annotations.

---

### 4. Event IDs and readable labels

The event array itself contains numerical codes rather than human-readable task labels.

MNE therefore also creates an `event_id` dictionary that maps annotation descriptions to event codes.[^mne-events]

For example:

```python
{
    "T0": 1,
    "T1": 2,
    "T2": 3
}

### References

MNE Developers. (2026). *mne.Annotations — MNE-Python 1.12.1 documentation*. MNE-Python.

MNE Developers. (2026). *mne.datasets.eegbci.load_data — MNE-Python 1.12.1 documentation*. MNE-Python.

MNE Developers. (2026). *mne.io.Raw — MNE-Python 1.12.1 documentation*. MNE-Python.

MNE Developers. (2026). *Parsing events from raw data — MNE-Python documentation*. MNE-Python.

MNE Developers. (2026). *Working with sensor locations — MNE-Python 1.12.1 documentation*. MNE-Python.

Schalk, G. (2009). *EEG Motor Movement/Imagery Dataset* (Version 1.0.0). PhysioNet. doi:10.13026/C28G6P.