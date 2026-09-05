
# NeuroSignalLab Project Story/Timeline

## Why I started this project
I started NeuroSignalLab because my interests in medicine, informatics and neurophysiology are starting to converge into a single question: How can biological signals be interpreted and translated into useful computational systems?

In medicine, I am learning how the nervous system functions through electrical and chemical signals. Through my research experience in a neurophysiology lab, I am understanding how these electrical signals can be turned into data and interpreted. And in informatics, I am learning how this data can be transformed into reproducible and convenient software tools. 

This project seeks to bridge my three interests into a concrete project that can showcase how neural signals can be processed, modeled, and visualized through software. 

## My background
I´m Henrik, a 20 year old medical and informatics student at UiO. 

I was put into a competitive environment at a very early age, competing in international piano competitions from the age of 10. In my formative years, and due to isolation in covid, I developed an interest in performance psychology. Through recognizing my own cognitive patterns, I got more and more intrigued in how the human brain functioned biologically and psychologically.  

In highschool, seeking to understand how humans behaved around motivation, desires and wants, I started contacting psychiatrists and healthcare professionals in Oslo and abroad, all while understanding how my own mind developed under pressure throughout competition. Applying these concepts and talking to professionals made me realize how many subgroups in our society are starved of meaningful connections and moments in their lives. This led me to start my own company, Golden Conversations. 

After developing for a few months, my company and a few recruited employees deployed in various elderly homes throughout Oslo during my final year of highschool. During that period, we held concerts, speed friendings, had many deep and meaningful conversations with elderly and other various events. The elderly were varied, many could not hear or see properly, some suffered from memory loss and others struggled to move properly. It truly made me realize that problems in healthcare were much larger and more systematic than my own personal struggles. 

I knew I needed more knowledge, and so i started studying medicine. Shortly into my studies i joined a lab to further pursue my understanding in neurological illnesses such as Alzheimers and Epilepsy. Inside the lab i saw that meaningful discovery was often found behind mountains of data and gathering of evidence. You dont only need to measure it, like we do during medschool, but also process, model, interpret and translate them. I felt the need to learn more tools in order to interpret these signals better.

So, programming and my interest in ML, which only were side interests used to create websites and journaling agents, became something i needed to understand deeper. To better this understanding, I not only started studying informatics in my 2nd semester, but also wanted to finish a big project that connected my interests together. A model or app could always produce a number or a result. However to understand the ways of preserving the context of the biological signal, how the model was trained, its limitations and how to further develop the model, I knew I needed to amass much more knowledge, and experience first hand what it means to create a reliable tool. This is why I am building NeuroSignalLab. 


## What I want to Understand
I want to understand the full path from raw EEG data to machine-learning prediction. That means not only training a model, but also learning how models are evaluated, and why interpretation must be handled carefully. Using my knowledge from a neurophysiology lab, I want to understand how this process can be automated and made more efficient. 

I also want to understand why EEG machine learning is difficult. EEG signals are noisy, subject-specific, artifact-sensitive, and easy to evaluate incorrectly if data leakage occurs.

## Initial Research Question
How reliably can classical machine-learning and EEG deep-learning models decode motor-imagery states from open EEG records?

What do preprocessing, evaluation design, and interpretability reveal about the limits of applying EEG machine-learning to neurotechnology or clinical contexts?

This project uses open EEG datasets to build a reproducible process for loading, preprocessing, visualizing, classifying, and interpreting brain-signal data. The goal is not only to compare model performance, but also to understand the practical challenges of EEG-based machine learning, including subject variability, data leakage, model interpretability, and clinical limitations.

What does a responsible EEG machine-learning pipeline actually require?

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

It was most important to remember that saving the appropriate metadata to the correct epoch is the most crucial step in data loading. you need the correct subject, the correct channels, correct sampling and event label. This is very important for every EEG program. 

The next step is to provide a notebook with the fundamental knowledge required to understand EEG and neural signal processing. Then, we can load and refine the raw EEG data. 

## Week 2 — Technical Foundation

This week, I moved from a project idea to creating a foundation note. I set up the local Python environment, installed the core packages, created the first Jupyter notebook, and confirmed that MNE-Python runs correctly inside the project environment.

This week was about understanding that EEG is not a clean readout of thought or intention. Before any model can be meaningful, the data structure has to be understood. In my labs, the files were sorted into NWB files where the anatomical mapping, labels and events were clearly labeled. As I was working with connectivity and not motor-imagery, the channels to include were much more straightforward. 

The structure of the previous files did much of the organizational work for me. Now the data-mapping process should be a lot more rigorous and attentive.  

I also learned that the PhysioNet motor-imagery dataset contains runs, annotations, labels, and task-specific meanings that must be mapped carefully. In particular, labels such as `T1` and `T2` depend on the run type, so the first version of the project should focus on a controlled subset of motor-imagery runs before expanding. This will again differ from my previous EEG experience, as the experimental conditions were easier to distinguish from the file structure.” 

The setup notebook is intentionally simple. It does not analyze EEG yet. Its purpose is to verify that the environment can import NumPy, Pandas, Matplotlib, scikit-learn, and MNE. This creates a clean starting point for the next notebook.

The next step is to load a real EDF file from the PhysioNet dataset, inspect the `Raw` object, check metadata, inspect annotations, convert annotations into events, and begin visualizing real EEG data.


## Week 3 — First EEG Loading and Visualization

**What did I build this week?**
This week, I moved from environment setup into working with real EEG data. I loaded the first PhysioNet EEG Motor Movement/Imagery EDF file, inspected the MNE `Raw` object, checked the sampling frequency, channel count, recording length, annotations, and event labels.

**What did I learn technically?**
I learned the specific documentation style of the dataset. Before training any classifier, I had to understand how the recording is structured: what the channels are called, where the channels are positioned on the scalp, the internal structure of the raw data, how the annotations are stored, how task labels are converted into events, and whether event timing is preserved correctly.

Most of this week was understanding and figuring out how the EDF was structured internally by sourcing through the different attributes, arrays and metadata within the structure. For instance, figuring out what the data within the event array represented, and how to label it cleanly. The same adaptation was made to MNE´s data loading, specifically storing data in volts. 

I also learned how to set a standard montage for the electrodes. It provided approximate standard scalp positions, which made it easier to understand which channels to consider combined with previous litterature. 

Later, I verified that the event times matched the annotation onsets and created a compact event summary showing the number and timing range of `T0`, `T1`, and `T2`.

Finally, I created basic visualizations: a raw EEG preview from central scalp electrodes and an event timeline across the recording. These plots are visual checks showing that the signal can be loaded, inspected, visualized, and connected to task labels.

**What is the next step?**
The next technical step is to move from continuous raw EEG into epochs. This means cutting the recording into time-locked segments around `T1` and `T2` events so that each segment can become one machine-learning example.

## Week 4 — Building the Preprocessing Pipeline

**What did I build this week?**

This week I built the first complete preprocessing pipeline for the motor-imagery classification problem.

I narrowed the project qeustion to: can EEG distinguish imagined left-fist movement from imagined right-fist movement? I chose runs 4, 8, and 12 from the PhysioNet EEG Motor Movement/Imagery Dataset because they are repeated versions of the same left-versus-right motor-imagery task. T1 represents imagined left-fist movement and T2 represents imagined right-fist movement, while T0 is retained in the raw recording but is not used as a classification class. 

The final preprocessing pipeline now:

- loads runs 4, 8, and 12,
- standardizes channel names and attaches the EEG montage,
- keeps all 64 EEG channels,
- concatenates the three runs while respecting recording boundaries,
- applies a common-average EEG reference using an MNE projection,
- band-pass filters the EEG from 7–30 Hz,
- extracts T1 and T2 motor-imagery events,
- creates epochs from -1 to +4 seconds,
- retains +1 to +4 seconds as the machine-learning window,
- creates the feature array `X`, class labels `y`, and trial metadata.

The full epochs contain 64 channels × 801 samples, while the final machine-learning trials contain 64 channels × 481 samples.

After developing and inspecting the preprocessing notebook, I mimplemented it into `src/neurosignallab/preprocessing.py` as a reusable `preprocess_subject()` function. I then tested the same function across several subjects instead of keeping the preprocessing hard-coded for Subject 1.

**What did I learn technically?**
The biggest change this week was that I started understanding how each signal transformation affected the signal we tried to extract. 

Motor imagery changes ongoing sensorimotor rhythms, particularly activity in the mu and beta frequency ranges. These changes can appear as event-related desynchronization or synchronization: decreases or increases in oscillatory power that vary across frequency, time, and scalp location. This gives a physiological reason for focusing the first analysis on a broad 7–30 Hz frequency range rather than simply choosing a filter because an example used it.

I also learned more clearly why CSP is relevant to the eventual classifier. CSP instead learns weighted combinations of electrodes whose variance differs between the two classes. This is why I decided to retain all 64 EEG channels.

I learned that filtering is not simply “removing unwanted frequencies.” A digital filter introduces transition regions and possible temporal effects such as ringing. I therefore need to respect boundaries between concatenated runs rather than allowing the filter to treat the end of one recording and the beginning of another as physiologically continuous.

I also learned why a -1 to +4 second epoch sampled at 160 Hz contains 801 rather than 800 samples: MNE includes both endpoints. The same reasoning explains why the +1 to +4 second ML window contains 481 samples.

**What confused me?**
Several concepts that initially sounded similar were actually different operations.

The main one was the distinction between an **EEG reference**, a **voltage baseline correction**, and an **ERD/ERS reference period**.

A common-average EEG reference changes what each channel's voltage is measured relative to. MNE can store that transformation as a projection instead of immediately applying it. An epoch baseline correction, by contrast, subtracts a mean voltage from each epoch. ERD/ERS analysis is different: it compares oscillatory power during the task with oscillatory power during a reference time interval. These three ideas all use “reference” or “baseline,” but they solve different problems.

I was also confused about the relationship between ERP and ERD/ERS. I originally thought of both simply as responses to an event. I now understand that an ERP is a relatively time- and phase-locked voltage response, while ERD/ERS describes changes in oscillatory power that do not require the oscillation itself to have the same phase across trials.

Another question was why the classifier should begin at +1 second rather than at cue onset. The first second may contain visual cue-evoked activity, meaning a classifier could partially learn the response to seeing the cue rather than the sustained neural state associated with imagining movement. This is why I decided to retain the complete -1 to +4 second epoch for analysis, but use only +1 to +4 seconds for the first classifier. 

**What decision did I make?**
I decided on a first preprocessing protocol rather than continue changing parameters before I have a baseline model (see preprocessing_protocol.md).

These decisions are intended to form a reproducible baseline. More complicated choices such as narrower frequency bands, filter-bank CSP, channel selection, subject-specific frequency ranges, or additional artifact rejection should be included as later.

I also decided that CSP will not be fitted during preprocessing. Because CSP uses the class labels, it must later be fitted only on training data inside the machine-learning pipeline. Fitting it on the complete dataset before splitting would introduce information leakage.

**What limitation did I notice?**
The most important limitation is that preprocessing does not automatically make the EEG trustworthy.

The dataset itself contains variation between recordings and subjects. This became visible when I validated the reusable preprocessing pipeline across Subjects 1–5. The dimensions were consistent, but Subject 5 contained 21 left and 24 right trials rather than the 23/22 split seen in Subjects 1–4. Checking the original annotations showed that this difference already existed in the raw recording.

More generally, previous work on EEGMMIDB has identified subjects with non-standard recording structures. Quality control therefore needs to remain part of the analysis. 

I also do not yet have a justified artifact-rejection threshold. Peak-to-peak amplitude can be used to identify unusually large or flat epochs. For now, I inspect the data and postpone automatic artifact rejection until I have clear criterias. 

---

**How does this connect to my larger goal?**
This week created the bridge between raw EEG recordings and machine learning.

Before building classifiers, I need to know that every model receives data that have been processed consistently and that the preprocessing decisions have physiological and methodological reasons behind them. Otherwise, I would not know whether the model had learned motor imagery, visual cue responses, preprocessing artifacts, subject-specific information, or some alternative property of the dataset.

The goal is to build a reproducible brain-signal decoding pipeline and understand where its conclusions are reliable and where they are limited. Week 4 established the preprocessing foundation required for that.

Model performance is only one part of the problem. Data quality, preprocessing choices, metadata preservation, leakage prevention, and physiological interpretation determine whether performance actually means anything.

---

### **What is the next step?**

The next step is to build the first classical machine-learning baseline.

I will begin with CSP as the spatial feature-extraction method and a simple classifier such as LDA. CSP must be fitted only using the training data, so the evaluation pipeline must be designed before looking at model performance.

This first model´s purpose is to establish an interpretable baseline against which later can be compared.

The progression is therefore:

`validated preprocessing → CSP features → classical classifier → honest evaluation → stronger models`

## Week 5 — Building the First Classical EEG Decoding Baseline

**What did I build this week?**
This week I built the first complete machine-learning baseline for NeuroSignalLab.

I used Common Spatial Patterns (CSP) for supervised spatial feature extraction and Linear Discriminant Analysis (LDA) for classification. The model was evaluated using leave-one-run-out cross-validation.

For each subject, the model was trained on two of runs 4, 8, and 12 and evaluated on the remaining run. CSP and LDA were both fitted separately inside every training fold so that the held-out run could not influence feature extraction or classification.

I first tested the pipeline on Subject 1, then Subjects 1–5, then Subjects 1–20, and finally the complete 109-subject EEGMMIDB cohort.

The final experiment contained 327 evaluation folds:

`109 subjects × 3 held-out runs = 327 folds`

The fold-level and subject-level results were stored separately so that both run-level variability and overall subject performance could be examined.


**What did I learn technically?**
The main lesson this week was that building a classifier is not only about choosing an algorithm. The evaluation methodology determines what the resulting accuracy actually means.

I learned the difference between training data and held-out data, how cross-validation repeatedly creates new train/test splits, and why EEG data require special attention to grouping.

Trials were grouped by recording run. This allowed the model to be evaluated on an entire run that did not participate in training.

I also learned why CSP must remain inside the machine-learning pipeline. CSP is supervised because it uses both EEG data and class labels to learn spatial filters. If we fitted CSP before cross-validation would therefore allow information from the test data to influence the learned representation and create data leakage.

Technically, I learned the complete transformation:

`64-channel EEG`
→ `CSP spatial filters`
→ `CSP components`
→ `component average power`
→ `log-power CSP features`
→ `LDA`
→ `left/right prediction`

I also learned the distinction between components and features. A CSP component is a spatially filtered EEG time series, while a CSP feature is a numerical summary of that component, usually its log average power.

Another important connection was between EEG power and variance. Variance describes how strongly a signal fluctuates around its mean. For an approximately zero-centered band-limited signal, variance and average power are closely related. This explains why CSP can use variance differences to detect spatial differences in motor-imagery.

**What confused me?**
One difficulty was understanding what exactly CSP was producing.

Initially, it was easy to mix together electrodes, spatial filters, components, and features. I eventually understood that CSP does not simply choose the best electrodes. It learns weighted combinations of all electrodes. Applying one of these spatial filters creates a new time series called a CSP component, and the power of that component is then summarized into a CSP feature.

I also needed to distinguish model parameters from hyperparameters.

Parameters are learned from the training data. Examples include CSP spatial-filter weights and the means, covariance structure, and decision boundary learned by LDA.

Hyperparameters are choices about how the learning procedure operates. For example, `n_components=4` determines how many CSP components are retained. It is chosen before fitting rather than learned directly by CSP.

The evaluation code was another source of confusion. In particular, I had to understand that `LeaveOneGroupOut` returns indices identifying which trials belong to the training and test sets rather than returning the EEG data themselves.

I was also confused by how LDA actually works.

At first, I understood LDA mainly as “a classifier that draws a straight line between two classes.” That is directionally correct, but incomplete. I did not initially understand what the line was based on.

LDA assumes that the CSP features for each class form roughly bell-shaped clusters in feature space.

For example, after CSP, each trial may be represented by four features. Left-imagery trials form one cluster of points, and right-imagery trials form another.

LDA then models:

- the center of the left-imagery cluster,
- the center of the right-imagery cluster,
- and how the features spread and vary together.

The center of each cluster is its **mean**.

The way the features spread and vary together is described by the **covariance matrix**.

The key LDA assumption is that the two classes can have different centers, but approximately the same shape and spread.

In simpler terms:

`different means`
→ the left and right clusters are centered in different places

`shared covariance matrix`
→ the two clusters are assumed to have roughly the same shape, spread, and orientation

Because LDA assumes this shared covariance structure, the resulting boundary between the two classes is linear.

I had also initially mixed up variance and covariance.

Variance describes how much one feature varies.

Covariance describes how two features vary together.

For example, if CSP feature 1 tends to increase when CSP feature 2 also increases, they have positive covariance.

The covariance matrix contains the variances of the individual features and the covariances between them.

So LDA is not simply drawing an arbitrary straight line. It learns where the two class clusters are centered and how the feature space is distributed, then uses that information to construct a linear decision boundary.

In this project:

`EEG`
→ `CSP`
→ `four log-power features`
→ `LDA models the left/right feature clusters`
→ `linear decision boundary`
→ `left/right prediction`

**What decision did I make?**
This week I decided to establish a fixed classical baseline before attempting to optimize the model.

The baseline uses:

- the Week 4 preprocessing protocol,
- 7–30 Hz EEG,
- the +1 to +4 second machine-learning window,
- all 64 channels,
- four CSP components,
- LDA,
- leave-one-run-out cross-validation,
- balanced accuracy as the primary metric.

These settings were kept unchanged across all 109 subjects.

I deliberately did not try several CSP component counts or repeatedly modify the frequency band after observing performance. Doing so would turn the baseline experiment into model optimization and could introduce selection bias.

---

### **What limitation did I notice?**

The major limitation was that decoding performance varied dramatically between subjects.

Across all 109 subjects, mean balanced accuracy was approximately 0.597 and median balanced accuracy was approximately 0.568, but individual subject averages ranged from approximately 0.351 to 0.979.

This means that the cohort average hides substantial heterogeneity.

The three held-out runs had similar cohort-average balanced accuracies:

- Run 4: approximately 0.589
- Run 8: approximately 0.595
- Run 12: approximately 0.608

There was therefore no obvious large systematic difference between runs, while differences between subjects were much larger.

However, I cannot yet conclude that every subject above 0.50 shows statistically meaningful decoding. Individual folds contain relatively few trials, and I have not yet performed statistical significance or permutation testing.

Most importantly, the experiment remains within-subject. Every subject's model was trained using EEG from that same person. The results therefore say nothing yet about whether a model can generalize to an entirely unseen individual.

---

### **How does this connect to my larger goal?**

This week moved NeuroSignalLab from preprocessing into actual brain-signal decoding.

More importantly, it showed why evaluation design is as important as model architecture.

A model score only becomes meaningful when I can explain exactly what information the model was allowed to learn from and exactly what information remained unseen.

The experiment also revealed an important challenge in EEG machine learning: the same method can work extremely well for some individuals and poorly for others.

This begins to shift the project from simply asking:

> Can I classify motor imagery?

toward the more interesting question:

> How reliable and generalizable are EEG decoding systems across recordings and across people?

That question is directly relevant to whether a neurotechnology model can move beyond a carefully calibrated individual experiment and become useful across a broader population.

---

### **What is the next step?**

The next step is to test cross-subject generalization.

The current baseline asks whether a model can generalize from two runs to an unseen run from the same person.

The next experiment will instead ask:

> Can a model trained using EEG from some subjects classify motor imagery from a completely unseen subject?

This changes the evaluation unit from:

`unseen run`

to:

`unseen person`

and will test whether the spatial motor-imagery patterns learned by CSP + LDA transfer across individuals.

After establishing that baseline, later experiments can investigate controlled hyperparameter optimization, statistical significance, alternative classical methods, and eventually deep-learning approaches.

### Week 6

**What did I build this week?**

**What did I learn technically?**

**What confused me?**

**What decision did I make?**

**What limitation did I notice?**

**How does this connect to my larger goal?**

**What is the next step?**

## Connection to application to the US
THis project clarifies my interest in studying at intersections of medicine, informatics, neuroscience and human-centered AI. I am trying to build technical skills that can work with biological data, which furthers my medical understanding. 

Cornell, specifically is relevant because it can provide an environment where i can combine computing, neuroscience, data science and heath-related applications in an intentional and serious way. 

## One-sentence TLDR
I built NeuroSignalLab to understand the process from raw EEG signals to machine-learning predictions, while learning the challenges you face while developing responsible neurotechnology.
