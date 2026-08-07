# neurosignallab

## Overview
EEG-based motor imagery decoding with public data sets, classic ML, deep learning, and interpretability tools. 

## Medical Disclaimer
This is a research and educational project for me own development. It is not a diagnostic tool, medical device or clinial support system. THe models and visualizations in this repository shoudl not be used to diagnose, monitor, treat or predict neurological disease 

## Motivation
I started NeuroSignallab because i wanted to learn how to translate biological signals into useful systems. 

As a medical student i am learning how the physiology of the nervous system works. As an informatics student I am learning how to interpret complex data into tools.

Through my research at a neurophysiology lab, I learned how to study brain signals and connectivity patterns quantitatively, which furthered my interest in combining these two interests into a concrete technical project. 

Therefore, I wish to translate this complex noisy EEG-data into a software that can showcase, interpret and visualize brain signals in a reproducible manner. 


## Research Question

How reliably can classical machine-learning and EEG deep-learning models decode motor-imgaery states from open EEG records?

What do preprocessing, evaluation design, and interpretability reveal about the limits of applying EEG machine-learning to neurotechnology or clinical contexts?

This project uses open EEG datasets to build a reproducible pipeline for loading, preprocessing, visualizing, classifying, and interpreting brain-signal data. The goal is not only to compare model performance, but also to understand the practical challenges of EEG-based machine learning, including subject variability, data leakage, model interpretability, and clinical limitations.

## Dataset

The repository does not include the full raw EEG datasets used in this project. 

Users should download datasets directly from the original sources: 

- PhysioNet EEG Motor Movement/Imagery Dataset
- CHB-MIT Scalp EEG Database (SUBJECT TO REMOVAL)

- Only small sample files are included for demonstration purposes

## License
This project´s source code is licensed under the MIT License. 

The datasets in this project are not redistributed in this repository. The datasets are governed by their own original licenses, access conditios and citation requirements. Please refer to the origianl dataset providers for dataset access, citation requirements and terms of use. 

## Planned Methods

This project will build a reproducible EEG machine-learning pipeline for motor-imagery brain-computer interface exploration, with an optional clinical EEG extension using seizure data.

### 1. EEG Data Loading and Exploration

The first stage will use MNE-Python file to load EEG recordings from open datasets such as the PhysioNet EEG Motor Movement/Imagery dataset. I will inspect sampling frequency, channel names, recording duration, annotations/events, and basic raw EEG.

### 2. Preprocessing

The EEG data will be preprocessed by selecting relevant EEG channels, applying bandpass filtering, extracting task-related events, and converting raw continious EEG recordings into fixed-length epochs suitable for machine-learning models.

For motor imagery, the initial preprocessing will focus on frequency ranges commonly associated with sensorimotor rhythms, especially the mu/alpha and beta bands.

### 3. Manual interpretation

Before deep learning, I will build classical baseline/convolution models using interpretable EEG features such as channel variance, bandpower, power spectral density features, and potentially Common Spatial Pattern features.

These baselines provide a comparison point for later deep-learning models.

### 4. Classical Machine-Learning Models

I will train simple classifiers such as logistic regression, random forest, and/or support vector machines using scikit-learn. These models will help establish whether the preprocessing and feature extraction pipeline contains useful signal.

### 5. Deep-Learning Models

After building classical baselines, I will train a simple convolutional neural network on EEG epochs. I will then compare this with an EEGNet-style model using PyTorch and/or Braindecode.

The goal is not only to maximize accuracy, but to understand how deep-learning models handle EEG signals compared with simpler baselines.

### 6. Evaluation

The project will compare "naive random splits" with more realistic session-wise or subject-wise evaluation. EEG models can appear artificially strong if data from the same subject or session leaks into both training and testing sets.

Metrics will include accuracy, balanced accuracy, F1 score, confusion matrix, and per-class performance.

### 7. Visualization and Dashboard

I will build visualizations of raw EEG signals, filtered signals, power spectra, spectrograms, model predictions, and evaluation results. These will later be integrated into a Streamlit dashboard.

### 8. Interpretability

The project will explore simple interpretability methods such as saliency maps and occlusion sensitivity to visualize which EEG channels or time segments most influenced the model prediction.

These visualizations will be treated as tools, not as proof of true causation.

### 9. Optional Clinical EEG Extension

If the main motor-imagery pipeline is stable, I will add an exploratory seizure-detection extension using the CHB-MIT scalp EEG dataset. This extension will be presented carefully as an educational/research exploration, not as a diagnostic system.

### 10. Reproducibility

The project will be organized into notebooks, reusable Python scripts, saved configurations, saved metrics, and a clear technical report so that the analysis can be inspected and repeated.

## Expected Deliverables


By the end of this project, NeuroSignalLab aims to include the following deliverables:

### 1. EEG Data Loading and Visualization

A program that loads open EEG recordings using MNE-Python, inspects metadata such as sampling frequency, number of channels and channel names, and visualizes raw EEG signals.

Expected output:

* `notebooks/01_load_and_visualize_eeg.ipynb`
* raw EEG figure
* short explanation of dataset structure

### 2. EEG Preprocessing Pipeline

A reproducible preprocessing program that converts continuous EEG recordings into epochs.

Expected output:

* channel selection
* bandpass filtering
* event extraction
* epoch creation
* saved processed arrays
* `notebooks/02_preprocess_motor_imagery.ipynb`

### 3. Baseline Machine-Learning Models

Classical machine-learning baselines trained on interpretable EEG features before using deep learning.

Expected features may include:

* channel variance
* bandpower
* power spectral density features
* Common Spatial Pattern features, if appropriate

Expected models may include:

* logistic regression
* random forest
* support vector machine or similar classifier

### 4. Deep-Learning Model

A simple CNN and/or EEGNet-style model trained on EEG epochs for motor-imagery classification.

Expected output:

* PyTorch dataset and dataloader
* CNN or EEGNet-style model
* training curves
* saved model checkpoint
* model comparison against classical baselines

### 5. Evaluation

A comparison of different evaluation strategies to avoid misleading results.

Expected evaluation methods:

* naive random split
* session-wise split
* subject-wise split, if possible

Expected metrics:

* accuracy
* balanced accuracy
* F1 score
* confusion matrix
* per-class performance

The goal is not only to report performance, but to understand how evaluation design affects the apparent reliability of EEG machine-learning models.

### 6. Visualizations

A set of figures that make the project understandable to both technical and non-technical readers.

Expected figures:

* raw EEG trace
* filtered EEG trace
* power spectral density plot
* spectrogram or time-frequency plot
* confusion matrix
* model comparison chart

### 7. Streamlit Dashboard

An interactive dashboard that demonstrates the project pipeline using sample EEG data.

Expected app features:

* select an EEG sample/window
* view EEG trace
* view spectrogram or frequency-domain representation
* view model prediction
* view model confidence
* read limitations and disclaimer

### 8. Interpretability Module

A basic interpretability analysis using saliency maps and/or occlusion sensitivity.

Expected output:

* channel-by-time attribution heatmap
* occlusion-based channel or time-window importance plot
* explanation of what the attribution does and does not mean

### 9. Technical Report

A short technical report summarizing the motivation, dataset, methods, results, limitations, and future work.

Expected output:

* `reports/NeuroSignalLab_Technical_Report.pdf`

### 10. Optional Clinical EEG Extension

If the main motor-imagery pipeline is stable, the project may include an extension using public seizure EEG data.

This extension will be presented as exploration of the signals, not as a diagnostic model.


## Limitations and Ethics

NeuroSignalLab is a research and educational project. It is not a medical device, diagnostic tool, or clinical decision-support system. The models and visualizations in this repository should not be used to diagnose, monitor, treat, or predict neurological disease.

### Main Limitations

#### 1. Use of Public Datasets

This project uses open EEG datasets. TThe datasets are used for learning and research, but may not represent real-world clinical conditions, different patient populations, different EEG devices, or hospital environments.

#### 2. Subject Variability

EEG signals vary strongly between individuals. A model that performs well on one subject may not generalize to another subject. For this reason, the project will compare different evaluation strategies, including subject-wise or session-wise testing when possible.

#### 3. Risk of Data Leakage

EEG data can be especially vulnerable to data leakage. If windows from the same subject or recording session appear in both the training and test sets, model performance may appear better than it actually is. This project will explicitly compare naive and more realistic evaluation methods.

#### 4. Artifact Sensitivity

EEG recordings can be affected by eye blinks, muscle activity, electrode noise, faulty nodes, movement, and other artifacts. These artifacts may influence both classical machine-learning models and deep-learning models.

#### 5. Model Confidence Is Not Medical Certainty

A high model confidence score does not mean that the model is clinically correct. Model outputs should be interpreted as experimental predictions, not medical conclusions.

#### 6. Interpretability Limitations

Saliency maps and occlusion sensitivity can show which parts of the input influenced the model’s prediction, but they do not prove that those channels or time segments reflect true neurophysiological causes.

#### 7. Limited Clinical Validation

This project does not include prospective testing, neurologist validation, real-time EEG acquisition, regulatory review, or clinical workflow testing.

#### 8. Data and Privacy

The repository will not include private patient data. Large raw EEG datasets will not be redistributed through this repository. Users can download datasets directly from the original sources and follow the original dataset terms, licenses, and citation requirements.

### Ethical Position

The purpose of this project is to learn how neural signal data can be loaded, processed, modeled, visualized, and evaluated responsibly. 

The project seeks to emphasize its scientific humility, reproducibility, and careful communication of limitations.


## Project Roadmap

### Phase 1: Project Setup and EEG Foundations

**Goal:** Set up the repository and define the research question.

Planned tasks:

* create project repository
* write README v0
* write `notes/project_story.md`
* set up Python environment
* create notes for basic EEG concepts

Expected outputs:

* clean repository structure
* project story note
* EEG basics note
* Neurosignallab (NSL) environment

---

### Phase 2: EEG Loading and Visualization

**Goal:** Load real EEG recordings and visualize the raw signal.

Planned tasks:

* download a small subset of the PhysioNet EEG Motor Movement/Imagery dataset
* load EEG files using MNE-Python
* inspect sampling frequency, channel names, and recording duration
* plot raw EEG traces

Expected outputs:

* `notebooks/01_load_and_visualize_eeg.ipynb`
* raw EEG trace figure

---

### Phase 3: EEG Preprocessing

**Goal:** Convert continuous EEG recordings into machine-learning-ready epochs.

Planned tasks:

* select EEG channels
* apply bandpass filtering
* extract task events or annotations
* create epochs around motor-imagery events
* save processed arrays for modeling

Expected outputs:

* `notebooks/02_preprocess_motor_imagery.ipynb`
* processed EEG arrays
* short explanation of preprocessing decisions

---

### Phase 4: Classical Baseline Models

**Goal:** Build simple baseline models before using deep learning.

Planned tasks:

* extract interpretable EEG features
* train classical machine-learning models
* evaluate baseline performance
* create first confusion matrix and metrics table

Expected outputs:

* `notebooks/03_baseline_features_and_models.ipynb`
* baseline results table
* confusion matrix

---

### Phase 5: Honest Evaluation

**Goal:** Evaluate models in a way that avoids misleading performance claims.

Planned tasks:

* compare naive random split with session-wise or subject-wise splits
* use balanced accuracy, F1 score, and confusion matrices
* explain how data leakage can affect EEG model performance

Expected outputs:

* `notebooks/04_honest_evaluation.ipynb`
* split comparison table
* short report on EEG evaluation limitations

---

### Phase 6: Deep-Learning Models

**Goal:** Train a CNN and/or EEGNet-style model on EEG epochs.

Planned tasks:

* convert EEG epochs into PyTorch tensors
* create Dataset and DataLoader objects
* train a simple CNN
* train or test an EEGNet-style model
* compare deep learning against classical baselines

Expected outputs:

* `notebooks/05_simple_cnn.ipynb`
* `notebooks/06_eegnet_comparison.ipynb`
* training curves
* model comparison table

---

### Phase 7: Visualization and Dashboard

**Goal:** Build an interactive demo that makes the project understandable.

Planned tasks:

* create EEG trace visualizations
* create PSD or spectrogram visualizations
* build a Streamlit dashboard
* add model prediction to the dashboard
* add disclaimers and limitations

Expected outputs:

* `app/streamlit_app.py`
* public demo link, if deployed
* dashboard screenshots

---

### Phase 8: Interpretability

**Goal:** Explore which EEG channels or time segments influence model predictions.

Planned tasks:

* implement saliency maps
* implement occlusion sensitivity
* visualize attribution results
* explain interpretability limitations

Expected outputs:

* `notebooks/07_interpretability.ipynb`
* saliency heatmap
* occlusion importance plot

---

### Phase 9: Optional Clinical EEG Extension

**Goal:** Explore whether the same pipeline can be adapted to clinical EEG seizure data.

Planned tasks:

* load a small subset of public seizure EEG data
* create seizure and non-seizure windows
* train a simple baseline model
* discuss clinical limitations carefully

Expected outputs:

* exploratory seizure notebook
* seizure/non-seizure visualization
* short limitations section

---

### Phase 10: Final Report and Portfolio Package

**Goal:** Turn the project into a polished portfolio artifact.

Planned tasks:

* clean repository
* refactor reusable scripts
* finalize README
* write technical report
* create demo video or screenshots
* connect project to Cornell application narrative

Expected outputs:

* final README
* technical report PDF
* GitHub repository
* app demo
* project summary for applications


## Current Status

Phase 1

## How to Run

TBD
