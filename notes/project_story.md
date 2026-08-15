
# NeuroSignalLab Project Story/Timeline

## Why I started this project

I start NeuroSignalLab because my interests in medicine, informatics and neurophysiology are starting to converge into a single question: How can biological signals be interpreted and translated into useful automated efficient systems?

In medicine, I am learning how the nervous system works as a result of their electrical signals. Through my research experience in a neurophysiology lab, I am understanding how these electrical signals can be turned into data and interpreted. And in informatics, I am learning how this data can be transformed into an automated efficient tool. 

This project seeks to bridge my three interests into a concrete project that can showcase how electrical signals turned into data can show how actions are formed through software. 

## My background
I´m Henrik, a 20 year old medical and informatics student at UiO. 

I was put into a competitive environment at a very early age, competing in international piano competitions from the age of 10. In my formative years, and due to isolation in covid, I developed an interest in performance psychology. Through recognizing my own cognitive patterns, I got more and more intrigued in how the human brain functioned biologically and psychologically.  

In highschool, seeking to understand how humans behaved around motivation, desires and wants, I started contacting psychiatrists and healthcare professionals in Oslo and abroad, all while understanding how my own mind developed under pressure throughout competition. Applying these concepts and talking to professionals made me realize how many subgroups in our society are starved of meaningful connections and moments in their lives. This led my to start my own company, Golden Conversations. 

After developing for a few months, my company and a few recruited employees deployed in various elderly homes throughout Oslo during my final year of highschool. During that period, we held concerts, speed friendings, had many deep and meaningful conversations with elderly and other various events. THe elderly were varied, many could hear or see properly, some suffered from memory loss and others struggled to move properly. It truly made me realize that problems in healthcare were much larger and more systematic than my own personal struggles. 

I knew I needed more knowledge, and so i started studying medicine. Shortly into my studies i joined a lab to further pursue my understanding in neurological illnesses such as Alzheimers and Epilepsy. Inside the lab i saw that meaningful discovery was often found behind mountains of data and gathering of evidence. You dont only need to measure it, like we do during medschool, but also process, model, interpret and translate them. I felt the need to learn more tools in order to interpret these signals better. 

So, programming and my interest in ML, which only were side interests used to create websites and journaling agents, became something i needed to understand deeper. To better this understanding, I not only started studying informatics in my 2nd semester, but also wanted to finish a big project that connected my interests together. This is why I am building NeuroSignalLab. 

## What I want to Understand
I want to understand the full path from raw EEG data to machine-learning prediction. That means not only training a model, but also learning how models are evaluated, and why interpretation must be handled carefully. Using my knowledge from a neurophysiology lab, I want to understand how this process can be automated and made more efficient. 

I also want to understand why EEG machine learning is difficult. EEG signals are noisy, subject-specific, artifact-sensitive, and easy to evaluate incorrectly if data leakage occurs.

## Initial Research Question

How reliably can classical machine-learning and EEG deep-learning models decode motor-imagery states from open EEG records?

What do preprocessing, evaluation design, and interpretability reveal about the limits of applying EEG machine-learning to neurotechnology or clinical contexts?

This project uses open EEG datasets to build a reproducible process for loading, preprocessing, visualizing, classifying, and interpreting brain-signal data. The goal is not only to compare model performance, but also to understand the practical challenges of EEG-based machine learning, including subject variability, data leakage, model interpretability, and clinical limitations.

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
