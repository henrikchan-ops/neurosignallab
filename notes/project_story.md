
# NeuroSignalLab Project Story/Timeline

## What I started this project

## My background

## What I want to UNderstand

## Initial Research Question

## Major Project decisions

For the main project, I will focus on motor-imagery EEG rather than clinical seizure detection. Motor imagery is a better starting point because it connects naturally to brain-computer interfaces and allows me to build a full EEG decoding program without making diagnostic claims. 

The optional seizure extension will only be added if the main project is stable. If included, it will be framed as exploratory clinical analysis, not as a diagnostic model.

I will not upload full raw EEG datasets to the repository. Instead, I will provide code, instructions, metadata files, small sample data if appropriate, and refer to the original dataset sources.

I will use classical machine-learning baselines before deep learning because I want to show whether simpler interpretable methods already capture useful signal.


## Disclaimer

This project is not a medical device, diagnostic system, or clinical decision-support tool. The models should not be used to diagnose, monitor, treat, or predict neurological disease.

If the model performs well, that does not mean it generalizes to new subjects or real clinical settings. Subject-wise and session-wise testing are important because EEG models can appear artificially strong when data from the same subject or recording session leaks into both training and testing sessions.

Interpretability methods such as saliency maps or occlusion sensitivity CAN show what influenced a model prediction, but they do not prove true neurophysiological causation.


## Weekly Reflections

### Week 1 - Project setup
This week I created the initial repository for the project, as well as drafted the README and updated the Project Story. The project should make a tool that is consistent and reproducible, and seriously tackle the challenges related to training models. It should end up being a quality product, not just used for learning. 

THe most important insight was how to divide the project into different phases and realize which outputs need to be delivered. What was mostly taken for granted in my labs, such as csvs with metadata, separation into epochs, must be clearly stated in the README as essential steps in this process. The README should be precise, and it took time to figure out the correct structure to make it sensible. I understand the importance of making the model I train reproducible for others. 

The next step is to provide a notebook with the fundamental knowledge required to understand EEG and neural signal processing. Then, we can load and refine the raw EEG data. 



### Week 2

**What did I build this week?**

**What did I learn technically?**

**What confused me?**

**What decision did I make?**

**What limitation did I notice?**

**How does this connect to my larger goal?**

**What is the next step?**

### Week 3

## Connection to application to the US
THis project clarifies my interest in studying at intersections of medicine, informatics, neuroscience and human-centered AI. I am trying to build technical skills that can work with biological data, which furthers my medical understanding. 

Cornell, specifically is relevant because it can provide an environment where i can combine computing, neuroscience, data science and heath-related applications in an intentional and serious way. 

## One-sentence TLDR
I built NeuroSignalLab to understand the process from raw EEG signals to machine-learning predictions, while learning the challenges you face while developing responsible neurotechnology.
