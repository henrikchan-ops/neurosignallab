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

## Week 6 — Cross-Subject Generalization

### 1) Goal

The goal of Week 6 is to test whether the CSP + LDA motor-imagery
baseline can generalize to a completely unseen subject.

Week 5 tested within-subject, across-run generalization.

Week 6 instead tests cross-subject generalization:

training:
Subjects A, B, C, ...

testing:
Subject Z — completely unseen during fitting

The preprocessing and model are kept fixed so that the main change
between the experiments is the level of generalization being tested.

The fixed baseline remains:

- unilateral left- vs right-fist motor imagery
- runs 4, 8 and 12
- all 64 EEG channels
- common-average reference
- 7–30 Hz band-pass filtering
- +1 to +4 s machine-learning window
- four CSP components
- LDA classifier
- balanced accuracy as the primary evaluation metric

The EEG Motor Movement/Imagery Dataset contains the same motor-imagery
protocol across 109 subjects, with 64-channel EEG sampled at 160 Hz.
Runs 4, 8 and 12 correspond to imagined unilateral left/right fist
movement. [1]


### 2) Levels of generalization

A model can be evaluated at different levels.

Easy generalization -> A random trial split tests whether the model can classify new trials
when the same subjects may already be represented in the training set.

Harder generalization -> A leave-one-run-out split tests whether the model can generalize to a
new recording run from the same subject.

Even harder generalization -> A leave-one-subject-out split tests whether the model can generalize
to a person whose data were completely absent during model fitting.

Samples from the same subject share person-specific physiology, electrode topology and other charactiristics. We want to answer if the model can recognize left-right imagery based on generalization of data, and not the subject-specific quirks.

Grouped
cross-validation keeps samples belonging to the same individual
together in either training or test folds. [2]

### 3) Leave-One-Subject-Out Cross-Validation

Leave-One-Subject-Out (LOSO) cross-validation can be implemented using
LeaveOneGroupOut, with subject identity used as the group variable.

For 109 subjects:

Fold 1:
train = Subjects 2–109
test = Subject 1

Fold 2:
train = Subjects 1, 3–109
test = Subject 2

...

Fold 109:
train = Subjects 1–108
test = Subject 109

Every subject therefore acts as the test subject once.

The important change from the Week 5 cross-validation algorithm
is the groups variable.

LeaveOneGroupOut guarantees that all observations belonging to the
held-out group are excluded from its paired training set, as similar to Week 5. [2]


### 4) Subject-dependent vs subject-independent decoding

Subject-dependent decoding means that EEG from the target subject
participates in model fitting.

The Week 5 experiment was subject-dependent because the model was still trained using other runs from the
same individual.

Subject-independent decoding means that the target subject does not
participate in fitting.

The Week 6 baseline is subject-independent because the held-out
subject contributes no EEG to CSP or LDA fitting.

This makes it harder for CSP, as spatial patterns could vary from subject to subject. It needs to find patterns consistent across people, which is fundamentaly harder.


### 5) Inter-subject and intra-subject variability

Intra-subject variability refers to variatn in EEG within one person,
for example across runs, sessions or days.

Inter-subject variability refers to differences in EEG between
different people.

Sensorimotor EEG can vary substantially both within and between
subjects. These differences reduce the transferability of models
trained on one set of EEG recordings to different subjects or
sessions. [3]

Potential contributors to inter-subject variability include:

- differences in neurophysiology
- differences in sensorimotor rhythm strength and timing
- anatomical differences
- different mappings between neural sources and scalp electrodes
- differences in motor-imagery cognitive strategy
- attention and psychological state
- recording-related variability

Therefore, the same experimental class label does not imply that every
subject produces an identical EEG feature distribution.


### 6) Domain and domain shift

A domain is a distribution of data. For instance between CSP features.

For the cross-subject experiment, each participant creates its own separate domain.

For one LOSO fold:

source domains = training subjects
target domain = held-out subject

The prediction task remains the same:

left vs right motor imagery

but the EEG distribution may change between source and target
subjects.

This is called domain shift.

The literature describes inter-subject and inter-session
variability as causes changing EEG feature distributions that can
reduce model generalization. [3]

#### Definitions of domains

**Domain generalizaton** - subject-independent cross-subject generalization: learning using source-domain data and generalize to unseen domain without the target domain included in model fitting[5]

**Domain adaptation** - When the target domain is included in the traning fold

**Subject-specific calibration** - When target domain is included in the training fold, but the trials are not included in the test-fold
. Subject-specific BCI systems often require labelled EEG
from a new user before the model can work well. Since we are training the model to be subject-independent, we want to remove the need for calibration[3,6]

**Transfer learning** - using knowledge learned in source domain to improve learning in different target settings. This knowledge can be transfered in multiple stages of the pipeline, and reduces the need for subject-specific calibration[6]

Potential future methods include:

- feature or covariance alignment
- regularized/transfer CSP
- Riemannian methods
- subject-adaptive models
- deep domain adaptation


#### Why are we not solving domain shift yet?

Because we want to create a benchmark and baseline, that later can be improved with different alignment methods and transfer-learning. 

### 7) Covariate shift

Covariate shift is a more specific type of distribution shift.

Covariate shift means the distribution of the inputs changes between training and testing, while the underlying relationship between inputs and labels is assumed to stay the same.

Tne inputs from the train and test set could be different:

P_train(X) != P_test(X)

while the relationship between input and target is assumed to remain
approximately stable:

P_train(y | X) ~= P_test(y | X)

However, that assumption is not always the case. The target subject could have a distribution wildly different to the source domains. But the same way of classifying stays the same. 

The meaning of inputs stays the same, but certain datasets can expose the classification to different input.

In EEG, inter-subject variability is often discussed using
covariate-shift terminology. [3]

However, not every subject difference ends up retaining the relationship.

Therefore, "domain shift" is a safer general term for the Week 6
problem.

#### What happens to CSP across subjects?

Cross-subject CSP asks:

Which weighted combinations of electrodes distinguish left from right
imagery across the training population and also transfer to a new
person?

The spatial filters learned from the training subjects must
capture discriminative patterns that are sufficiently consistent
between people.

Inter-subject differences can make this difficult because the
covariance and spatial structure learned from the training population
may not represent the held-out subject well.

#### What happens to LDA across subjects?

After CSP, each trial is represented by a small number of CSP
log-power features.

With four CSP components LDA learns the class means and a shared covariance structure from the
training-subject features.

If the unseen subject's feature distribution is shifted relative to
the training population, the learned LDA boundary may not transfer
well.

Cross-subject failure can therefore result from the CSP
representation failing to transfer, the LDA decision boundary failing
to transfer, or both.


### 8) Data leakage in cross-subject evaluation

Data leakage occurs when information that should not be available influences model fitting or model selection. [7]

For a held-out subject, no information from that subject may influence
learned components such as:

- CSP spatial filters
- LDA parameters
- learned feature scaling
- PCA or feature selection
- learned normalization
- hyperparameter selection

Fitting CSP
before the cross-validation split would allow EEG and labels from the
test subject to influence the feature representation.

For each LOSO fold:

training subjects
→ fit CSP
→ transform training EEG
→ fit LDA

held-out subject
→ apply already-fitted CSP
→ apply already-fitted LDA
→ prediction

A Pipeline helps protect against leakage by ensuring that learned
transformations are fitted using the same training subset as the
classifier. [7]


### 9) Fixed preprocessing vs learned preprocessing

The general rule is:

fixed predefined operation
→ can be applied consistently

data-learned transformation
→ fit only using training data

### 10) Structure of the combined dataset

Week 5 processed each subject separately:

X.shape ≈ (45, 64, 481)
y.shape ≈ (45,)
groups = recording runs

Week 6 combines trials from all subjects:

X.shape ≈ (all trials, 64, 481)
y.shape ≈ (all trials,)
groups.shape ≈ (all trials,)

For each trial i:

X[i] = EEG epoch
y[i] = left/right class
groups[i] = subject that produced the epoch

Balanced accuracy also remains the primary metric.

### 11) Cohort-level evaluation

Each LOSO fold produces one balanced-accuracy score for one held-out
subject.

The result will therefore contain:

Subject 1 BA
Subject 2 BA
...
Subject 109 BA

The main statistics will include:

- mean subject-level balanced accuracy
- median
- range
- distribution across subjects

Averaging the subject-level scores gives each subject equal weight
rather than allowing subjects with more trials to contribute more to
the cohort score.


### 12) Comparison with Week 5

Week 5 produced one within-subject balanced-accuracy score per subject.

Week 6 will produce one cross-subject balanced-accuracy score per
subject.

The important comparison becomes:

subject | within-subject BA | cross-subject BA

We want to figure out:
How much does decoding performance change when subject-specific
training information is removed?

If cross-subject performance decreases substantially, this would
suggest that information useful for within-subject decoding does not
transfer perfectly between individuals.

## 13) What Week 6 will not do

The first cross-subject baseline will not:

- tune CSP component count
- change the frequency band
- change the time window
- introduce another classifier
- use transfer learning
- perform domain adaptation
- use target-subject calibration
- exclude subjects because their performance is poor
- introduce deep learning

The Week 6 result must first establish how the original CSP + LDA
baseline behaves under strict subject-independent evaluation.


### 14) Main questions I should be able to answer

1. Why does random trial splitting not measure performance on unseen
   subjects?

Because trials from the same subject can occur in both training and
testing, allowing the model to learn subject-specific structure.

2. What does LOSO do?

It removes every trial belonging to one subject from the training set
and uses that entire subject as the test set.

3. Why must CSP remain inside the Pipeline?

Because CSP is supervised and learns its spatial filters from the EEG
and class labels. The held-out subject must not influence those
filters.

4. Why is cross-subject decoding difficult?

Because EEG distributions differ between individuals, so spatial
features and decision boundaries learned from training subjects may
not transfer perfectly to a new person.

5. What is domain shift?

A difference between the data distributions encountered during
training and testing.

6. What is the difference between domain generalization and domain
adaptation?

Domain generalization predicts an unseen domain without using that
domain for model fitting. Domain adaptation uses some information from
the target domain to adapt the model.

7. Why do we keep the Week 5 model settings unchanged?

So that differences between within-subject and cross-subject
performance primarily reflect the change in the generalization
problem rather than simultaneous changes to the model.


## References Week 6

[1] Goldberger AL et al. / PhysioNet. EEG Motor Movement/Imagery
Dataset v1.0.0. PhysioNet. Dataset documentation.

[2] scikit-learn developers. Cross-validation: evaluating estimator
performance. Sections on grouped data and LeaveOneGroupOut.
scikit-learn User Guide.

[3] Saha S, Baumert M. Intra- and Inter-subject Variability in
EEG-Based Sensorimotor Brain Computer Interface: A Review.
Frontiers in Computational Neuroscience. 2020;13:87.
doi:10.3389/fncom.2019.00087.

[4] MNE-Python developers. mne.decoding.CSP documentation.
MNE-Python.

[5] Zhou K, Liu Z, Qiao Y, Xiang T, Loy CC.
Domain Generalization: A Survey.
IEEE Transactions on Pattern Analysis and Machine Intelligence.
2023;45(4):4396-4415.
doi:10.1109/TPAMI.2022.3195549.

[6] Wu D, Jiang X, Peng R.
Transfer learning for motor imagery based brain-computer interfaces:
A tutorial.
Neural Networks. 2022;153:235-253.
doi:10.1016/j.neunet.2022.06.008.

[7] scikit-learn developers.
Common pitfalls and recommended practices: Data leakage;
Pipeline documentation.
scikit-learn User Guide.

[8] scikit-learn developers.
balanced_accuracy_score documentation.
scikit-learn User Guide.

[9] Lotte F, Bougrain L, Cichocki A, Clerc M, Congedo M,
Rakotomamonjy A, Yger F.
A review of classification algorithms for EEG-based
brain-computer interfaces: a 10 year update.
Journal of Neural Engineering. 2018;15(3):031005.
doi:10.1088/1741-2552/aab2f2.

## Week 7 — Nested Cross-Validation and Controlled Hyperparameter Selection

### 1) Goal

The goal of Week 7 is to determine whether controlled hyperparameter
selection can improve the subject-independent CSP + LDA motor-imagery
decoder without producing a biased generalization performance.

Week 6 used a fixed model with 4 CSP-components. 

Week 7 introduces model selection: Can CSP hyperparameters be selected using only training-subject data in a way that improves performance on completely unseen subjects?

### 2) Parameters vs hyperparameters

Parameters are values learned directly during model fitting.

Examples:

CSP:
- spatial-filter weights

LDA:
- class means
- shared covariance structure
- decision coefficients

Hyperparameters control the model-fitting procedure and are chosen
outside the ordinary fit operation. [1]

Examples relevant to CSP include:

- n_components
- covariance regularization (`reg`)

A hyperparameter is not directly estimated by CSP or LDA during
`fit()`.

However, once validation performance is used to choose a
hyperparameter, the hyperparameter choice has effectively been learned
from data.

Therefore hyperparameter selection also requires separation from the
final test data too.

### 3) Model fitting, model selection, and model assessment

These are three different processes.

Model fitting:

training data
→ learn CSP filters
→ learn LDA parameters

Model selection:

validation data
→ compare candidate hyperparameters
→ choose configuration

Model assessment:

independent test data
→ estimate how the entire chosen procedure generalizes

The validation data are allowed to influence model selection.

The test data is not. We do not want the test data to be part of model selection. The test data should be evaluated with an already selected model.[1,2]

#### What is selection bias?

Selection bias is when you select the model based on the best test performance. 

We want the selection to be bias, to truly figure out what the best overall model is. Selecting the model based on test result may cause the model to fit noisy performance, instead of differences between algorithms.

Cawley and Talbot showed that the model-selection criterion itself can
be overfit, producing optimistic performance estimates. [3]

Varma and Simon similarly showed that using the same cross-validation
procedure both to optimize a classifier and to estimate its error can
produce biased results. [2]


### 4) Nested cross-validation

Nested cross-validation separates hyperparameter selection from final
performance estimation.

It has two loops:

OUTER CV → estimates generalization performance

INNER CV → selects hyperparameters

For the Week 7 cross-subject experiment the outer fold consists of 1 subject as the test split, and 108 as the train split. Then the inner fold splits 4/5 of the subjects into training split and 1/5 into model validation splits.

Subject 1 is completely excluded while hyperparameters are selected.

After selecting the best configuration, the model is refitted on all
outer-training subjects and evaluated once on Subject 1.

The process is repeated for every subject. [1–4]

#### Outer Leave-One-Subject-Out evaluation

The outer loop retains the Week 6 evaluation structure.

This means only one subject is in each of the held-out groups.

This allows the tuned model to be compared directly with the Week 6
fixed CSP + LDA baseline.


#### Inner group-aware cross-validation

The inner cross-validation must also preserve subject identity.

We do not want to optimize the hyperparameters for new trials from known subjects

GroupKFold function guarantees that one subject does not occur on both sides of
the same inner-split. [5]

### 5) Why the inner loop does not need LOSO

It would be possible to use Leave-One-Subject-Out for both the inner
and outer loops.

However, this would require approximately 108 inner folds for every
outer fold and for every hyperparameter configuration.

Nested cross-validation is already computationally taxing.

A smaller GroupKFold maintains the essential subject-separation rule
while making hyperparameter search substantially more manageable.

Leave-one-out-style validation can also have relatively high
variance and computational cost. [4,5]


### 6) GridSearchCV

GridSearchCV function performs exhaustive search over a predefined set of
hyperparameter combinations. [6]

A grid search contains:

- a model pipeline -> CSP/LDA

- a parameter grid

- a cross-validation splitter -> inner cross-validation group

- a scoring function -> balanced accuracy

GridSearchCV tests every candidate combination across the inner folds
and chooses the configuration with the highest mean inner validation
score.

After that, we can refit all outer-training subjects to the new configuration. 

Keep in mind GridSearchCV is not the final performance.

### 7) Pipeline hyperparameter names

Parameters inside a scikit-learn Pipeline are addressed using:

step_name__parameter_name

Two underscores are used. [7]

For a Pipeline containing steps called:

"csp"
"lda"

CSP's number of components becomes:

csp__n_components

and CSP's covariance regularization becomes:

csp__reg


### 8) CSP n_components

`n_components` controls how many CSP components are retained.

MNE explicitly states that CSP `n_components` should be selected using
cross-validation. [8]

Too few components may discard useful discriminative information.

Too many components may introduce weaker or noisy spatial directions
and increase model variance.

Therefore more components do not automatically mean better
performance.


### 9) Bias and variance

Bias describes systematic error caused by a model
being too constrained to capture relevant structure.

Variance describes sensitivity to the particular training dataset.


simpler model:
- higher bias
- lower variance

more flexible model:
- lower bias
- potentially higher variance

Hyperparameters influence this trade-off.

For CSP:

few components → simpler representation

many components → richer representation → potentially more noise and instability

The optimal choice should be based on validation performance rather
than training performance. [9]


### 10) CSP covariance regularization

CSP depends on class covariance matrices.

Basically the sum of left and right signals describe spatial covariance of the EEG.

An empirical covariance estimate follows the available training data
closely but may be unstable.

Regularization makes the covariance estimate more constrained and
potentially more stable. Basically, it makes small fluctuations have smaller effect.

MNE CSP exposes this through the `reg` parameter. [8]

`reg=None` uses empirical covariance estimation.

Other supported settings can introduce shrinkage or alternative
regularized covariance estimators.

### 11) Shrinkage

Shrinkage combines the empirical covariance estimate with a simpler,
more stable covariance structure.

A looser covariance structure makes small fluctuations in covariance have less effect.

If its shown mathematically: 

Sigma_regularized = 
(1 - alpha) * Sigma_empirical
+
alpha * Sigma_simple

Small alpha:
→ mostly empirical covariance

larger alpha:
→ stronger regularization

Regularization introduces some bias but can reduce variance.

Methods such as Ledoit-Wolf and OAS estimate shrinkage in principled
ways and are supported by MNE covariance estimation. [10]


### 12) CSP regularization vs LDA regularization

CSP covariance regularization and LDA covariance regularization act at
different stages.

CSP regularization affects EEG channel variance, which affects CSP spatial filters

LDA regularization affects CSP feature covariance, which affects the LDA classifier


Scikit-learn supports shrinkage for LDA when compatible solvers such
as `lsqr` or `eigen` are used. [11]

The initial Week 7 experiment should keep LDA fixed so that the search
focuses on the CSP representation. We do not want multiple major changes to the model. 


### 13) The scoring metric

Balanced accuracy remains the primary metric.

The same metric should be used for inner model selection and outer model evaluation

Therefore GridSearchCV should explicitly optimize balanced accuracy.

The choice of scoring metric determines what the search means by the
"best" model.


### 14) Grid search vs randomized search

GridSearchCV evaluates every parameter combination specified in a
grid. [6]

RandomizedSearchCV samples a fixed number of configurations from a
parameter space instead of testing every possible combination. [13]

Randomized search is useful when the parameter space is large.

For Week 7, we only have a small amount of hyperparameters to consider, so that creates smaller candidate sets to search through. With larger distributions and grids, we would choose th erandomized search


### 15) The search space is part of the experiment

Searching more candidate configurations provides more opportunities
to fit noise in the validation estimates.

The candidate hyperparameter grid itself is part of the
experimental design.

The search space should be small, scientifically plausable and defined before examining test results. 

Repeatedly modifying the grid after seeing test performance gradually
turns the test dataset into development data. [3]

Keep in mind, GridSearchCV's `best_score_` represents the mean inner validation score
of the selected hyperparameter configuration.

### 16) Computational cost

Nested cross-validation requires many model fits.

If:

C = number of candidate configurations
K = number of inner folds
O = number of outer folds

then the inner search requires approximately:

C × K × O

model fits.

For example:

12 candidates
× 5 inner folds
× 109 outer folds
=
6540 inner fits

plus refitting the selected model in every outer fold.

This is why we use GroupKFold and keep the search space compact. 


### 17) What the final nested result represents

Nested CV does not necessarily identify one universal
hyperparameter configuration.

Different outer folds may choose different settings.

For example:

Subject 1 outer fold:
best n_components = 6

Subject 2:
best n_components = 4

Subject 3:
best n_components = 8

The nested result therefore estimates the performance of a procedure using this workflow:

Given training subjects, use grouped cross-validation to select the hyperparameters, refit the model, and apply it to an unseen person.

### 18) Hyperparameter-selection stability

The selected hyperparameters can be recorded for every outer fold.

This allows questions such as:

How often was each n_components value selected?

Did one covariance regularization method dominate?

Were the chosen settings highly variable across outer folds?

Stable selections may indicate that one configuration is favored by the training data.

Highly variable selections may indicate that the optimum is affected by particular subjects used for training.

This shoud be interpreted carefully.


### 19) Tuned vs fixed baseline

The main Week 7 result will compare:

Week 6:
fixed CSP + LDA

vs

Week 7:
nested-CV-selected CSP + LDA

Both should use the same outer subject-level evaluation.

For every subject:

subject
| fixed cross-subject BA
| tuned cross-subject BA
| difference

This will determine whether the model-selection procedure actually
improves performance on unseen subjects.

Inner CV estimates contain noise, and a configuration that wins the
inner search does not necessarily generalize better to the outer test
subject.

Brain-decoding studies have shown that cross-validation estimates can
have substantial variability and that parameter tuning does not always
outperform sensible default models. [4]

### 20) Main Week 7 leakage rules

The outer test subject must not influence:

- CSP fitting
- LDA fitting
- hyperparameter selection
- covariance regularization selection
- feature selection
- learned normalization
- model-family selection

The inner validation subjects may influence hyperparameter selection,
because that is their purpose.

Everything learned from data must be fitted within the appropriate
training split.

## References

[1] scikit-learn developers.
Tuning the hyper-parameters of an estimator.
scikit-learn User Guide.

[2] Varma S, Simon R.
Bias in error estimation when using cross-validation for model
selection.
BMC Bioinformatics. 2006;7:91.
doi:10.1186/1471-2105-7-91.

[3] Cawley GC, Talbot NLC.
On Over-fitting in Model Selection and Subsequent Selection Bias in
Performance Evaluation.
Journal of Machine Learning Research.
2010;11:2079–2107.

[4] Varoquaux G, Raamana PR, Engemann DA, Hoyos-Idrobo A,
Schwartz Y, Thirion B.
Assessing and tuning brain decoders: Cross-validation, caveats, and
guidelines.
NeuroImage. 2017;145(Pt B):166–179.
doi:10.1016/j.neuroimage.2016.10.038.

[5] scikit-learn developers.
GroupKFold and grouped cross-validation documentation.
scikit-learn User Guide.

[6] scikit-learn developers.
GridSearchCV documentation.
scikit-learn.

[7] scikit-learn developers.
Pipeline documentation.
scikit-learn.

[8] MNE-Python developers.
mne.decoding.CSP documentation.
MNE-Python.

[9] scikit-learn developers.
Validation curves: plotting scores to evaluate models.
Section on bias, variance, underfitting, and overfitting.
scikit-learn User Guide.

[10] Engemann DA, Gramfort A.
Automated model selection in covariance estimation and spatial
whitening of MEG and EEG signals.
NeuroImage. 2015;108:328–342.
doi:10.1016/j.neuroimage.2014.12.040.

[11] scikit-learn developers.
Linear and Quadratic Discriminant Analysis.
Section on shrinkage and covariance estimation.
scikit-learn User Guide.

[12] scikit-learn developers.
balanced_accuracy_score documentation.
scikit-learn.

[13] scikit-learn developers.
RandomizedSearchCV documentation.
scikit-learn.

[14] Blankertz B, Tomioka R, Lemm S, Kawanabe M, Müller KR.
Optimizing Spatial Filters for Robust EEG Single-Trial Analysis.
IEEE Signal Processing Magazine.
2008;25(1):41–56.
doi:10.1109/MSP.2008.4408441.

## Week 8 — Statistical Validation, Uncertainty, and Robustness

### 1) Goal

The goal of Week 8 is to determine how much confidence can be placed
in the classical EEG decoding results in Weeks 5–7.

The previous experiments produced point estimates:

Week 5:
within-subject CSP + LDA
mean balanced accuracy ≈ 0.597

Week 6:
fixed cross-subject CSP + LDA
mean balanced accuracy ≈ 0.565

Week 7:
nested-tuned cross-subject CSP + LDA
mean balanced accuracy ≈ 0.575

These numbers describe observed performance, but they do not by
themselves quantify uncertainty or statistical evidence.

Week 8 therefore asks:

1. How uncertain are the cohort-level performance estimates?
2. Is the within- to cross-subject performance change convincing?
3. Did nested hyperparameter tuning produce a systematic improvement?
4. How should chance-level decoding be assessed?
5. Are the conclusions subject variability and known data irregularities?


### 2) Unit of statistical inference

The statistical unit should match the scientific unit of
generalization.

Therefore the primary unit of inference is the subject:

n = 109 subjects

not:

n = 4898 trials

Trials belonging to the same subject are correlated and cannot be
treated as thousands of independent participants.

Treating correlated trials as independent observations would create
pseudoreplication and artificially underestimate uncertainty.

Subject-level resampling and paired comparisons should therefore be
used for the main cohort analyses.


### 3) Point estimates and uncertainty

A point estimate is one numerical estimate of performance.

For example:

mean cross-subject BA = 0.565

A different sample of subjects would not produce exactly the same
number.

Therefore predictive performance should be reported together with an
estimate of uncertainty.

However, cross-validation results in neuroimaging can have substantial
uncertainty, and variance calculated across CV folds and underestimate uncertainty across folds since they are not independent. Interpreting fold-to-fold variability is not a reliable standard error. [1,2]


We want to know how uncertain these point estimates are. 

### 4) Confidence intervals

A confidence interval gives a range of possible values around an estimated point.

For example:

mean BA = 0.565
95% CI = [0.548, 0.582]

A narrow interval indicates greater precision.

A wide interval indicates greater uncertainty.

A 95% confidence interval should not be interpreted as a 95%  probability that the true parameter lies inside the
particular observed interval.

Instead, it meants that across repeated datasets, approximately 95% of intervals
constructed by the same procedure would contain the target point estimate.


### 5) Bootstrap resampling

The bootstrap estimates uncertainty by repeatedly resampling the
observed units with replacement units. [3]

This is used for scores that do not assume normal distribution.

For this project, the resampling unit should be the subject.

A bootstrap replicate contains 109 subject observations sampled with
replacements from the original 109 subjects.

Some subjects can appear multiple times and some may not appear in a
particular replicate.

They all end up creating a mean BA of the bootstrap sample.


Repeating this thousands of times produces a bootstrap distribution.

This can be used to estimate:

- confidence intervals
- standard errors
- uncertainty in mean balanced accuracy
- uncertainty in paired model differences

### 6) Paired bootstrap

When comparing two models evaluated on the same subjects, the
observations are paired.

For Subject i:

fixed_i
tuned_i

belong together.

Bootstrap resampling must preserve that pairing.

If Subject i is sampled, both its fixed and tuned scores must be
included.

The primary statistic can then be:

difference_i = tuned_i - fixed_i

and bootstrap samples can be used to estimate a confidence interval
around the mean paired difference.


### 7) Confidence interval vs hypothesis test

A confidence interval addresses:

How large could the effect possible be?

A hypothesis test addresses:

Would an effect of this size be unusual if some hypothesis were true (we usually use th enull hypothesis)?

### 8) Null and alternative hypotheses

For a paired comparison of Week 6 and Week 7, a null hypothesis can be:

H0:
mean(tuned BA - fixed BA) = 0

A two-sided alternative is:

H1:
mean(tuned BA - fixed BA) != 0

A one-sided alternative would instead test a pre-specified direction.

Because the Week 7 results have already been observed, a two-sided test
is preferable for the formal fixed-vs-tuned comparison. We just want to know whether or not there is significant difference between the two methods. 


### 9) P-values

A p-value is calculated under the assumption that the null hypothesis
is true.

It represents how unusual the observed statistic would be under compared to assumption of the null hypothesis.

If p= 0.02: 
It means that, assuming the null hypothesis is true, hese results would occur 2% of the time in this procedure.


### 10) Statistical vs practical significance

A statistically detectable difference can still be practically small.

For example, the Week 7 tuned model improved mean balanced accuracy by
approximately:

+0.0099

or roughly one balanced-accuracy percentage point.

Typically a p < 0.05 signifies statistical significance, meaning that the null-hypothesis would not hold true. However, its practical importance still depends on the
size of the effect and its confidence interval.

Therefore results should be described using:

effect size
+
confidence interval
+
p-value

rather than only:

significant / non-significant


### 11) Effect size

Effect size tells us how large the effect is.

The most interpretable effect size for the current
experiments is the difference in balanced accuracy.

For two models:

Delta BA =
BA_B - BA_A

For example:

Delta BA = +0.010

means that Method B improved balanced accuracy by approximately one
percentage point on average.

### 12) Paired comparisons

Week 6 and Week 7 were evaluated on the same 109 outer test subjects.

Therefore their results are paired.

For each subject:

d_i =
tuned_i - fixed_i

The analysis should focus on the collection of paired differences
rather than treating the two sets of scores as independent samples.


### 13) Paired permutation test

A paired permutation test evaluates whether the assignment of the two
methods within each subject is exchangeable under the null
hypothesis. [4]

For one subject:

fixed_i
tuned_i

the values can either remain in their observed positions or be swapped.

Across subjects, these swaps are performed randomly and the test
statistics, such as the mean paired difference, is recalculated.

Repeating this procedure generates distribution that could provide evidence for and against H0.


#### Sign-flip interpretation of paired permutation

For paired differences:

d_i = tuned_i - fixed_i

swapping the two methods is equivalent to changing:

d_i -> -d_i

Therefore a paired permutation test can also be understood as randomly
flipping the sign of each subject's difference under the null.

#### Why do we not do a t-test?

A paired t-test requires many distributional assumptions, such as the data fitting into a normal distribution. 

The BA differences are potentiionally bounded, contain zeros, descrete or skewed. 

### 14) Wilcoxon signed-rank test

The Wilcoxon signed-rank test is a paired non-parametric test. Meaning it does not use the given values of the BA difference, but assigns them a rank depending on how much larger or smaller their value is compared to other data. 

This makes it so that extremely large or small outlier data does not interfere with our analysis of significance. [5]

However, the current data contain bounded values, many exact ties, and
a directly interpretable paired design.

A permutation test is therefore a particularly transparent primary
analysis for this project.


### 15) Chance level vs statistical significance

For binary balanced accuracy:

expected chance BA = 0.5

However:

observed BA > 0.5

does not automatically imply statistically significant decoding by the model.

Combrisson and Jerbi demonstrated that theoretical chance level and
the statistical significance threshold for decoding accuracy are not
equivalent. [6]

Therefore 0.50 should be interpreted as the expected binary chance
value, not an automatic significance threshold.

### 16) Label-permutation testing

Classifier-level permutation testing can test the null hypothesis when
there is no meaningful relationship between EEG  and class
labels. [7]

We want to figure out if the model is exploiting information between the EEG and the labels.

The procedure is:

original EEG + labels
→ compute real classifier performance

shuffle labels
→ rerun classifier evaluation
→ obtain null score

repeat many times
→ null distribution

If there is no relationship between EEG and the labels, the score should look similar to shuffled-label scores.

Ojala and Garriga describe label-permutation testing as a way to
evaluate whether a classifier has found real class structure, or is abusing the label markings. [7]


### 17) Exchangeability and restricted permutations

Labels should only be permuted in ways that preserve important
experimental structure.

Unrestricted shuffling across every trial and
subject would remove everything about the experiment we want to test.

A more appropriate null-dataset can preserve:

- subject identity
- run identity
- trial counts
- class counts

while destroying the EEG-label relationship.

A possible strategy is therefore to permute left/right labels within
subject/run blocks.

The validity of a permutation test depends on which labels you can swap without damaging the experiment. That is what exchangeability means.


### 18) Full-pipeline permutation testing

If the real prediction procedure contains data-driven model selection,
the same model-selection procedure should normally be rerun under each
permutation.

For Week 7:

shuffle labels
→ inner hyperparameter selection
→ refit
→ outer evaluation

for each permutation

Selecting hyperparameters using real labels and then permuting
only the final classification stage would not reproduce the null
distribution of the complete algorithm. The whole pipelin must be permutated.

This makes full Week 7 label-permutation testing computationally very
expensive.


### 19) Practical permutation strategy

If you have 1000 label permutations put into the nested week 7 procedure -> it creates millions of model fits.

Week 8 should distinguish:

1. Subject-level statistical inference using the already-computed outer
subject scores to pair permutation/bootstrap methods.

2. Rerun of full classifier-level  with label-permutations. 

Subject-level paired permutation tests are computationally inexpensive.

A full nested Week 7 classifier permutation would require millions of
model fits if thousands of permutations were used.

A classifier-level chance test is therefore more practical
for the Week 6 procedure.


### 20) Empirical permutation p-values

If B permutations are performed, and C amount of permutation
are at least as statistically significant as the observed data, an empirical
p-value can be calculated as:

p = (C + 1) / (B + 1)

This prevents a permutation test from reporting an
impossible p-value of exactly zero. [8]

The minimum possible p-value therefore depends on the number of
permutations.

For example:

999 permutations
→ minimum p = 0.001

9999 permutations
→ minimum p = 0.0001

### 21) Type I and Type II errors

A Type I error occurs when a null hypothesis is rejected even though
it is true.

A Type II error occurs when a genuine effect exists but the test fails
to detect it.

### 22) Statistical power

Power is the probability of detecting an effect when the true effect of a particular size exists. 

Power generally increases with:

- larger true effects
- more independent subjects
- lower variability

After data collection, confidence intervals around the effect are more
informative than "observed power" calculations.


### 23) Multiple comparisons

Testing many hypotheses creates opportunities for false
positive findings.

For example, separately testing:

- multiple model comparisons
- 109 individual subjects
- many channels
- many frequency bands

can greatly increase the probability of at least one false positive.

Therefore multiple-testing correction must be considered whenever
several related hypotheses are evaluated.


### 24) Holm correction

Holm's sequential procedure controls the family-wise error rate. [9]

Family-wise error rate refers to the probability of making at least
one false rejection within a defined family of hypotheses.

Holm correction is useful when there are a small number comparisons. It is a lot less conversative than the typical Bonferroni correction.

For Week 8, if the two main comparisons are:

Week 5 vs Week 6
Week 6 vs Week 7

Holm correction across these two tests is a reasonable
choice.


### 25) False discovery rate

False discovery rate asks, among all results i call significant, what fraction do i expect to be false.

FDR methods are useful for larger exploratory families, such as
testing significance separately across many subjects, channels, or
features.

They are usually less conservative than family-wise error control.

### 26) Cross-validation dependence

Cross-validation fold scores are not independent observations.

In LOSO:

Fold 1:
train Subjects 2–109

Fold 2:
train Subjects 1,3–109

These training datasets overlap heavily.

Therefore standard errors computed simply from variation across CV
folds can substantially underestimate uncertainty. [1,2]

Outer subject scores are useful for studying variability across
held-out subjects, but they are not completely
independent model-training experiments.

#### What corrections should we use?

Holm correction across the difference comparisons of: 

Week 5 vs Week 6 
Week 6 vs Week 7

Benjamini-Hochberg FDR when we test significance for all 109 subjects. 


### 27) Interpretation of subject-level bootstrap intervals

Bootstrapping the 109 already-computed outer test scores measures variability across held-out subjects.

It does not fully capture uncertainty caused by drawing a new training
population and retraining the algorithm.

A complete bootstrap of the learning procedure would require resampling of subjects, retraining of CSP/LDA and retesting.

Therefore Week 8 should only focus on whether the BA changes as the subjects get replaced. Creating so-called subject-level
bootstrap confidence intervals for cohort performance.

### 28) Robust descriptive statistics

Because EEG decoding performance varies strongly across subjects,
cohort results should include more than the mean.

Useful descriptive statistics include:

- mean
- median
- interquartile range (the range between 25th and 75th percentile)
- minimum and maximum
- bootstrap confidence interval

The median and IQR are less sensitive to extreme subject scores than
the mean.


### 29) Robustness and sensitivity analysis

Robustness analysis asks whether the main conclusion persists under
reasonable alternative analyses.

Relevant NeuroSignalLab analysis include:

- Do predefined irregular recordings materially change the result?
- Are conclusions driven by a small number of subjects?
- Do mean and median results tell a consistent story?
- Do known sampling or annotation irregularities distort the comparison?

Subjects should not be excluded simply because their classification
performance is poor or unusual.

Exclusion should be based on predefined technical or data-quality
criteria.


### 30) Sensitivity analyses

A sensitivity analysis can compare:

a primary analysis with all subjects

against

a secondary analysis that
exclude only subjects meeting predefined technical irregularity
criteria

If the conclusion remains similar, the result is more robust.

Any exclusions and the reason for them must be reported explicitly.


### 31) Planned Week 8 analyses

The Week 8 statistical notebook should focus on three main questions.

#### A) Performance uncertainty

For Weeks 5, 6, and 7:

- mean balanced accuracy
- median
- IQR
- subject-level bootstrap 95% CI

#### B) Cost of cross-subject generalization

Compare Week 5 vs Week 6 using paired subject results.

Report:

- mean paired difference
- median paired difference
- paired bootstrap CI
- paired permutation p-value

#### C) Effect of nested tuning

Compare Week 6 vs Week 7.

Report:

- mean paired difference
- median paired difference
- paired bootstrap CI
- paired permutation p-value

If both comparisons are treated as one inferential family, apply Holm
correction to the two p-values.


#### D) Chance-level analysis

Chance-level inference should be considered separately from
model-comparison inference.

Chance-level testing asks:

Is there evidence that the EEG contains information about the class
labels beyond what would be expected under no EEG-label relationship?

A classifier-level label-permutation test is the stronger direct test
of this question. THis could be done for the Week 6 pipeline, but not the large Week 7 nested analysis. 


### 32) Interpretation principles

Week 8 should report:

effect magnitude
+
uncertainty
+
statistical evidence

A p-value should never replace effect size.

A confidence interval should never be interpreted as proof.

A statistically significant one-percentage-point improvement may still
be practically small.

A numerically above-chance score is not automatically statistically
above chance.

The goal is not to obtain p < 0.05.

The goal is to determine how strongly the existing results are
supported and how uncertain they remain.


## References

[1] Varoquaux G, Raamana PR, Engemann DA, Hoyos-Idrobo A,
Schwartz Y, Thirion B.
Assessing and tuning brain decoders: Cross-validation, caveats, and
guidelines.
NeuroImage. 2017;145(Pt B):166–179.
doi:10.1016/j.neuroimage.2016.10.038.

[2] Varoquaux G.
Cross-validation failure: Small sample sizes lead to large error bars.
NeuroImage. 2018;180(Pt A):68–77.
doi:10.1016/j.neuroimage.2017.06.061.

[3] SciPy developers.
scipy.stats.bootstrap documentation.
SciPy Reference Guide.

[4] SciPy developers.
scipy.stats.permutation_test documentation.
Section on paired permutation tests (`permutation_type="samples"`).
SciPy Reference Guide.

[5] SciPy developers.
scipy.stats.wilcoxon documentation.
SciPy Reference Guide.

[6] Combrisson E, Jerbi K.
Exceeding chance level by chance: The caveat of theoretical chance
levels in brain signal classification and statistical assessment of
decoding accuracy.
Journal of Neuroscience Methods. 2015;250:126–136.
doi:10.1016/j.jneumeth.2015.01.010.

[7] Ojala M, Garriga GC.
Permutation Tests for Studying Classifier Performance.
Journal of Machine Learning Research.
2010;11:1833–1863.

[8] scikit-learn developers.
permutation_test_score documentation.
scikit-learn.

[9] Holm S.
A Simple Sequentially Rejective Multiple Test Procedure.
Scandinavian Journal of Statistics.
1979;6(2):65–70.

[10] Benjamini Y, Hochberg Y.
Controlling the False Discovery Rate: A Practical and Powerful
Approach to Multiple Testing.
Journal of the Royal Statistical Society: Series B.
1995;57(1):289–300.
doi:10.1111/j.2517-6161.1995.tb02031.x.
