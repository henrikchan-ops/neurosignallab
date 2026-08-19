# EEG Basics

Sources: 

Mike C Cohen´s NEW ANTS series

EEG Motor Movement/Imgaery Dataset v1.0.0

MNE Over of Python

MNE Annotations and events

## 1. What is EEG?

Electroencephalography or EEG is a method for recording brain activity from electrodes placed on the scalp. That means that EEG cannot measure individual neurons. Instead, it records large-scale synchronous potential/electrical activity. 

The data from the EEG is sampled from multiple electrodes repeatedly over time. This creates a time-frequency table for all electrode channels. This table can later be filter and used to represent events and brain activity. 

### Origins of EEG and EEG data
Communication through electrochemical signaling
Ions go into and out of neuron and creates a spatial asymmetry -> creates electrical field
With EEG -> A larger electrode on the scalp -> cannot measure single neuron electrical field
Many neurons activate simultaneously -> collective electrical field transmit all the way to the scalp -> that gets measured

We want to know what the signals mean -> information can be manifested as a signal
Cognition comes from interacting between neurons -> EEG is what can you say about brain computation from signals
This is hard to analyze -> we dont know what the origin of the contents are

## 2. Why EEG Is Difficult to Interpret

### Disadvantages of EEG
Limited to synchronous large scale potentials -> cannot measure individual neurons
Two opposing electrical fields will cancel each other out -> no signal measured
Uncertainties in anatomical localization -> where in the brain does the signal come from -> However might not need to have physical evidence
Data is complex -> lots of noise, complicated, time-consuming and annoying
Sometimes too high temporal precision and resolution -> problem for slower processes 

Basically brain waves are true sources we cannot measure, so instead we use sensors to measure it
The problem is the sensors contain multiple true sources -> creates noise
We want to weight a combination which can give an estimate of the source we want ot measure (without the noise) -> more similar to true source
This is called “source” components

How can sources be separated?
Anatomically -> studying specific regions
Cognitively -> studying specific cognitive processes (for instance only long-term memory)
Statistically -> This is what will be used in this project

Source separation via filtering
Temporal/spectral filtering -> take measured data and combine it so that it gets weighted by a function -> This is what is done in this project
Spatial filtering -> Each channel is affected by the weight at each time point

Assumptions for spectral separation
Usually you have a noise and signal source
You cannot use perfect source separation -> signal and noise will be mixed in a spectrum -> impossible to separate with spectral separation

## 3. Channels and Electrodes
## 4. Sampling Frequency
## 5. EDF Files
## 6. MNE Raw Objects

A raw object represents continuous EEG data recording as well as important metadata. In this project they are stored in EDF files. 
This means that everything is stored into one file -> events, labels, metadata, sampling frequency -> all in one file. 

From the Raw data we extract from the dataset, we wish to gain the info related inside them and convert them into epochs. The info attribute to the raw-data includes sampling frequency, channels, channel names, etc. Epochs are discontinuous cut-out data segments that include events that we want to further inspect.

We then wish to find the events inside of the raw-data. Which we then enter into an event_id dictionary. Now that we have all the necessary info, and the events extracted, we can convert the raw object and events array to epochs. 

Here we use the raw-data, list of events, the event dictionary, and mark the alloted time-slot. You can also reject events using certain criteria. 

The workflow becomes: 
Load continuous data -> inspect metadata -> event extraction -> convert into epochs


## 7. Events, Annotations, Onset, and Duration

Annotations are time labels attached to events in the raw-data. Using the annotation, we can extract events and put it into the event-dictionary. The resulting dictionary can then be used to create Epochs from the Raw-data. 

An annotation is divided into: 
Onset -> time until event starts
Description -> what happened during event
Duration -> how long the event lasts

The differences in electrical activity, signal different events, like rest or task-related events. To be able to convert annotations into an array, the events within the experiment should be mapped out.

Events = The eletrical signals converted into a numerical array 
Epoch = A cut-out EEG window around an event

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

There were 14 total runs for each subject, outlined more clearly in a older version of the dataset. Runs 4, 8 and 12 have T1 as imagined left fist and T2 as imagined right fist. Since labels T1 and T2 change, we start first with runs 4,8 and 12 to isolate the motor-imagery tasks. 

Then as we map out other runs, labels need to be recorded and changed. 

## 10. Mu/Alpha and Beta Rhythms

Because event-related desynchronization during movement and imagery typically is observed around alpha/mu (8-13 Hz) and beta (15-25) Hz, we can filter the EEG signal inside this bandwidth after preprocessing. 

## 11. Preprocessing

Preprocessing: 
Time-consuming
Tedious
If you do it well, you only do it once

Processing: 
Hypothesis and exploratory
Needs to be done multiple times

Preprocessing steps (depending on data, study and lab)
Import data into Python
Apply high-pass filter -> to remove artefacts and noise
Import channel locations -> for topographical mapping
Epoch data around important events -> put focus on interesting data -> Makes data 3d -> time channels and epoch/trials
Subtract pre-stimulus baseline -> similar to effects of high-pass filter
Adjust marker values 
Manual trials rejection -> removes artefacts and noise -> can be done differently (in accordance to type 1 and 2 mistakes)
Mark bad electrodes -> noisy electrodes
Average reference EEG channels -> or at least rereference EEG channels in a way -> avoid electrodes on one side of the head -> the reference electrode should be as clean as possible
Run ICA to clean data -> find what you want to remove from dataset

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

EEG-data is noisy, subject specific and sensitive to artefacts, making it difficult to concisely generalize and train. The model can usually appear very strong if the train/test split of data is too easy. The same applies if similar epochs/subjects/recording sessions are in both train and test datasets. 

It is therefore important to have and compare different evaluation strategies: 

Within-session evaluation - can the model classify new trials from same recording-context
Cross-session evaluation - can the model classify data from another session of the same subject
Cross-subject evaluation - can the model classify data from a new person?

This way we subject the model to generalization -> if the model works on data it has never seen before

## 14. Why EEG Machine Learning Is Difficult

EEGNet learns useful EEG features, but requires correct preprocessing, labelling and evaluation design. Its a reasonable comparison model, but it requires classic baslines and a simple CCN first. 

## 15. What I Need to Check Before Modeling
## 16. Sources


### Advantages of EEG
Direct measure of electrical brain activity
Temporal resolution and precision match speed of cognition
They are complex and rich -> many analyses can be made
Findings can be linked across scales, methods and species -> can measure meaningful activity at every scale



