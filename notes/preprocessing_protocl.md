# Week 4 — Preprocessing Protocol

## 1. Research Question

### Decision
Can EEG distinguish imagined left-fist movement from imagined right-fist movement?

The initial project is a binary motor-imagery classification problem.

## 2. Dataset

PhysioNet EEG Motor Movement/Imagery Dataset (EEGMMIDB).[^physionet]

The dataset contains 64-channel EEG sampled at 160 Hz and includes repeated motor-execution and motor-imagery runs.[^physionet]

## 3. Runs

### Decision

Use: `runs = [4, 8, 12]`

### Reasoning

MNE and PhysioNet identify runs 4, 8, and 12 as the three repetitions of the left-versus-right motor-imagery task.[^physionet][^mne-eegbci]

Using all three runs increases the available number of trials while keeping the experimental task consistent.

We will not initially combine them with runs 6, 10, and 14 because those runs represent a different motor-imagery task.[^physionet][^mne-eegbci]

Mixing these tasks would change the meaning of `T1` and `T2`.

## 4. Classification Classes

### Decision

Use:

- `T1` = imagined left fist
- `T2` = imagined right fist

Do not use `T0` as a classification class in the initial model.

### Reasoning

For runs 4, 8, and 12, PhysioNet defines:

- `T0` = rest
- `T1` = left-fist imagery
- `T2` = right-fist imagery[^physionet]

The primary research question concerns the more subtle distinction between two motor-imagery states.

Including `T0` would introduce an easier rest-vs-task distinction, as opposed to the left-vs-right distinction.

`T0` will remain in the original continuous recording and can still be used for inspection/referencing

## 5. Channels

### Decision

Retain all 64 EEG channels during initial preprocessing.

### Reasoning

Motor imagery produces spatially distributed sensorimotor EEG patterns rather than information confined to a single electrode.[^mcfarland]

CSP is designed to learn weighted spatial combinations of multiple electrodes.[^ramoser][^mne-csp]

The MNE CSP example also retains all available EEG channels rather than restricting the classifier to C3, Cz, and C4.[^mne-csp-example]

Restricting the classifier to these electrodes now would constitute an early "feature-selection" decision that has not yet been demonstrated to be optimal.

Keep in mind that data-driven channel selection must be fitted using training data only.

## 6. EEG Reference

### Decision

Use common average referencing, and store the average reference as an MNE projection:

`raw.set_eeg_reference("average", projection=True)`

### Reasoning

EEG voltages are measured relative to a reference rather than as absolute potentials.

MNE's average-reference procedure creates a reference using the average across eligible EEG channels.[^mne-reference]

With `projection=True`, MNE stores the average-reference transformation as a projector rather than immediately modifying the EEG samples.[^mne-reference]

That means the projector can later adapt to excluded channels or marked "bad" channels.[^mne-reference-tutorial]

This is also the approach used in MNE's motor-imagery CSP example.[^mne-csp-example]

The projector can then be applied during the processing stage.

## 7. Frequency and Filtering

### Decision

Apply a `7–30 Hz` band-pass filter.

### Reasoning

Motor imagery is associated with changes in sensorimotor mu and beta rhythms.[^mcfarland][^erd]

McFarland et al. demonstrated motor-imagery desynchronization in mu and beta activity, while MNE's standard motor-imagery CSP example uses a 7–30 Hz band-pass filter.[^mcfarland][^mne-csp-example]

The 7–30 Hz band is therefore a broad, literature-supported baseline.

Later experiments may evaluate:

- narrower bands
- separate mu and beta bands
- filter-bank CSP
- subject-specific spectral selection



Filtering will use an FIR design consistent with MNE's standard workflow.

When filtering concatenated runs, run boundaries must be accounted for.

The MNE CSP example uses `skip_by_annotation="edge"` to avoid treating discontinuous recording segments as one continuous signal.[^mne-csp-example]

MNE's filtering documentation and Widmann et al. emphasize that filtering can induce temporal ringing and other distortions, so cutoff and transition parameters should be treated as methodological choices.[^widmann][^mne-filter]

---

## 8a. Stored Epochs Window

### Decision

Create epochs from:

`-1.0 s to +4.0 s`

relative to T1/T2 onset.

### Reasoning

MNE's motor-imagery CSP example uses epochs from -1 to +4 seconds.[^mne-csp-example]

MNE's ERDS example also analyzes motor-imagery activity over approximately this interval, and importantly **uses the pre-cue period for ERD/ERS reference calculations**.[^mne-erds]

At 160 Hz, MNE includes both time endpoints.

Therefore:

`(-1 to +4 s) = 5 seconds`

and:

`5 × 160 + 1 = 801 time samples`[^mne-epochs]

Expected full-epoch shape for one trial:

`64 channels × 801 samples`

Keep in mind the pre-cue section provides:

- context before the motor-imagery cue
- a period for visual QC
- a possible reference period for later ERD/ERS analysis

## 8b. Machine-Learning Epochs Window

### Decision

For the initial classifier, use:

`+1.0 s to +4.0 s`

from each stored epoch.

### Reasoning

The MNE CSP example explicitly delays classification until one second after cue onset to **reduce classification of cue-evoked responses** rather than the intended motor-imagery activity.[^mne-csp-example]

MNE's example specifically uses 1–2 seconds for its training demonstration.

Our use of 1–4 seconds is therefore a project design choice, not a value directly prescribed by MNE.

The reasoning is to:

1. exclude the first second after the visual cue;
2. retain a longer interval of sustained motor imagery for later classical and deep-learning models.

This decision should remain fixed for the initial baseline rather than being adjusted after observing classification accuracy.

At 160 Hz:

`(4 - 1) × 160 + 1 = 481 samples`

because MNE includes the final time point.[^mne-epochs]

Expected machine-learning trial shape:

`64 channels × 481 time samples`


## 9. Baseline Correction

### Decision

Use `baseline=None` for the primary machine-learning epochs.

### Reasoning

MNE's motor-imagery CSP example does not apply voltage baseline correction to the epochs.[^mne-csp-example]

This is appropriate because the initial classification problem focuses on oscillatory spatial/spectral features, not an ERP amplitude relative to a voltage baseline.

For later ERD/ERS visualization, the pre-cue period,`-1 to 0 s`, may be used as a power reference.[^mne-erds]

Please do not confuse these two operations.

Essentially, 
Machine-learning epoch `baseline=None` and ERD/ERS reference `compares task-period spectral power with reference-period spectral power` (pre cue period)

Please note that the choice of ERD/ERS reference interval can substantially affect estimated ERD/ERS magnitude.[^erd-baseline]

## 10. Sampling Frequency

### Decision

Retain the native:

`160 Hz`

sampling frequency.

### Reasoning

PhysioNet records EEGMMIDB at 160 samples per second.[^physionet]

The Nyquist frequency is therefore:

`160 / 2 = 80 Hz`

A 30 Hz upper passband is well below the 80 Hz Nyquist limit (causing no aliasing) at 160 Hz sampling rate.

There is no need to resample currently.

Keeping the native sampling rate also avoids introducing an unnecessary preprocessing operation.

---

## 11. Dataset Quality Control

### Decision

Perform explicit QC before modeling.

### Reasoning

Shuqfa et al. demonstrated that EEGMMIDB contains recording irregularities and excluded six subjects in their curated version.[^shuqfa]

This means that dataset integrity should be checked rather than assumed.

For every subject, I should verify:

- subject ID
- run ID
- sampling frequency
- recording duration
- number of channels
- expected channel names
- presence of T1 and T2
- number of T1 trials
- number of T2 trials
- missing annotations
- NaN values
- infinite values
- extreme amplitudes
- flat channels or epochs

After epoching, also verify:

- expected number of epochs
- epoch dimensions
- class balance
- dropped epochs
- reasons for epoch rejection

The six abnormal subjects previously identified should be treated as QC flags and not initially excluded.

Note: The final exclusion criteria must be written down before the final model evaluation.

## 12. Artifact Rejection

### Decision

Do not immediately copy an amplitude-rejection threshold from another EEG study.

First inspect the distribution and quality of the epochs.

### Reasoning

MNE can reject epochs based on maximum peak-to-peak amplitude using `reject`, and can identify unusually flat signals using `flat`.[^mne-epochs]

If a threshold is eventually introduced, it should be:

- justified from the current dataset
- documented
- applied consistently
- selected before final model evaluation

## 13. Preservation of Metadata

### Decision

Preserve at least:

- subject ID
- run ID
- trial/event ID
- class label

for every epoch.

### Reasoning

These identifiers are needed later to create more secure train/test splits.

For example, subject-wise generalization cannot be evaluated correctly if the subject identity is missing.

Run identity could also be useful for:

- run-wise QC
- debugging
- evaluating session/run effects
- avoiding accidental dependence between training and test data

## 14. CSP and Train/Test Leakage

CSP will not be fitted during the basic preprocessing stage.

When CSP is introduced during baseline modeling, it must be placed inside the training/cross-validation pipeline (and not the test-split).[^mne-csp][^mne-csp-example]

Because CSP uses class labels, fitting it before splitting would allow information from the held-out data to influence the learned feature representation.

## 15. Initial Protocol Summary

The first baseline preprocessing protocol is therefore:

| Component | Decision |
|---|---|
| Dataset | PhysioNet EEGMMIDB |
| Task | Imagined left fist vs imagined right fist |
| Runs | 4, 8, 12 |
| Classes | T1 vs T2 |
| Rest | T0 retained but not classified |
| Channels | all 64 EEG channels |
| Reference | common average reference |
| Reference implementation | MNE projection |
| Filter | 7–30 Hz band-pass |
| Sampling rate | 160 Hz |
| Stored epochs | -1 to +4 s |
| Full epoch samples | 801 |
| ML window | +1 to +4 s |
| ML samples | 481 |
| Voltage baseline correction | None |
| ERD/ERS reference | possibly -1 to 0 s for later analysis |
| QC | mandatory before modeling |
| Metadata | preserve subject, run, trial, and class |
| CSP fitting | training data only |

These decisions should remain fixed for the first baseline experiment.

## 16. Processing Order / Workflow

The intended Week 4 sequence is:

`load runs 4, 8, 12`

→ `verify each run`

→ `standardize channel names`

→ `attach standard montage`

→ `preserve subject/run identity`

→ `concatenate runs while preserving boundaries`

→ `add average-reference projection`

→ `band-pass filter 7–30 Hz`

→ `extract events`

→ `retain T1/T2`

→ `create -1 to +4 s epochs`

→ `inspect epoch quality`

→ `perform QC`

→ `retain +1 to +4 s ML window`

→ `create X and y`

→ `preserve metadata`

→ `proceed to baseline modeling`

---

# References

[^physionet]: Schalk, G. (2009). *EEG Motor Movement/Imagery Dataset* (Version 1.0.0). PhysioNet. doi:10.13026/C28G6P.

[^mne-eegbci]: MNE Developers. *mne.datasets.eegbci.load_data — MNE-Python documentation*. Used for the official mapping between EEGBCI run numbers and experimental tasks.

[^shuqfa]: Shuqfa, Z., Lakas, A., & Belkacem, A. N. (2024). Increasing accessibility to a large brain–computer interface dataset: Curation of PhysioNet EEG Motor Movement/Imagery Dataset for decoding and classification. *Data in Brief, 54*, 110181. doi:10.1016/j.dib.2024.110181.

[^mcfarland]: McFarland, D. J., Miner, L. A., Vaughan, T. M., & Wolpaw, J. R. (2000). Mu and beta rhythm topographies during motor imagery and actual movements. *Brain Topography, 12*(3), 177–186. doi:10.1023/A:1023437823106.

[^erd]: Pfurtscheller, G., & Lopes da Silva, F. H. (1999). Event-related EEG/MEG synchronization and desynchronization: Basic principles. *Clinical Neurophysiology, 110*(11), 1842–1857. doi:10.1016/S1388-2457(99)00141-8.

[^ramoser]: Ramoser, H., Müller-Gerking, J., & Pfurtscheller, G. (2000). Optimal spatial filtering of single trial EEG during imagined hand movement. *IEEE Transactions on Rehabilitation Engineering, 8*(4), 441–446. doi:10.1109/86.895946.

[^mne-csp]: MNE Developers. *mne.decoding.CSP — MNE-Python documentation*. Used for CSP input/output structure and supervised fitting.

[^mne-csp-example]: MNE Developers. *Motor imagery decoding from EEG data using the Common Spatial Pattern (CSP) — MNE-Python documentation*. Used for the reference 7–30 Hz filter, average-reference projection, all-EEG-channel selection, -1 to +4 second epochs, delayed classification window, `baseline=None`, CSP/LDA pipeline, and handling of concatenation boundaries.

[^widmann]: Widmann, A., Schröger, E., & Maess, B. (2015). Digital filter design for electrophysiological data — a practical approach. *Journal of Neuroscience Methods, 250*, 34–46. doi:10.1016/j.jneumeth.2014.08.002.

[^mne-filter]: MNE Developers. *Background information on filtering — MNE-Python documentation*. Used for filter-transition, phase, FIR, ringing, and time-frequency trade-off concepts.

[^mne-reference]: MNE Developers. *mne.set_eeg_reference — MNE-Python documentation*. Used for common-average referencing and `projection=True`.

[^mne-reference-tutorial]: MNE Developers. *Setting the EEG reference — MNE-Python documentation*. Used for behavior and advantages of average-reference projectors.

[^mne-epochs]: MNE Developers. *mne.Epochs / mne.BaseEpochs — MNE-Python documentation*. Used for epoch timing, inclusive endpoints, data shape, baseline correction, projection application, `reject`, and `flat`.

[^mne-erds]: MNE Developers. *Compute and visualize ERDS maps — MNE-Python documentation*. Used for motor-imagery ERD/ERS analysis and the -1 to 0 second power-reference example.

[^erd-baseline]: *Impact of the baseline temporal selection on the ERD/ERS analysis for Motor Imagery-based BCI*. Used for the importance of ERD/ERS baseline-window selection.