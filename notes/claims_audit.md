# NeuroSignalLab Claims Audit

## Purpose

This document defines which claims NeuroSignalLab can make based on the
completed experiments and which claims would go beyond the available
evidence.

It should be used when writing:

- the README
- technical report
- Streamlit app
- portfolio description
- CV bullets
- application materials
- presentations or interviews

The goal is to distinguish clearly between:

- measured results
- supported interpretations
- limitations
- possible future applications

and to avoid presenting interpretation as established fact.

---

# Claim categories

## MEASURED RESULT

Directly calculated from the project's data or model outputs.

These claims can normally be stated directly as long as the experimental
context is included.

## SUPPORTED INTERPRETATION

A reasonable conclusion from the measured results, but not itself a
direct measurement.

These claims should use cautious wording such as:

- suggests
- indicates
- is consistent with
- demonstrates within this dataset
- highlights

## LIMITATION

A known boundary of the experiment or a reason the result should not be
generalized too broadly.

## FUTURE APPLICATION

Something the project could potentially contribute to in the future but
did not test directly.

These claims should use wording such as:

- could
- may
- potential
- future work
- would require additional validation

## NOT SUPPORTED

A claim that should not appear as a conclusion of NeuroSignalLab.

---

# 1. Dataset and task

### Claim

"NeuroSignalLab studies motor-imagery EEG classification."

**Category:** MEASURED / FACTUAL PROJECT DESCRIPTION

**Status:** APPROVED

The task is classification of imagined left versus imagined right fist
movement from EEG.

### Claim

"NeuroSignalLab performs subject-independent EEG decoding."

**Category:** MEASURED / EXPERIMENTAL DESIGN

**Status:** APPROVED

Training, validation, and test subjects were separated at the subject
level.

The final test set contained subjects that were not used to train the
model.

NeuroSignalLab investigates subject-independent classification of left-versus-right motor-imagery EEG.

### Claim

"The model generalizes to completely unseen subjects."

**Category:** SUPPORTED INTERPRETATION

**Status:** APPROVED

The final model was evaluated on 17 previously unseen test subjects.

However, performance was modest and highly variable between subjects.

The frozen EEGNet retained measurable classification performance on previously unseen subjects, although substantial subject-to-subject variability remained. However, as performance varied, we cannot claim that the model generalized equally to all subjects

# 2. Final held-out test performance

### Claim

"The final held-out balanced accuracy was lower than the validation balanced accuracy"

**Category:** MEASURED RESULT

**Status:** APPROVED

Exact result:

- balanced accuracy = 0.5756
- accuracy = 0.5760
- macro F1 = 0.5721
- test subjects = 17
- test trials = 757

The frozen Configuration D EEGNet achieved 57.6% balanced accuracy on 757 trials from 17 held-out subjects.

### Claim

"The validation balanced accuracy was approximately 62.8%."

**Category:** MEASURED RESULT

**Status:** APPROVED

For the deployment seed-42 checkpoint:

- validation balanced accuracy = 0.6277

Configuration D also showed strong reproducibility across development
seeds.

### Claim

"The validation result overestimated final generalization."

**Category:** SUPPORTED INTERPRETATION

**Status:** APPROVED

Validation BA:

~62.8%

Final test BA:

~57.6%

Performance decreased by approximately five percentage points from validation to the final held-out cohort, indicating that development performance was somewhat optimistic for completely unseen subjects.

### Claim

"The model performed above chance."

**Category:** POTENTIALLY UNSUPPORTED STATISTICAL CLAIM

**Status:** DO NOT USE AS A FORMAL CLAIM

The observed balanced accuracy is greater than 0.50, but no dedicated
statistical significance test was pre-specified and performed on the
final held-out result.

The model achieved 57.6% balanced accuracy.

# 3. Subject variability

### Claim

"Performance varied substantially between subjects."

**Category:** MEASURED RESULT / SUPPORTED INTERPRETATION

**Status:** APPROVED

Final test-subject balanced accuracy ranged approximately from:

- 0.458
- to 0.801

Mean subject BA:

~0.578

Median subject BA:

~0.581

Generalization varied substantially across unseen subjects, with subject-level balanced accuracy ranging from approximately 46% to 80%.

---

### Claim

"The decoder works equally well for most people."

**Category:** NOT SUPPORTED

**Status:** DO NOT USE

The large subject-level range directly contradicts this claim.

---

# 4. Class-specific behavior

### Claim

"The final model performed better on imagined-left trials than
imagined-right trials."

**Category:** MEASURED RESULT

**Status:** APPROVED

Final confusion matrix:

- left → left: 254
- left → right: 126
- right → left: 195
- right → right: 182

This corresponds to better recall for imagined-left trials in the final
test cohort.

The held-out evaluation showed asymmetric class performance, with better recall for imagined-left than imagined-right trials.

---

### Claim

"The model is inherently biased toward left-hand imagery."

**Category:** TOO STRONG

**Status:** DO NOT USE

The final test cohort showed a left-prediction tendency, but this does not
establish that this is an inherent property of EEGNet in general.

The final test cohort showed a tendency toward left-class predictions.

---

# 5. Model comparison

### Claim

"EEGNet generalized better than the generic CNN during development."

**Category:** MEASURED RESULT

**Status:** APPROVED

Development results showed approximately:

- Generic CNN: 0.530 ± 0.014 BA
- CSP + LDA: 0.573 BA
- ShallowConvNet: 0.621 ± 0.007 BA
- Configuration D EEGNet: 0.628 ± 0.002 BA
- Constrained EEGNet: 0.634 ± 0.012 BA

Under the fixed subject-independent development protocol, EEG-specific architectures generalized substantially better than the generic CNN.

### Claim

"Configuration D was selected because it had the highest validation
accuracy."

**Category:** INCORRECT

**Status:** DO NOT USE

The constrained EEGNet had a slightly higher mean validation BA.

Configuration D was selected because it combined strong performance with
much lower between-seed variability.

Configuration D was selected as the primary model because it combined competitive validation performance with substantially greater reproducibility across random seeds.

# 6. Reproducibility

### Claim

"Configuration D was reproducible across random seeds."

**Category:** MEASURED RESULT / SUPPORTED INTERPRETATION

**Status:** APPROVED

Five-seed development result:

approximately:

0.628 ± 0.002 balanced accuracy

Configuration D showed highly consistent validation performance across five predefined random seeds.

---

### Claim

"The final test result itself is proven reproducible across random
seeds."

**Category:** NOT SUPPORTED

**Status:** DO NOT USE

Only the frozen seed-42 checkpoint was evaluated on the final test set.

Seed robustness was evaluated during development, not by repeatedly
training models against the held-out test cohort.

---

# 7. Interpretability

### Claim

"The model relies on centro-parietal EEG channels."

**Category:** SUPPORTED INTERPRETATION

**Status:** PARTIALLY APPROVED

Cross-subject channel occlusion showed strong class-dependent sensitivity
around channels including:

- CP3 / C3 for correct left predictions
- CP4 / C4 for correct right predictions

Channel occlusion showed class-dependent model sensitivity around centro-parietal electrodes.

### Claim

"The model learned activation in motor cortex."

**Category:** NOT SUPPORTED

**Status:** DO NOT USE

Scalp EEG electrodes are not equivalent to localized cortical sources. The project did not perform source localization.

The model showed electrode-level sensitivity patterns.

---

### Claim

"The interpretability maps show brain activation."

**Category:** NOT SUPPORTED

**Status:** DO NOT USE

Topographic plots interpolate electrode-level model-sensitivity values. They are not maps of cortical activation.

### Claim

"Gradient saliency was checked against an untrained model."

**Category:** MEASURED RESULT

**Status:** APPROVED

The trained-model saliency maps showed little positive correlation with
those from a randomly initialized EEGNet across the tested validation
examples.

Do not describe this as a complete formal interpretability validation.

# 8. Learned temporal filters

### Claim

"EEGNet learned multiple distinct temporal filters."

**Category:** MEASURED RESULT / SUPPORTED INTERPRETATION

**Status:** APPROVED

The first convolution contained eight different learned kernels.

Within the 7–30 Hz input band, their peak normalized magnitude responses
were distributed approximately between 12 and 28 Hz.

### Claim

"The network learned mu and beta rhythms."

**Category:** NOT SUPPORTED

**Status:** DO NOT USE

Some learned filter responses overlap frequencies commonly associated
with sensorimotor EEG rhythms, but frequency overlap alone does not
establish physiological identity.

The learned temporal kernels showed distinct frequency-response profiles across approximately 12–28 Hz within the available input band.

---

### Claim

"Filter 1 detects exactly 12.50 Hz."

**Category:** TOO PRECISE

**Status:** AVOID

The kernels span only 40 samples / 250 ms.

The FFT was zero-padded for visualization, which creates a smoother
frequency curve but does not create additional true frequency
resolution.

Filter 1 showed its strongest response around 12–13 Hz.

---

# 9. BCI claims

### Claim

"NeuroSignalLab is a brain-computer interface."

**Category:** TOO STRONG

**Status:** DO NOT USE WITHOUT QUALIFICATION

The project implements an offline EEG decoding component that could form
part of a BCI.

It does not implement a full online BCI loop.

### Claim

"NeuroSignalLab is a real-time BCI."

**Category:** NOT SUPPORTED

**Status:** DO NOT USE

The project does not perform live EEG acquisition, continuous processing,
real-time decision logic, or feedback.

### Claim

"The project demonstrates closed-loop neurofeedback."

**Category:** NOT SUPPORTED

**Status:** DO NOT USE


# 10. Neurorehabilitation claims

### Claim

"Motor-imagery decoding has potential relevance to neurorehabilitation."

**Category:** FUTURE APPLICATION / CONTEXT

**Status:** NOT YET APPROVED 

Motor-imagery decoding is relevant to research on future neurorehabilitation BCIs, where detected cortical activity could potentially be linked to external feedback or assistance.

---

### Claim

"NeuroSignalLab improves rehabilitation outcomes."

**Category:** NOT SUPPORTED

**Status:** DO NOT USE

No patients, rehabilitation intervention, clinical outcomes, or
longitudinal recovery measures were studied.

### Claim

"The system induces neuroplasticity."

**Category:** NOT SUPPORTED

**Status:** DO NOT USE

No neuroplastic changes were measured.

### Claim

"The model could eventually be connected to FES, robotics, or other
feedback systems."

**Category:** FUTURE APPLICATION

**Status:** NOT YET APPROVED

This should always be presented as a possible future extension, not an
existing capability.

---

# 11. Clinical claims

### Approved description

NeuroSignalLab is an educational and research prototype and has not been validated for diagnostic, therapeutic, or clinical use.

---

# 12. Model-output claims

### Claim

"The model is 70% confident that the user imagined the left hand."

**Category:** NOT SUPPORTED

**Status:** DO NOT USE

The softmax outputs were not calibrated.

Do not call these calibrated probabilities or confidence estimates.


# 13. Final-test integrity

### Claim

"The final result was evaluated on a previously untouched test cohort."

**Category:** MEASURED / EXPERIMENTAL DESIGN

**Status:** APPROVED

The 17 test subjects were not used for:

- architecture selection
- hyperparameter selection
- early stopping
- interpretability development
- Streamlit model development
- model selection

The frozen model was evaluated once.

# 14. Main project conclusion

## Approved concise conclusion

NeuroSignalLab investigated subject-independent left-versus-right motor-imagery EEG decoding using classical and neural-network approaches. EEG-specific architectures generalized more reliably than a generic CNN during development, and the selected Configuration D EEGNet showed highly stable validation performance across random seeds. On a final held-out cohort of 17 unseen subjects, the frozen model achieved 57.6% balanced accuracy, with substantial variation between individuals. Interpretability analyses showed class-dependent electrode sensitivity and distinct learned temporal-filter responses, but these findings describe model behavior rather than causal neurophysiology.

---

# 15. Claims suitable for a CV

Appropriate examples:

> Built an end-to-end PyTorch EEG decoding pipeline for subject-independent motor-imagery classification across 109 subjects, comparing classical and deep-learning approaches.

> Developed and evaluated EEGNet using subject-level train/validation/test separation, multi-seed reproducibility analysis, interpretability, and a held-out 17-subject final evaluation.

> Built a Streamlit research demo integrating EEGNet inference, EEG visualization, and channel-occlusion interpretability.

Use the exact final performance number only when useful:

> Achieved 57.6% balanced accuracy on a final held-out cohort of 17 previously unseen subjects.

# 16. Future-work claims

The following can be discussed as future work rather than completed
results:

- online EEG streaming
- subject-specific calibration
- adaptive decoding
- session-to-session robustness
- independent external-dataset validation
- artifact handling under real-world conditions
- closed-loop feedback
- FES or robotic-control integration
- clinical-population evaluation
- additional motor-imagery classes

These should never be described as capabilities already demonstrated by
NeuroSignalLab.

# Final rule

For every important public claim, ask:

1. Did NeuroSignalLab directly measure this?
2. If not, is it a cautious interpretation supported by the results?
3. Is it actually a limitation or future possibility?
4. Could a reader interpret the wording as a stronger medical,
   physiological, or engineering claim than the project demonstrated?

When uncertain, prefer the narrower claim.