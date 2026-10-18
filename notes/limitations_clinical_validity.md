# Limitations and Clinical Validity

## 1. Project scope

NeuroSignalLab is an educational research project investigating
subject-independent motor-imagery EEG classification.

The task is binary classification of imagined left versus imagined right fist movement using EEG. It does not claim to do anything more than that. 

## 2. Final generalization performance

The final Configuration D EEGNet was evaluated once on a held-out test
set containing 17 previously unseen subjects and 757 trials.

Final results:

- Accuracy: 0.5760
- Balanced accuracy: 0.5756
- Macro F1: 0.5721

The held-out balanced accuracy was lower than the development validation
balanced accuracy of 0.6277.

This indicates that validation performance had lower
generalization to completely unseen subjects.

## 3. Subject-to-subject variability

Performance varied substantially between unseen subjects.

Test-subject balanced accuracy ranged from approximately:

- lowest: 0.458
- highest: 0.801

Mean subject balanced accuracy was approximately 0.578.

Some subjects were decoded substantially better than others.

This is an important limitation for subject-independent EEG decoding,
where differences between individuals can strongly affect model
performance.

## 4. Class asymmetry

The final test confusion matrix was:

- true left → predicted left: 254
- true left → predicted right: 126
- true right → predicted left: 195
- true right → predicted right: 182

The model therefore performed better on imagined-left trials than on
imagined-right trials in the final test set.

This asymmetry should be reported rather than corrected after observing
the test results.

## 5. Dataset and external validity

The project uses the PhysioNet EEG Motor Movement/Imagery Dataset
(EEGMMIDB).

The final analysis includes 109 subjects and uses motor-imagery runs
4, 8, and 12.

Results are specific to this dataset, task, preprocessing pipeline, and
evaluation protocol.

Performance should not be assumed to transfer directly to:

- different EEG hardware
- different electrode montages
- different recording environments
- different motor-imagery paradigms
- clinical populations
- real-time BCI systems
- rehabilitation settings

External validation on independent datasets would be required before
making broader generalization claims.

## 6. Offline versus online BCI

NeuroSignalLab performs offline classification of pre-recorded EEG.

The current pipeline does not include:

- live EEG acquisition
- continuous streaming preprocessing
- online artifact handling
- real-time windowing
- adaptive calibration
- decision smoothing
- feedback to the user
- control of an external device
- closed-loop neurofeedback

The project should be described as an offline EEG decoding
research prototype rather than a complete online BCI.

## 7. Preprocessing assumptions

The preprocessing pipeline is fixed and includes:

- 64 EEG channels
- common-average reference
- 7–30 Hz FIR filtering
- 160 Hz sampling rate
- +1 to +4 second analysis window
- no arbitrary epoch rejection

These choices define the signal presented to the model.

## 8. Limited task complexity

The current task contains only two classes:

- imagined left fist
- imagined right fist

A binary, cue-based motor-imagery experiment is substantially simpler
than many real BCI applications.

Successful performance on this task does not demonstrate that the same
model could reliably decode:

- multiple movement classes
- continuous movement intention
- unconstrained EEG
- asynchronous user intent
- real-world BCI commands

## 9. Interpretability limitations

NeuroSignalLab uses:

- gradient saliency
- channel occlusion
- temporal occlusion
- learned temporal-filter visualization

These techniques describe properties of the model. They do not establish causal neurophysiology.

Similarly, learned temporal filters showed different frequency-response
profiles between approximately 12 and 28 Hz within the input band.

These should be described as learned model sensitivities rather than
specific physiological rhythms.

The 40-sample temporal kernels span only approximately 250 ms, so precise
frequency peaks should also be interpreted cautiously.

## 10. Occlusion perturbations are artificial

Channel occlusion was implemented by replacing one channel with zeros.

Because the EEG was common-average referenced, zeroing a single channel
also alters the relationships represented by the original referenced
signal.

Occlusion results should be treated as model-sensitivity
evidence rather than direct physiological evidence.

## 11. Neural-network uncertainty

The model's softmax outputs are displayed as model outputs rather than
calibrated confidence estimates.

No dedicated probability-calibration analysis was performed.

A value such as:

Left: 60%
Right: 40%

should not be interpreted as:

"There is a 60% probability that the subject imagined the left hand."

It only describes the relative output of the classifier after softmax.

## 12. Clinical validity

Decoder performance is not equivalent to clinical effectiveness.

A classification model can perform above chance while still being
unsuitable for rehabilitation or clinical use.

Clinical evaluation would require separate evidence involving outcomes
such as:

- functional improvement
- rehabilitation benefit
- usability
- safety
- reliability over repeated sessions
- patient-specific performance

NeuroSignalLab does not test these outcomes.

## 13. Neurorehabilitation interpretation

Motor-imagery EEG decoding is relevant to research on BCIs and
neurorehabilitation because cortical signals could potentially be used
to trigger feedback or external actions.

However, NeuroSignalLab only studies the decoding component of such a
system.

It does not demonstrate:

- neuroplastic change
- motor recovery
- therapeutic efficacy
- successful closed-loop rehabilitation

These remain possible future applications.

## 14. Test-set integrity

The final test set consisted of 17 subjects that were kept separate from
model development.

The frozen Configuration D seed-42 checkpoint was evaluated once.

After observing the test results:

- no architecture changes were made
- no hyperparameters were changed
- no preprocessing was changed
- no thresholds were changed
- no subjects were excluded
- no retraining was performed

The final test result is treated as a reporting result.

## 15. Main conclusion

NeuroSignalLab demonstrates that a compact EEG-specific neural network
can achieve stable performance for motor-imagery classification under a controlled development protocol.

The frozen model achieved 57.6% balanced accuracy on 17 completely
unseen test subjects, with substantial performance variation between
individuals.

The project demonstrates both the potential and the difficulty
of cross-subject EEG decoding.

It does not demonstrate a clinically deployable BCI or physiological
causality.