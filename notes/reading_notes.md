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

Q1

left vs right is better

Gives clear binary question -> Spatially more different sensorimotor EEG patterns

Its easier to preserve, subject id, run id and trial id

Runs 4, 8 and 12 gives us most data without making it too complicated -> make the research question harder to reach

S: Optimal spatial filtering

Q2
We want to not make T0 a classification

Only T1 and T2: 

Because this way the model would easily be able to distinguish between task and no task, but perhaps not left vs right imagery

THen it must explore more subtle differences
Classic BCI work you treat it as a two class problem

S: Optimal spatial filtering

Q3
Motor imagery typically works around mu 8-13 and beta 13-30

Older work suggests that its invovled in mu and beta rhythms in ERD/ERS

MNEs deconing pipeline uses 7-30, so we can use that. 

It isnt optimal, but we can later filter into smaller sub-bands, but use a baseline of 7-30 Hz

Be careful with filtering

S: Motor imagery and exectuoin

Mu and beta topo

ERD, event related dynamics

MNE CSP

Optimal spatial filtering

Q4 

MNEs own ERD usees -1 to +4

This is important so you can get context around the trial. 

The EEGBCI example says it delays classification window by 1 second after ue onset to avoid classifying evoked responses -> We dont want to learn visual cues -> But the motor imagery

So this way we have the sustained motor imagery, but avoid the initial cue response. 

WE should store -1 to r, but use 1-4 for ML. 

Q5
Keep all channels 

SPatial methods like CSP are designed to learn combinations of multiple channels

We can later determine a predetermined subset of electrodes. 

We dont want testdata information to influence feature selection

Q6 EEG reference

EEG is always relative to a refernce

We use MNEs average referencing -> constructing a virtual refernce from the mean signal across all channels

Q7 Baseline correction
We are not trying to classify ERP amplitude -> but the oscillatory structures and later spatial/spectral features

We can therefore use none. 

For ERD visualizations we can use The precue period can be used as a baseline. -> But NOT for ML epochs

We want to select preprocessing protocl before looking at performance. 

### Notes for articles

#### 1) Physionet, what experiment produced the data

Subjects labeled 1-109
64 electrodes at 160 Hz
10-10 arrangement in an EDF+

Performed 14 runs, with 1-2 as resting baselines: 

Unilateral imagined

Unilateral execution

Bilateral imagined

Bilateral execution

We want to ask: 
Can EEG distinguish imagined left-fist movement from imagined right-fist movement

Keep in mind only three runs per patient

#### 2) Shuqfa, Lakas & Belkacem (2024)

Is the original PhysioNet dataset perfectly uniform?

There are multiple missing trials, trials with length zero and issues. 

We can skip 6 problematic subjects: 

S088
S089
S092
S100
S104
S106

Typical runs include: 
15 T0
7-8 T1 and T2 trials
Events around 4.1 +- 0.2
Runs around 123,5

We should program checks into the code. No all data is valid

#### 3) Pfurtscheller & Lopes da Silva ERD and ERS

What biological signal are we trying to detect

Event related desynchronization ERD - When neuronal population gets engagaed, oscillations can become less synchronized -> EEG power in band decreases

Event-related synchronizations ERS - 

ERD and ERS -> CHanges in ongoing oscillatory power -> not identical phase trial to trial

ERP -> Phase locked -> electrical deflection occurs at same latency eveyr cue -> you can average the trials

Motor-imgaery analysis cares about frequency, power, time and spatial location


For instance: 

Resting mu power = 10
Imgaery mu power = 6

6-10/10 * 100 = -40%

THat means theres a 40% power reduction -> ERD

Basically this is the process: 

EEG -> separate frequencies -> estimate power -> compare task power with pre-task power -> calculate relative change

#### McFarland et al. Why mu, beta and central electrodes?

Which frequencies and scalp areas are relevant for hand motor imagery

in experiment: 
mu = 8-12
beta = 18-25

Both actual and imagined movement produced desynchronization: 

Mu = Lateral postcentral foci
Beta = more diffuse and more strongly near the vertex

The differences between movement/rest and imagery/rest were cocentrated around 8-28 Hz

#### Ramoser et al. Common Spatial Patterns

WHy keeping multiple channels can help with classification

CSP -> Which weighted combination of electrodes produces the largest distinction between the two classes?

Learned spatial filters can discriminate

The weighting is learned from data

CSP wants to maximize variance for one class and minimize for the other. 

Because band-limited oscillatory EEG, variance is closely related to signal power

CSP uses class labels to learn its filters

Basically we have to do this: 

Training data -> fit CSP

Test data -> apply already fitted CSP

If we fit CSP to the whole dataset, its wrong -> we need to preserve all necessary channel info for the future. 

#### Motor imgaery decoding using CSP
The best example that connects to our project

We can take inspiration from their code

So the experiment is structured so that the participant sees something visually before the movement gets imagined: 

At t=0 the participant sees something. If left and right cues differ -> We learn left and right visual stimulus 

And we dont learn left-hand vs right-hand imagery

#### WIdmann, Schrøger and Maess. FIltering is not harmless

CUt off requency, transition bandwidth and phase can affect signals

What we choose to preserve is important

For instance, in MNE doesnot instantly disappear at 7-30 Hz

We can use MNEs skip_by_annotation = "edge" to for instance avoid the end of Run 4 being concatenated with start of run 8

We dont want to filter acroos discontinuities. And we perhaps want to filter between trials too. 

#### MNE Epochs

How to turn EEG into trials

COntinuous recording -> find T1/T2 onset -> Cut fixed time window -> one epoch per motor imagery trial


EEG does not measure absolute voltage

But compares the electrode - the reference -> Every EEG is dependant on the refernce

The CSP example usees projection = True for its refernce


WHat is baseline correction?

Epoch baseline subtracts the mean voltage

ERD/ERS compares oscillatory power

We will have baseline corerction set to None at first. 

Epochs can have large artifacs or flat channels: 

MNE can calculate Peak to peak amplitude -> meaning epochs get rejected if it exceeds a threshold

We need to find the appropriate threshgold depdning on data


#### Summary from the 8 articles

What do the files and labels mean? 

RUns 4,8 and 12 -> T1 left imgaery T2 right imagery

Can every recording be trusted?

No -> Run lengths and trial counts

What EEG phenomenon reflects motor engagement?

Frequency specific ERD/ERS

Where and at what frequencies?

Central sensorimotor regions -> mu and beta rhythms

How can electrodes become useful features

CSP learns spatial combinatons of electrodes

HOw do we isolate relevant frequencies safely?

CAreful 7-30 Hz band-pass filtering

How do we implement all this?

Load -> Combine recordings -> standarize -> montage -> refernce -> filter -> event -> epochs -> insepct epoch quality -> QC


### Week 4 Preprocessing Protocol

#### Research task
Binary classification of imagined left- versus right-fist movement.

#### Dataset
PhysioNet EEG Motor Movement/Imagery Dataset.

#### Runs
Runs 4, 8, and 12: imagined left-versus-right fist movement.

#### Classes
T1 = imagined left fist  
T2 = imagined right fist

T0 is retained in the original recording for reference and exploratory analysis but is not used as a classification target.

#### Channels
All 64 EEG channels are retained initially.

C3, Cz, and C4 remain useful for visualization and physiological sanity checks, but channel selection is not performed at the preprocessing stage.

#### EEG reference
Common average reference.

#### Frequency filtering
7–30 Hz band-pass filter.

This range covers the main sensorimotor mu and beta rhythms associated with motor imagery while matching a standard MNE EEGBCI decoding pipeline.

#### Epoch extraction
Create epochs from:

-1.0 s to +4.0 s relative to T1/T2 cue onset.

The pre-cue section is retained for quality control and possible later ERD/ERS analysis.

#### Machine-learning window
Use:

+1.0 s to +4.0 s

for the first classification experiment.

The first second after the cue is excluded to reduce the possibility of decoding cue-evoked visual responses instead of sustained motor imagery.

#### Baseline correction
No baseline subtraction is applied to the primary machine-learning input.

For later ERD/ERS visualization, the -1 to 0 s interval may be used as a reference period.

#### Sampling frequency
Retain the native 160 Hz sampling frequency.

#### Expected machine-learning trial shape

Approximately:

64 channels × 480 time samples

for each 3-second motor-imagery trial.