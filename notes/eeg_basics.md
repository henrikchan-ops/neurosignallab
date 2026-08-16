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

## Artefacts and Data cleaning

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

