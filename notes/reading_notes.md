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


## Week 4

### Notes for preprocessing
#### 1) Physionet, what experiment produced the data?

The PhysioNet EEG Motor Movement/Imagery Dataset (EEGMMIDB) contains EEG recordings collected during motor execution and motor imagery tasks.[^physionet]

The dataset contains recordings from 109 subjects. EEG was recorded using 64 scalp electrodes arranged according to the international 10-10 system at a sampling frequency of 160 Hz. The recordings are distributed in EDF+ format.[^physionet]

Each subject completed 14 runs:

- Run 1: eyes-open baseline
- Run 2: eyes-closed baseline
- Runs 3, 7, and 11: executed left-versus-right fist movement
- Runs 4, 8, and 12: imagined left-versus-right fist movement
- Runs 5, 9, and 13: executed both-fists-versus-both-feet movement
- Runs 6, 10, and 14: imagined both-fists-versus-both-feet movement[^physionet][^mne-eegbci]

The meaning of the annotation labels depends on the type of run.

For unilateral fist runs:

- `T0` = rest
- `T1` = onset of left-fist movement or imagery
- `T2` = onset of right-fist movement or imagery

For bilateral hand/foot runs:

- `T0` = rest
- `T1` = onset of both-fists movement or imagery
- `T2` = onset of both-feet movement or imagery[^physionet]

We want to ask: 
Can EEG distinguish imagined left-fist movement from imagined right-fist movement?

For the current project, runs 4, 8, and 12 provide three repetitions of the same left-versus-right motor-imagery task.

#### 2) Dataset Quality Control: Shuqfa, Lakas & Belkacem

Is the original PhysioNet dataset perfectly uniform?

Shuqfa, Lakas, and Belkacem systematically curated the dataset and excluded six subjects because of anomalies in the recordings, leaving 103 subjects in their curated version.[^shuqfa]

6 subjects reported non-standard recording structures:  

S088
S089
S092
S100
S104
S106 [^shuqfa][^domain-adaptation]

Later, we decide our own exclusion criteria. 

A typical task recording contains repeated rest and task intervals, with approximately 7–8 events of each task class per run. The task intervals are approximately four seconds long.[^shuqfa]

The preprocessing pipeline should therefore check:

- recording duration
- sampling frequency
- channel availability
- event labels
- event counts
- missing or abnormal trials
- invalid numerical values
- unusually flat or extreme signals

This process is called quality control, or QC.

#### 3) Event-related Desynchronization and Synchronization: Pfurtscheller & Lopes da Silva

What biological signal are we trying to detect?

ERD refers to an event-related decrease in oscillatory power within a particular frequency band.[^erd]. ERD occurs when activity contributing to an ongoing rhythm becomes less synchronized.

A neuronal population may exhibit a relatively strong ongoing rhythm before a task. When that network becomes engaged, the rhythmic activity can become less synchronized, causing the measured power in that frequency band to decrease.

##### Event-Related Synchronization — ERS

ERS refers to an event-related increase in oscillatory power within a particular frequency band.[^erd]

ERD and ERS are:

- frequency-specific
- time-dependent
- spatially dependent

This means that ERD and ERS can occur at different times, in different frequency bands, and at different scalp locations.

A commonly way to calcuate it would be using reference power:

`(task power - reference power) / reference power × 100`

For example:

Resting mu power = 10  
Imagery mu power = 6

`(6 - 10) / 10 × 100 = -40%`

The result represents a 40% reduction in power and therefore ERD.

It is important not to confuse:

1. **EEG reference** — the electrical reference against which electrode voltage is measured.
2. **ERD/ERS reference period** — a time interval whose oscillatory power is used as a baseline for comparison.

These are separate concepts.

#### 4) What is Event-related potential?

An ERP, or event-related potential, is a voltage response that occurs at a relatively consistent latency (delay) and phase (specific point in brainwave oscillation) relative to an event.[^erd]

For example, a visual cue may produce a repeatable voltage deflection (voltage change) after the cue appears. If this response occurs at approximately the same time and phase across trials, averaging the trials preserves it.

ERD/ERS describes changes in ongoing oscillatory power. The underlying oscillations do not need to have the same phase on every trial. What remains consistent is the change in power (amount of activity in certain frequency).[^erd]

Motor-imagery analysis cares about frequency, power, time and spatial location

ERP:

`event → repeatable voltage waveform`

ERD/ERS:

`event → change in oscillatory power`

Motor imagery can produce both evoked responses (response to stimulus/ERP) and ERD/ERS.

However, the primary interest for sustained motor imagery is change of ongoing sensorimotor rhythms rather than only the initial visually evoked response to the cue.[^erd][^mcfarland]

This is one reason that a motor-imagery classifier may deliberately exclude the immediate period after cue onset.
  

##### How does ERD/ERS differ from ERP?

ERP is a waveform that is consistent phase and latency relative to an event. For instance the ERP when a participant sees a visual cue -> the voltage deflection over trials is the ERP, because it occurs at roughly the same time and phase on every trial. 

##### Why is motor imagery using ERD/ERS instead of ERP?
The experiment is structured so that the participant get a visual cue before the movement gets imagined at t=0. The model can instead learn left-right visual stimulus instead left-hand vs right-hand imagery.[^mne-csp-example]

Because ERP is voltage and analyzed in amplitude, it emphasizes phase-locked responses such as the visual cue. Since the project whats to classify sustained, frequency-specific sensorimotor rhythms, it can be better characterized by ERD/ERS. 

#### 5) Why mu and beta: McFarland et al. 

Which frequencies and scalp areas are relevant for hand motor imagery?

McFarland et al. studied 64-channel EEG from participants performing or imagining left- and right-hand movements.[^mcfarland]

They examined that during: 
- mu rhythm: approximately 8–12 Hz
- beta rhythm: approximately 18–25 Hz

Both actual movement and imagined movement were associated with desynchronization in mu and beta activity. [^mcfarland]

Mu desynchronization showed relatively lateral sensorimotor foci, while beta desynchronization was more diffuse and showed stronger activity near the vertex.[^mcfarland]

##### Other definitions to keep in mind

Focus (plural foci) - THe region where effect is strongest for that specific ERD/ERS/ERP. Though, it does not mean the exact cortical source beneath produced that signal.

Vertex - Approximate location of the top-center of the head. Typically channels called Cz. THis is why C3, Cz and C4 are typical landmarks in motor-imagery EEG.

Variance - how much a signal fluctuates around its mean. Often kan be used to interpret power by mean squared amplitude. CSP uses variance to identify class-discrimination. 


#### 6) Common Spatial Patterns: Ramoser et al.

WHy keeping multiple channels can help with classification.

Common Spatial Patterns (CSP) is a supervised spatial-filtering method designed to extract discriminative information from multichannel data.[^ramoser][^mne-csp]

Instead of selecting one electrode, CSP learns weighted combinations of electrodes to distinguish between brainstates.

Conceptually, a CSP component could look like:

`component = 0.8 × C3 + 0.2 × Cz - 0.7 × C4 + ...`

The weights are learned from the data.

CSP searches for spatial filters that produce large variance for one class and small variance for the other, combined with complementary filters showing the opposite pattern.[^ramoser]. CSP can then emphasize spatial patterns of oscillatory power that distinguish the two motor-imagery classes.

##### Conceptual use of CSP

The conceptual timeline is:

`multichannel EEG`

→ `CSP spatial filters`

→ `small number of CSP components`

→ `component variance/power`

→ `usually log-transformed features`

→ `classifier`

→ `training data → fit CSP`

→ `test data → apply already-fitted CSP`

If all data is used to fit CSP, the test data will influence extraction and cause data leakage. 

CSP is useful here because it is:

- established in motor-imagery BCI research
- interpretable
- computationally efficient
- designed for multichannel signals
- directly sensitive to differences in class-related variance

#### 7) Filtering is not harmless: Widmann, Schrøger and Maess 

Filtering is a transformation of the signal, not simply the deletion of unwanted frequencies.[^widmann]

For the first motor-imagery baseline, the planned passband is:

`7–30 Hz`

This choice includes the main mu and beta activity relevant to the current motor-imagery hypothesis and matches the frequency range used in MNE's standard motor-imagery CSP example.[^mne-csp-example]

Real filters cannot change instantaneously between a passband and stopband.

Instead, filters contain transition regions:

`stopband → transition band → passband → transition band → stopband`

Sharper filters can produce longer temporal ringing.[^widmann][^mne-filter]. Causing frequency domain and time-domain plots to be affected. 

A good filter includes a transition band around the cutoff that slowly phases the signal out. Since you need datapoints around the edge to calculate an output, a sharp cutoff requires longer filters and can increase temporal "ringing".

#### 8) Filtering boundaries

Edge artifacts are a separate problem that occurs near the beginning/end of a signal or at discontinuities because the filter lacks normal neighbouring data around those boundaries.

Runs 4, 8, and 12 belonging to the same subject may be concatenated for convenient processing, but the boundaries between runs must still be preserved. Different subjects remain separate. 

If runs are concatenated, MNE boundary annotations allow filtering to respect the discontinuities between them.

The intended approach is to filter the continuous recording segments while respecting boundaries between runs. The end of one experimental run and the beginning of another are not continuous.

MNE's `concatenate_raws()` marks recording boundaries with bad boundary annotations.[^mne-concat]

MNE's motor-imagery CSP example filters uses `skip_by_annotation="edge"` so the filter does not treat concatenated recording segments as one continuous signal.[^mne-csp-example]

This is different from filtering every motor-imagery epoch independently.


##### What does average referencing mean?

EEG electrodes do not measure absolute electrical potential.

They measure potential differences relative to a reference.

A ***common average reference*** is when MNE computes the average across the eligible EEG channels and subtracts that average from each EEG channel:[^mne-reference]

`new channel = original channel - average across EEG channels`

##### How is average referencing a "projection"?

MNE can immediately apply the average reference to the raw data:

`raw.set_eeg_reference("average")`

or store it as a projection:

`raw.set_eeg_reference("average", projection=True)`[^mne-reference]


With `projection=True` the average-reference transformation is stored in the MNE object but is not immediately applied to the signal.

A transformation operator (like the MNE reference)removes the channel-average component so that the the mean across the EEG channels is zero at each time point. 

The standard MNE motor-imagery CSP example uses average reference as a projection.[^mne-csp-example] This is because a projection can adapt to excluded channels.


#### 9) Epochs

How to turn EEG into trials

Continuous EEG must be divided into task-related trials before trial-based machine learning: 

`continuous EEG`

→ `find T1/T2 onset`

→ `extract a fixed time interval around each onset`

→ `one epoch per task event`

MNE represents epoched EEG with the shape:

`n_epochs × n_channels × n_times`[^mne-epochs]

For example:

`45 × 64 × 801`

would mean:

- 45 epochs
- 64 channels
- 801 time samples

At 160 Hz, an epoch from -1 to +4 seconds contains 801 samples because MNE includes the samples corresponding to both the starting and ending times.[^mne-epochs]

#### 10) Baseline Correction

MNE epoch baseline correction subtracts the mean voltage during a selected baseline interval from the epoch. Creating a refencer oscillatory power.[^mne-epochs]

Please understand that the ERD/ERS compares oscillatory power during a task with oscillatory power during the reference period.[^erd][^mne-erds]

MNE's ERDS example instead uses the -1 to 0 second interval as a power reference for ERD/ERS visualization.[^mne-erds]

The choice of ERD/ERS reference period matters because different baselines can alter the apparent magnitude of ERD/ERS.[^erd-baseline]

#### 11) Artifact rejection

Individual Epochs may contain unusually large artifacts or nearly flat signals.

MNE can reject epochs using peak-to-peak amplitude.[^mne-epochs]

If the peak-to-peak amplitude of any relevant channel exceeds a specified `reject` threshold (from a max to min value), MNE can drop the epoch.

MNE also provides a `flat` threshold for detecting signals whose peak-to-peak amplitude is suspiciously small.[^mne-epochs]

This is determined through analyzing the data. 

The basic workflow should therefore be:

#### 12) Quality control

Before running this should all be checked: 

- subject and run identities
- sampling frequency
- number of channels
- channel names
- recording duration
- event labels
- event counts
- epoch counts
- class balance
- epoch dimensions
- NaN values
- infinite values
- flat channels
- extreme amplitudes
- unexpected dropped epochs
- run boundaries
- train/test leakage


#### 13) Summary / Workflow

MOTOR IMAGERY
      ↓
changes sensorimotor neural activity
      ↓
mu/beta rhythmic synchronization changes
      ↓
ERD / ERS
      ↓
changes 7–30 Hz POWER
      ↓
band-pass filter isolates relevant rhythms
      ↓
power ≈ variance for zero-mean band-limited signal
      ↓
left/right imagery produces different
spatial variance patterns across electrodes
      ↓
CSP finds combinations of electrodes
that maximize those differences
      ↓
CSP log-variance features
      ↓
classifier
      ↓
left vs right prediction

#### 14) References Week 4

[^physionet]: Schalk, G. (2009). *EEG Motor Movement/Imagery Dataset* (Version 1.0.0). PhysioNet. doi:10.13026/C28G6P.

[^mne-eegbci]: MNE Developers. *mne.datasets.eegbci.load_data — MNE-Python documentation*. Run definitions for the EEGBCI dataset.

[^shuqfa]: Shuqfa, Z., Lakas, A., & Belkacem, A. N. (2024). Increasing accessibility to a large brain–computer interface dataset: Curation of PhysioNet EEG Motor Movement/Imagery Dataset for decoding and classification. *Data in Brief, 54*, 110181. doi:10.1016/j.dib.2024.110181.

[^domain-adaptation]: *Domain-aware domain–class adaptation network for motor execution to motor imagery EEG classification* (2026). Used as a secondary confirmation of the six EEGMMIDB subjects reported as having non-standard recording structures.

[^erd]: Pfurtscheller, G., & Lopes da Silva, F. H. (1999). Event-related EEG/MEG synchronization and desynchronization: Basic principles. *Clinical Neurophysiology, 110*(11), 1842–1857. doi:10.1016/S1388-2457(99)00141-8.

[^mcfarland]: McFarland, D. J., Miner, L. A., Vaughan, T. M., & Wolpaw, J. R. (2000). Mu and beta rhythm topographies during motor imagery and actual movements. *Brain Topography, 12*(3), 177–186. doi:10.1023/A:1023437823106.

[^ramoser]: Ramoser, H., Müller-Gerking, J., & Pfurtscheller, G. (2000). Optimal spatial filtering of single trial EEG during imagined hand movement. *IEEE Transactions on Rehabilitation Engineering, 8*(4), 441–446. doi:10.1109/86.895946.

[^mne-csp]: MNE Developers. *mne.decoding.CSP — MNE-Python documentation*. Documentation of supervised Common Spatial Patterns decomposition.

[^mne-csp-example]: MNE Developers. *Motor imagery decoding from EEG data using the Common Spatial Pattern (CSP) — MNE-Python documentation*. Used for the reference CSP implementation, 7–30 Hz filtering, run-boundary handling, average-reference projection, epoching, and `baseline=None`.

[^widmann]: Widmann, A., Schröger, E., & Maess, B. (2015). Digital filter design for electrophysiological data — a practical approach. *Journal of Neuroscience Methods, 250*, 34–46. doi:10.1016/j.jneumeth.2014.08.002.

[^mne-filter]: MNE Developers. *Background information on filtering — MNE-Python documentation*. Used for FIR-filter design, transition bands, ringing, phase, and filter trade-offs.

[^mne-concat]: MNE Developers. *mne.concatenate_raws — MNE-Python documentation*. Used for understanding concatenation boundaries and boundary annotations.

[^mne-reference]: MNE Developers. *mne.set_eeg_reference — MNE-Python documentation*. Used for average referencing and `projection=True`.

[^mne-reference-tutorial]: MNE Developers. *Setting the EEG reference — MNE-Python documentation*. Used for understanding the advantages and behavior of average-reference projectors.

[^mne-epochs]: MNE Developers. *mne.Epochs / mne.BaseEpochs — MNE-Python documentation*. Used for epoch structure, inclusive time endpoints, baseline correction, peak-to-peak rejection, flat-signal rejection, and projection handling.

[^mne-erds]: MNE Developers. *Compute and visualize ERDS maps — MNE-Python documentation*. Used for ERD/ERS interpretation, time-frequency analysis, and use of a pre-cue power baseline.

[^erd-baseline]: *Impact of the baseline temporal selection on the ERD/ERS analysis for Motor Imagery-based BCI*. Used for the methodological importance of choosing ERD/ERS reference periods carefully.

## Week 5 — Evaluation Methodology and CSP + LDA

### 1) What is the goal of model evaluation?

The purpose of evaluation is to estimate how well a trained model performs on observations that did not participate in fitting/training the model.

Testing a model on the same data used for training does not measure generalization, rather it teaches memorization. A model learn patterns specific to the training data and perform poorly on unseen data.[^sklearn-cv]

The basic structure is:

`training data → fit model → unseen data → evaluate`

#### Testing structure: Cross-validation

Cross-validation repeatedly divides the available observations into folds. A new model is trained for each fold to fit its own separate CSP and LDA. The fold is split into training data, and held-out data used to evaluate the model.[^sklearn-cv]

#### Three types of data
Training data -> allows the CSP to learn spatial filters and Linear discriminant analysis to classify boundaries

Validation data -> Data used to compare model choices, like frequency range, differnet CSP components and filters. 

Test data -> Data that remains untouched until all methodological decisions are finished

### 2) Within-subject generalization

EEG observations can have a grouped structure.

For example, several trials may come from the same experimental run or the same subject. Observations from the same group may share recording-specific characteristics that cannot always be treated as independent.[^sklearn-cv]

For the initial within-subject experiment, the important grouping variable is runs.

Subject 1 contains motor-imagery trials from:

- Run 4
- Run 8
- Run 12

The initial evaluation therefore uses leave-one-run-out cross-validation:

`train 8 + 12 → test 4`

`train 4 + 12 → test 8`

`train 4 + 8 → test 12`

Scikit-learn's grouped cross-validation methods are designed to ensure that observations in a held-out group do not also occur in the training set, and vice versa.[^sklearn-cv]

This tests:

> Can a model trained on two runs from one subject generalize to an unseen run from the same subject?

This is **within-subject generalization**.

It does not yet answer whether the model generalizes to an unseen person. That is subject-wise evaluation.

### 3) What is data leakage?

Data leakage occurs when information that should belong only to the held-out data affects model fitting.

This produces an overly optimistic estimate of generalization performance.[^sklearn-leakage]

A general rule is:

Anything that learns something from the dataset must only learn from the training data.

The test data may be **transformed** using parameters learned from the training data, but they must not participate in fitting those parameters.[^sklearn-leakage]


#### Why CSP creates a leakage risk

Common Spatial Patterns (CSP) is a **supervised spatial-filtering method**, meaning it can see the class labels while learning.

MNE's implementation learns the CSP decomposition from:

`X = EEG epochs`

and

`y = class labels`.[^mne-csp]

Therefore fitting CSP on a complete dataset would be incorrect:

The CSP filters would already contain information from the future held-out trials / test data.

Instead, splitting into train/test folds and fit CSP using only traning X and traning y, could create a fitted classifier that can predict held out-trials:

This process must occur inside every cross-validation fold.

### 4) Why use a Pipeline?

A scikit-learn `Pipeline` chains transformations and a classifiers into one estimator.[^sklearn-pipeline]

In essence, it creates a procedure for which order classifier and transform should be used. 

During cross-validation, the complete pipeline is fitted separately for each training fold.

How it looks like in code:

#### Training fold

`training EEG`

→ `CSP.fit()`

→ `CSP.transform()`

→ `LDA.fit()`

#### Test fold

`unseen EEG`

→ `already-fitted CSP.transform()`

→ `already-fitted LDA.predict()`

This reduces the risk of accidentally fitting a transformation using information from the test fold.[^sklearn-leakage][^sklearn-pipeline]


### 5) What is Common Spatial Patterns?

CSP is a supervised spatial-filtering method commonly used for discriminating between two EEG conditions.[^ramoser][^mne-csp]

Our input has the form:

`n_epochs × n_channels × n_times`

For the current project:

`trials × 64 channels × 481 samples`

CSP learns weighted combinations of electrodes called a spatial filter, which is then used to create a smaller set of virtual CSP components. CSP components are spatial patterns across different channels, that can be fitted into CSP features using log average power. This can later be evaluated.

CSP seeks spatial filters whose signal variance differs strongly between the two classes. 

CSP searches for: large variance for class A and small variance for class B, and directions where the opposite relationship occurs.

#### What are different CSP elements?

CSP component
= new spatially filtered EEG time series

CSP feature
= numerical summary of that component,
  usually the log average power

#### What is variance?

How strongly does a signal fluctuate around its average value. The further it fluctuates, the higher the variance. 

### 6) Why does variance contain useful motor-imagery information?

Motor imagery is associated with changes in ongoing sensorimotor oscillations, particularly event-related desynchronization and synchronization in sensorimotor rhythms.[^erd]

ERD/ERS represents changes in oscillatory power.[^erd]

For a band-limited EEG signal, power is closely related to signal variance. 

Average power is the mean squared signal amplitude, while variance is the mean squared distance from the signal mean. If the signal mean is approximately zero, as its often after band-pass filtering; variance and average power are approximately equal.

This creates the chain:

`motor imagery`

→ `changes in sensorimotor oscillations`

→ `changes in mu/beta power`

→ `changes in spatial variance`

→ `CSP detects discriminative variance patterns`

---

### 7) What does CSP produce?

CSP transforms multichannel EEG into a smaller number of components using a weighted filter (spatial filter).

This is called a CSP component -> it represents diffeent spatial patterns across multiple channels.

The power values calculated from each component is the CSP feature. 

For example:

ONE EEG TRIAL

`64 channels × 481 samples`
     ↓
CSP spatial filter

`4 components × 481 samples`
     ↓
calculate power of each component

4 power values
     ↓
log transform

4 CSP features


MMNE computes the average power of each CSP component. With `transform_into="average_power"` and `log=None` or `log=True`. These power values are log-transformed to form the CSP features.[^mne-csp]

For the initial baseline, we use:

`n_components = 4`

and keep this choice fixed before examining model performance.

MNE notes that the number of CSP components is a parameter that should ultimately be selected through cross-validation.[^mne-csp]

The four CSP components are summarized into four log-power CSP features, and those four features are passed to LDA.

#### Why use log-variance

EEG power and variance tend to be skewed. For tansforming into a linear classifier, log-variance makes the features more suitable. 

Small differences among low values remain visible, while large values become less extreme

### 8) What is Linear Discriminant Analysis?

Linear Discriminant Analysis (LDA) is a classical linear classifier. Meaning it creates a linear boundary separating the two calsses.

In this project:

CSP = Turn EEG into discriminative features (like coordinates, vectors or datapoints)

LDA = Find a linear rule that separates those two feature vectors between left- and right-imagery trials.

LDA models each class using a multivariate Gaussian distribution while assuming that the classes share the same covariance matrix.[^sklearn-lda]

Multivariate gaussian distribution = cluster of feature points with a center and spread

Covariance matrix = How spread out the features are and how they vary together

To simplify it: LDA assumes each class forms a roughly bell-shaped cluster of points (the gaussian distrubution), and that the two clusters have about the same shape and spread (same covariance matrix), but are centered in different places (with different means).

This shared-covariance assumption produces a **linear decision boundary**.

LDA is useful as the first baseline because it is simple and computationally efficient. CSP followed by a linear discriminant classifier is a well-established motor-imagery EEG approach.[^ramoser][^mne-example]

### 9) What should we measure?

#### Accuracy

Accuracy is:

`number of correct predictions / total predictions`

Accuracy is easy to interpret, but it can become misleading if one class is substantially more common than another.

#### Balanced accuracy

Balanced accuracy is defined as the average recall obtained for each class.[^sklearn-balanced]

Recall for a class is the amount of trials from that true class that the model correctly identifies.

For two classes:

`balanced accuracy = (recall_left + recall_right) / 2`

This means that performance on the left and right classes contributes equally even when their numbers differ.

Balanced accuracy will be the primary metric for the first baseline.

Ordinary accuracy will also be reported.

Performance near 0.5 represents approximately chance-level discrimination when the two classes are balanced.

---

### 10) Report fold-level performance

Cross-validation should not produce only one final number.

For example:

`Run 4 held out → balanced accuracy = ...`

`Run 8 held out → balanced accuracy = ...`

`Run 12 held out → balanced accuracy = ...`

Then calculate:

`mean balanced accuracy`

and report the individual fold values as well.

Large differences between runs may reveal instability. Therefore we calculate different values. 

### 11) Hyperparameter selection can cause optimistic results

A parameter is values the algorithm learns from

A hyperparameter are decision about how the learning algorithm should operate. 

The CSP algorithm learns the components, But we chose how many components before fitting.

Suppose several CSP settings are tested:

`2 components`

`4 components`

`6 components`

`8 components`

If the setting with the highest cross-validation score is selected, the validation results have now influenced the model choice.

The socres are no longer unbiased estimates of generalization performance.

Remember we want to choose hyperparameters with training/validation data, not the final test data.

For the first baseline, we avoid this problem by defining`CSP n_components = 4` before looking at the classification results.

Later, model selection should use **nested cross-validation**:

`inner cross-validation → which hyperparameters?`

`outer cross-validation → how well does this selection generalize?`

The first Week 5 baseline does not require nested CV yet. We wnat to create a starting point first. 

---

### 12) Week 5 baseline protocol

#### Model

`preprocessed EEG`

→ `CSP (4 components)`

→ `log-power features`

→ `LDA`

→ `left/right prediction`

#### Evaluation

Leave one run out at a time:

`train runs 8 + 12 → test run 4`

`train runs 4 + 12 → test run 8`

`train runs 4 + 8 → test run 12`

#### Primary metric

`balanced accuracy`

#### Secondary metric

`accuracy`

#### Leakage rule

CSP and LDA must both be fitted **inside each training fold**.

### Initial scientific question

> Can a simple and interpretable CSP + LDA model distinguish imagined left- from right-fist movement in an unseen recording run from the same subject?

This is a within-subject baseline. Not cross-subject generalization


## Week 5 References

[^ramoser]: Ramoser, H., Müller-Gerking, J., & Pfurtscheller, G. (2000). Optimal spatial filtering of single trial EEG during imagined hand movement. *IEEE Transactions on Rehabilitation Engineering, 8*(4), 441–446. https://doi.org/10.1109/86.895946.

[^erd]: Pfurtscheller, G., & Lopes da Silva, F. H. (1999). Event-related EEG/MEG synchronization and desynchronization: Basic principles. *Clinical Neurophysiology, 110*(11), 1842–1857. https://doi.org/10.1016/S1388-2457(99)00141-8.

[^mne-csp]: MNE Developers. *mne.decoding.CSP — MNE-Python documentation*. MNE-Python. Used for CSP input structure, supervised fitting, spatial-filter transformation, average-power features, log transformation, and component selection.

[^mne-example]: MNE Developers. *Motor imagery decoding from EEG data using the Common Spatial Pattern (CSP) — MNE-Python example*. Used as a reference implementation for motor-imagery decoding with CSP and a linear discriminant classifier.

[^sklearn-cv]: scikit-learn Developers. *Cross-validation: evaluating estimator performance — scikit-learn User Guide*. Used for train/test separation, k-fold cross-validation, grouped cross-validation, and leave-one-group-out methodology.

[^sklearn-leakage]: scikit-learn Developers. *Common pitfalls and recommended practices: Data leakage — scikit-learn User Guide*. Used for the rule that fitted transformations must learn parameters only from training data and for preventing leakage during preprocessing.

[^sklearn-pipeline]: scikit-learn Developers. *sklearn.pipeline.Pipeline — scikit-learn documentation*. Used for chaining CSP and LDA so that trainable transformations and the final estimator are fitted together within cross-validation.

[^sklearn-lda]: scikit-learn Developers. *Linear and Quadratic Discriminant Analysis — scikit-learn User Guide*. Used for the probabilistic formulation of LDA, the shared-covariance assumption, and the resulting linear decision surface.

[^sklearn-balanced]: scikit-learn Developers. *sklearn.metrics.balanced_accuracy_score — scikit-learn documentation*. Used for the definition of balanced accuracy as the average recall across classes.