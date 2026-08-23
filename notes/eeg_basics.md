# EEG Basics

Sources: 

Mike C Cohen´s NEW ANTS series

EEG Motor Movement/Imgaery Dataset v1.0.0

MNE Over of Python

MNE Annotations and events

## 1. What is EEG?

Electroencephalography or EEG is a method for recording brain activity from electrodes placed on the scalp. That means that EEG measures larger brain areas, not individual neurons. The data from the EEG is sampled from multiple electrodes repeatedly over time. This creates an overview of how channels act over time for all electrode channels. This can later be filtered and used to represent events and brain activity. 

### Origins of EEG and EEG data
EEG data is communication through electrochemical signaling. Ions go into and out of neuron and creates a spatial asymmetry, which create electrical fields. 
With EEG, a larger electrode on the scalp, youcannot measure single neuron electrical field
Many neurons activate simultaneously and create a collective electrical field that transmit all the way to the scalp. This si what gets measured.[^cohen-notes] 

## 2. Why EEG Is Difficult to Interpret

EEG is difficult because it is a sensor that measures brainwaves, a true source we cannot measure. The EEG signals contain multiple true sources, as brainwaves from multiple regions can be picked up by one electrode. This creates noise.[^cohen-notes] 

Because it studies larger areas, two opposing electrical fields can cancel eachother out. We can also not precisely pinpoint the anatomical localization and exactly where the signal is coming from. 

EEG data contains a lot of noise, its complicated and can be time-consuming. 

A way of bypassing this is by filtering the data. We can separate it using different frequencies and combine the weighted data that gets weighted by a function. 

## 3. Channels and Electrodes
## 4. Sampling Frequency

Sampling frewuency means how many measurements are taken per second. If EEG sampled 160 Hz, the channel is measured 160 times per second.

The PhsyioNet motor-imagery dataset has a sampling frequency of 160 Hz.[^physionet-eegmmidb] A 4-second Epoch would contain: 

160 samples/second * 4 seconds = 640 time samples

The sampling frequency determines the number of time points in each epoch and the shape of the input to the ML-model. 

## 5. EDF Files
## 6. MNE Raw Objects

A raw object represents continuous EEG data recording as well as important metadata.[^mne-overview] In this project they are stored in EDF files. 
This means that everything is stored into one file -> events, labels, metadata, sampling frequency -> all in one file. 

From the Raw data we extract from the dataset, we wish to gain the info related inside them and convert them into epochs. The info attribute to the raw-data includes sampling frequency, channels, channel names, etc. Epochs are discontinuous cut-out data segments that include events that we want to further inspect.[^mne-events]

We then wish to find the events inside of the raw-data. Which we then enter into an event_id dictionary. Now that we have all the necessary info, and the events extracted, we can convert the raw object and events array to epochs. 

Here we use the raw-data, list of events, the event dictionary, and mark the alloted time-slot. You can also reject events using certain criteria. 

The workflow becomes: 
Load continuous data -> inspect metadata -> event extraction -> convert into epochs


## 7. Events, Annotations, Onset, and Duration

Annotations are time labels attached to events in the raw-data. Using the annotation, we can extract the numerical timing markers called Events. Events are numerical timing markers used to represent when experimental conditions occur. They tell the analysis code where in the continuous EEG recording a condition starts. The resulting Event-dictionary can then be used to create Epochs from the Raw-data.[^mne-annotations] 

An annotation is divided into: 
Onset -> time until event starts
Description -> what happened during event
Duration -> how long the event lasts

## 8. Epochs
## 9. Motor Imagery

What is motor imagery?
Imagined movement without performing it

We wish to use the data from the BCI to decode whether or not there was imagined movement from the EEG. 

Format: EDF+
Channels: 64 EEG channels
Sampling rate: 160 Hz (samples per second)
Tasks: Real and imagined motor movement

Labels: 
T0 -> rest
T1 -> left-fist or both-fists movement/imagery
T2 -> right fist or both feet movement/imagery

There were 14 total runs for each subject, outlined more clearly in a older version of the dataset. Runs 4, 8 and 12 have T1 as imagined left fist and T2 as imagined right fist. Since labels T1 and T2 change, we start first with runs 4,8 and 12 to isolate the motor-imagery tasks.[^physionet-eegmmidb] 

Then as we map out other runs, labels need to be recorded and changed. 

## 10. Mu/Alpha and Beta Rhythms

Because event-related desynchronization during movement and imagery typically is observed around alpha/mu (8-13 Hz) and beta (15-25) Hz, we can filter the EEG signal inside this bandwidth after preprocessing.[^erd] 

## 11. Preprocessing

Preprocessing: 
Time-consuming
Tedious
If you do it well, you only do it once

Processing: 
Hypothesis and exploratory
Needs to be done multiple times

Preprocessing steps vary by dataset, study type, and lab, but commonly include importing data, filtering, importing channel locations, epoching, marker adjustment, trial rejection, bad-electrode marking, rereferencing, and ICA.[^cohen-notes]

We will come back to this later. 

## 12. Artifacts and Cleaning

Data cleaning varies between experiments, labs and data

VIsual based artefact rejection first

Can you separate artefacts or do you have to remove them?

Keep in mind, eye movements can cause deflections -> they are artefacts

Are procedures that can separate those with independent component analysis (ICA)
You can have overlapping data in epoch series -> ask if you need to remove that trial

How long does it last? Is it synchronized? However, you dont have to throw out data because of brief and spatially localized data

Usually edge-artefacts can occur -> If you apply time-frequency analysis you can remove -> make a buffer zone that you would remove regardless

If artefacts occurs in areas you want to analyze data -> might need to remove the trial

Also keep in mind, which electrodes will you be doing data analysis. 

Electrical artefacts can occur: 
often you can remove the whole electrode and calculate mathematically based on neighbouring electrodes ->
 But if it has real activity you need to reconsider 
You can interpolate the channel for the artefact trials or run ICA -> 
Artefacts can often be mixed in with signals here
Obviously during collection keep an eye on the electrode and fix it mid analysis

## 13. Train/Test Splits and Generalization

A split means dividing data into different parts for model development and evaluation. 
A training set is data the model learns from. 
A test set is held back and used to evaluate how well the model performs. 

EEG-data is noisy, subject specific and sensitive to artefacts, making it difficult to concisely generalize and train. The model can usually appear very strong if the train/test split of data is too easy. The same applies if similar epochs/subjects/recording sessions are in both train and test datasets. 

It is therefore important to have and compare different evaluation strategies: 

Within-session evaluation - can the model classify new trials from same recording-context
Cross-session evaluation - can the model classify data from another session of the same subject
Cross-subject evaluation - can the model classify data from a new person?

This way we subject the model to generalization: if the model works on data it has never seen before. 
A mistake would be reporting one accuracy number without explaining what kind of generalization the split actually tested.

## 14. Why EEG Machine Learning Is Difficult

EEGNet is a compact convolutional neural network designed for EEG-based BCI tasks.[^eegnet] It is relevant to NeuroSignalLab because it can serve as a later deep-learning comparison model.

However, EEGNet should not be the first model one implements. A simple CNN and classical baselines should be built first. EEGNet results will only be meaningful if preprocessing, labeling, and evaluation are handled correctly.

We will come back to this later. 

## 15. What I Need to Check Before Modeling
## 16. Sources

## 16. Sources

[^cohen-notes]: Cohen, Mike X. *NEW ANTs / Neural Signal Processing and Analysis* course notes. Personal study notes/PDF. Used for EEG interpretation, source separation, preprocessing, artifacts, Fourier/time-frequency concepts.

[^mne-overview]: MNE-Python. *Overview of MEG/EEG analysis with MNE-Python*. https://mne.tools/stable/auto_tutorials/intro/10_overview.html. Accessed 2026-08-23.

[^mne-events]: MNE-Python. *Parsing events from raw data*. https://mne.tools/stable/auto_tutorials/intro/20_events_from_raw.html. Accessed 2026-08-23.

[^mne-annotations]: MNE-Python. *mne.Annotations*. https://mne.tools/stable/generated/mne.Annotations.html. Accessed 2026-08-23.

[^physionet-eegmmidb]: PhysioNet. *EEG Motor Movement/Imagery Dataset v1.0.0*. https://physionet.org/content/eegmmidb/1.0.0/. Accessed 2026-08-23.

[^moabb]: MOABB. *Mother of All BCI Benchmarks Documentation*. https://moabb.neurotechx.com/docs/. Accessed 2026-08-23.

[^eegnet]: Lawhern, V. J., Solon, A. J., Waytowich, N. R., Gordon, S. M., Hung, C. P., & Lance, B. J. *EEGNet: a compact convolutional neural network for EEG-based brain-computer interfaces*. Journal of Neural Engineering, 2018. https://pubmed.ncbi.nlm.nih.gov/29932424/.

[^erd]: Neuper/Pfurtscheller-related ERD literature summarized in motor-imagery EEG studies; for example, sensorimotor ERD is commonly discussed in alpha/mu and beta frequency bands during movement and imagery. See: https://pmc.ncbi.nlm.nih.gov/articles/PMC6795263/. Accessed 2026-08-23.





