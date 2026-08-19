# EEG Basics
Based on Mike X Cohen´s NEW ANTS series

## Intro - EEG is source separation

Neuroscience is source separation

Basically we have true sources we cannot measure, so instead we use sensors to measure it
Problem: The sensors contain multiple true sources -> creates noise
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

## What is EEG and how to interpret it

### Origins of EEG and EEG data
Communication through electrochemical signaling
Ions go into and out of neuron and creates a spatial asymmetry -> creates electrical field
With EEG -> A larger electrode on the scalp -> cannot measure single neuron electrical field
Many neurons activate simultaneously -> collective electrical field transmit all the way to the scalp -> that gets measured

### Origins of content of EEG signals
We want to know what the signals mean -> information can be manifested as a signal
Cognition comes from interacting between neurons -> EEG is what can you say about brain computation from signals
This is hard to analyze -> we dont know what the origin of the contents are

### Advantages of EEG
Direct measure of electrical brain activity
Temporal resolution and precision match speed of cognition
They are complex and rich -> many analyses can be made
Findings can be linked across scales, methods and species -> can measure meaningful activity at every scale

### Disadvantages of EEG
Limited to synchronous large scale potentials -> cannot measure individual neurons
Two opposing electrical fields will cancel each other out -> no signal measured
Uncertainties in anatomical localization -> where in the brain does the signal come from -> However might not need to have physical evidence
Data is complex -> lots of noise, complicated, time-consuming and annoying
Sometimes too high temporal precision and resolution -> problem for slower processes 

## Understanding how to spot artefacts and do data cleaning

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

## Understanding the pathway from raw data to deep-learning model

### What is raw data, and how do we use it?

A raw object represents continuous EEG data recording as well as important metadata. 

From the Raw data we extract from the dataset, we wish to gain the info related inside them and convert them into epochs. The info attribute to the raw-data includes sampling frequency, channels, channel names, etc. 

We then wish to find the events inside of the data. Which we then enter into an event_id dictionary. 

Using the raw object and events array, we convert it into epochs with mne-Epochs. Here we use the raw-data, list of events, the event dictionary and mark the alloted time-slot. You can also reject events using certain criteria. 

The workflow becomes: 
Load continuous data -> inspect metadata -> event extraction -> convert into epochs


### What are annotations?

An annotation contains stored event inside of a recording file. Using the annotation, we can extract events and put it into the event-dictionary. The resulting dictionary can then be used to create Epochs from the Raw-data. 

You can more easily think about it like this: 
Annotations = Readable table that displays electrical activity for all channels of the EEG attached to timepoints

The differences in electrical activity signal different events, like rest or task-related events. To be able to convert annotations into an array, the events within the experiment should be mapped out.

Events = The eletrical signals converted into a numerical array 
Epoch = A cut-out EEG window around an event

### Understanding PhysioNet´s EEG Motor Movement/Imagaery dataset

What is motor imagery?
Imagined movement without performing it

We wish to use the data from the BCI to decode whether or not there was imagined movement from the EEG. 

Format: EDF+
Channels: 64 EEG channels
Sampling rate: 160 Hz
Tasks: Real and imagined motor movement

Labels: 
T0 -> rest
T1 -> left-fist or both-fists movement/imagery
T2 -> right fist or both feet movement/imagery

There were 14 total runs for each subject, outlined more clearly in a older version of the dataset. Runs 4, 8 and 12 have T1 as imagined left fist and T2 as imagined right fist. Since labels T1 and T2 change, we start first with runs 4,8 and 12 to isolate the motor-imagery tasks. 

Then as we map out other runs, labels need to be recorded and changed. 

### MOABB, What to understand moving onto ML-development

EEG-data is noisy, subject specific and sensitive to artefacts, making it difficult to concisely generalize and train. The model can usually appear very strong if the train/test split of data is too easy. The same applies if similar epochs/subjects/recording sessions are in both train and test datasets. 

It is therefore important to have and compare different evaluation strategies: 

WIthin-session evaluation - can the model classify new trials from same recording-context
Cross-session evaluation - can the model classify data from another session of the same subject
Cross-subject evaluation - can the model classify data from a new person?


### Understanding EEGNet, convolutional neural networks for EEG-based BCIs

EEGNet learns useful EEG features, but requires correct preprocessing, labelling and evaluation design. Its a reasonable comparison model, but it requires classic baslines and a simple CCN first. 
