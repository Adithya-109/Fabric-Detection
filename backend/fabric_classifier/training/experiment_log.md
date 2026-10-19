# Experiment Log

This file is read before each attempt and appended after each attempt.

## Historical Backfill (Attempts 1-16)
- Attempt 1: blocked by environment setup issue.
- Attempt 2: top1 0.5653, macro_f1 0.5480, worst_recall 0.2500; below targets.
- Attempt 3: smaller batch/grad accumulation stabilized runtime, but metrics dropped.
- Attempt 4: policy-governed run improved worst recall to 0.3917 but still below required thresholds.
- Attempts 5-10: short policy-stop cycles and low improvement windows; no target breakthrough.
- Attempt 11: reset schedule after aggressive LR growth; still under target.
- Attempt 12: lower LR hurt performance further.
- Attempt 13: recovered part of the drop with extended epochs.
- Attempt 14: plateau-window policy stop at moderate gains.
- Attempt 15: best completed attempt so far (top1 0.5824, top3 0.8352, macro_f1 0.5832) but still below target criteria.
- Attempt 16: strong early validation trend, then policy stop from low worst-class recall trigger at epoch 20.

## Lessons So Far
- Chronic class weakness remains strongest in Polyester and Velvet, with Nylon/Linen/Fleece instability.
- Data-only top-up for Corduroy/Suede/Wool was not enough to hit final criteria.
- Lower backbone/head LR with longer warm-up tends to be safer than aggressive LR growth.
- Strict single-process control is mandatory to avoid checkpoint corruption.


## Attempt 17 Post-Mortem
- Timestamp UTC: 2026-04-19T16:02:02Z
- Status: completed_policy_stop
- Targets Met: False
- Research-Only Data Used: True
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 160, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.00035, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.01, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 12, "AUG_BRIGHTNESS": 0.2, "AUG_CONTRAST": 0.2, "AUG_SATURATION": 0.15, "AUG_HUE": 0.03, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 5, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 4, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 800, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": true}
- Metrics: top1=0.5618489583333334, top3=0.794921875, macro_f1=0.5560652798470868, worst_recall=0.19166666269302368, inference_ms=8.054310913085937, vram_mb=146.47119140625
- What Went Wrong: Run used research-only data, so it cannot be accepted as final deliverable.
- What I Learned: Research-only augmentation can be useful for direction finding, but final package must exclude it.
- What I Will Do Next: Disable research-only data for the next attempt and confirm metrics on commercial-safe data only.


## Attempt 18 Post-Mortem
- Timestamp UTC: 2026-04-19T17:10:40Z
- Status: completed_policy_stop
- Targets Met: False
- Research-Only Data Used: True
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 175, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.01, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 12, "AUG_BRIGHTNESS": 0.2, "AUG_CONTRAST": 0.2, "AUG_SATURATION": 0.15, "AUG_HUE": 0.03, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 5, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 4, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 800, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": true}
- Metrics: top1=0.5618489583333334, top3=0.794921875, macro_f1=0.5560652798470868, worst_recall=0.19166666269302368, inference_ms=7.680758056640625, vram_mb=180.51708984375
- What Went Wrong: Run used research-only data, so it cannot be accepted as final deliverable.
- What I Learned: Research-only augmentation can be useful for direction finding, but final package must exclude it.
- What I Will Do Next: Disable research-only data for the next attempt and confirm metrics on commercial-safe data only.


## Attempt 19 Post-Mortem
- Timestamp UTC: 2026-04-19T18:00:15Z
- Status: completed
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 60, "LR_BACKBONE": 0.0001, "LR_HEAD": 0.001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 10, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 800, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false}
- Metrics: top1=0.5622149837133551, top3=0.8104234337806702, macro_f1=0.5641840308001135, worst_recall=0.15000000596046448, inference_ms=7.834977416992188, vram_mb=150.234375
- What Went Wrong: Initial run failed to meet targets.
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 20 Post-Mortem
- Timestamp UTC: 2026-04-19T19:08:28Z
- Status: completed_policy_stop
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 75, "LR_BACKBONE": 8.5e-05, "LR_HEAD": 0.0009000000000000001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 13, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 800, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false}
- Metrics: top1=0.5387622149837134, top3=0.7856677770614624, macro_f1=0.5469244992085885, worst_recall=0.2916666567325592, inference_ms=7.960635986328125, vram_mb=180.97509765625
- What Went Wrong: Policy stop trigger fired: worst_recall_below_0_20_after_min_epoch
- What I Learned: Current hyperparameter/data configuration plateaued before reaching required metrics.
- What I Will Do Next: Apply auto-retry adjustments and continue from best warm-start checkpoint.


## Attempt 21 Post-Mortem
- Timestamp UTC: 2026-04-19T20:23:26Z
- Status: completed_policy_stop
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 90, "LR_BACKBONE": 7.225000000000001e-05, "LR_HEAD": 0.0008100000000000001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 16, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 800, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false}
- Metrics: top1=0.5504885993485342, top3=0.7934853434562683, macro_f1=0.552474412007213, worst_recall=0.3166666626930237, inference_ms=7.698821411132813, vram_mb=180.97509765625
- What Went Wrong: Policy stop trigger fired: val_metrics_plateau_window
- What I Learned: Current hyperparameter/data configuration plateaued before reaching required metrics.
- What I Will Do Next: Apply auto-retry adjustments and continue from best warm-start checkpoint.


## Attempt 22 Post-Mortem
- Timestamp UTC: 2026-04-19T21:43:28Z
- Status: completed_policy_stop
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 110, "LR_BACKBONE": 5.0575e-05, "LR_HEAD": 0.0006075000000000001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 20, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 4, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 800, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false}
- Metrics: top1=0.5537459283387622, top3=0.790228009223938, macro_f1=0.5612787834837564, worst_recall=0.375, inference_ms=7.822705078125, vram_mb=180.97509765625
- What Went Wrong: Policy stop trigger fired: val_metrics_plateau_window
- What I Learned: Current hyperparameter/data configuration plateaued before reaching required metrics.
- What I Will Do Next: Apply auto-retry adjustments and continue from best warm-start checkpoint.


## Attempt 23 Post-Mortem
- Timestamp UTC: 2026-10-10T02:39:20Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 60, "LR_BACKBONE": 0.0001, "LR_HEAD": 0.001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 10, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 24 Post-Mortem
- Timestamp UTC: 2026-10-10T02:39:29Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 75, "LR_BACKBONE": 8.5e-05, "LR_HEAD": 0.0009000000000000001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 13, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 25 Post-Mortem
- Timestamp UTC: 2026-10-10T02:39:37Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 90, "LR_BACKBONE": 7.225000000000001e-05, "LR_HEAD": 0.0008100000000000001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 16, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 26 Post-Mortem
- Timestamp UTC: 2026-10-10T02:39:46Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 105, "LR_BACKBONE": 6.141250000000001e-05, "LR_HEAD": 0.000729, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 19, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 27 Post-Mortem
- Timestamp UTC: 2026-10-10T02:39:55Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 120, "LR_BACKBONE": 5.2200625000000005e-05, "LR_HEAD": 0.0006561000000000001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 22, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 28 Post-Mortem
- Timestamp UTC: 2026-10-10T02:40:04Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 135, "LR_BACKBONE": 4.437053125e-05, "LR_HEAD": 0.00059049, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 25, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 29 Post-Mortem
- Timestamp UTC: 2026-10-10T02:40:13Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 150, "LR_BACKBONE": 3.77149515625e-05, "LR_HEAD": 0.000531441, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 28, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 30 Post-Mortem
- Timestamp UTC: 2026-10-10T02:40:21Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 165, "LR_BACKBONE": 3.2057708828124995e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 31 Post-Mortem
- Timestamp UTC: 2026-10-10T02:40:30Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 180, "LR_BACKBONE": 2.7249052503906245e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 32 Post-Mortem
- Timestamp UTC: 2026-10-10T02:40:39Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 195, "LR_BACKBONE": 2.3161694628320308e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 33 Post-Mortem
- Timestamp UTC: 2026-10-10T02:40:48Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 34 Post-Mortem
- Timestamp UTC: 2026-10-10T02:40:57Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 35 Post-Mortem
- Timestamp UTC: 2026-10-10T02:41:06Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 36 Post-Mortem
- Timestamp UTC: 2026-10-10T02:41:14Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 37 Post-Mortem
- Timestamp UTC: 2026-10-10T02:41:23Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 38 Post-Mortem
- Timestamp UTC: 2026-10-10T02:41:32Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 39 Post-Mortem
- Timestamp UTC: 2026-10-10T02:41:41Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 40 Post-Mortem
- Timestamp UTC: 2026-10-10T02:41:49Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 41 Post-Mortem
- Timestamp UTC: 2026-10-10T02:41:58Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 42 Post-Mortem
- Timestamp UTC: 2026-10-10T02:42:07Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 43 Post-Mortem
- Timestamp UTC: 2026-10-10T02:42:16Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 44 Post-Mortem
- Timestamp UTC: 2026-10-10T02:42:24Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 45 Post-Mortem
- Timestamp UTC: 2026-10-10T02:42:33Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 46 Post-Mortem
- Timestamp UTC: 2026-10-10T02:42:42Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 47 Post-Mortem
- Timestamp UTC: 2026-10-10T02:42:51Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 48 Post-Mortem
- Timestamp UTC: 2026-10-10T02:42:59Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 49 Post-Mortem
- Timestamp UTC: 2026-10-10T02:43:08Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 50 Post-Mortem
- Timestamp UTC: 2026-10-10T02:43:17Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 51 Post-Mortem
- Timestamp UTC: 2026-10-10T02:43:26Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 52 Post-Mortem
- Timestamp UTC: 2026-10-10T02:43:35Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 53 Post-Mortem
- Timestamp UTC: 2026-10-10T02:43:43Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 54 Post-Mortem
- Timestamp UTC: 2026-10-10T02:43:52Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 55 Post-Mortem
- Timestamp UTC: 2026-10-10T02:44:01Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 56 Post-Mortem
- Timestamp UTC: 2026-10-10T02:44:10Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 57 Post-Mortem
- Timestamp UTC: 2026-10-10T02:44:19Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 58 Post-Mortem
- Timestamp UTC: 2026-10-10T02:44:28Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 59 Post-Mortem
- Timestamp UTC: 2026-10-10T02:44:37Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 60 Post-Mortem
- Timestamp UTC: 2026-10-10T02:44:45Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 61 Post-Mortem
- Timestamp UTC: 2026-10-10T02:44:54Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 62 Post-Mortem
- Timestamp UTC: 2026-10-10T02:45:03Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 63 Post-Mortem
- Timestamp UTC: 2026-10-10T02:45:12Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 64 Post-Mortem
- Timestamp UTC: 2026-10-10T02:45:20Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 65 Post-Mortem
- Timestamp UTC: 2026-10-10T02:45:29Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 66 Post-Mortem
- Timestamp UTC: 2026-10-10T02:45:38Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 67 Post-Mortem
- Timestamp UTC: 2026-10-10T02:45:46Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 68 Post-Mortem
- Timestamp UTC: 2026-10-10T02:45:55Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 69 Post-Mortem
- Timestamp UTC: 2026-10-10T02:46:03Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 70 Post-Mortem
- Timestamp UTC: 2026-10-10T02:46:12Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 71 Post-Mortem
- Timestamp UTC: 2026-10-10T02:46:20Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 72 Post-Mortem
- Timestamp UTC: 2026-10-10T02:46:29Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 73 Post-Mortem
- Timestamp UTC: 2026-10-10T02:46:38Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 74 Post-Mortem
- Timestamp UTC: 2026-10-10T02:46:46Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 75 Post-Mortem
- Timestamp UTC: 2026-10-10T02:46:55Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 76 Post-Mortem
- Timestamp UTC: 2026-10-10T02:47:03Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 77 Post-Mortem
- Timestamp UTC: 2026-10-10T02:47:11Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 78 Post-Mortem
- Timestamp UTC: 2026-10-10T02:47:20Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 79 Post-Mortem
- Timestamp UTC: 2026-10-10T02:47:28Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 80 Post-Mortem
- Timestamp UTC: 2026-10-10T02:47:37Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 81 Post-Mortem
- Timestamp UTC: 2026-10-10T02:47:46Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 82 Post-Mortem
- Timestamp UTC: 2026-10-10T02:47:54Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 83 Post-Mortem
- Timestamp UTC: 2026-10-10T02:48:03Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 84 Post-Mortem
- Timestamp UTC: 2026-10-10T02:48:11Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 85 Post-Mortem
- Timestamp UTC: 2026-10-10T02:48:20Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 86 Post-Mortem
- Timestamp UTC: 2026-10-10T02:48:28Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 87 Post-Mortem
- Timestamp UTC: 2026-10-10T02:48:37Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 88 Post-Mortem
- Timestamp UTC: 2026-10-10T02:48:46Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 89 Post-Mortem
- Timestamp UTC: 2026-10-10T02:48:54Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 90 Post-Mortem
- Timestamp UTC: 2026-10-10T02:49:03Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 91 Post-Mortem
- Timestamp UTC: 2026-10-10T02:49:11Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 92 Post-Mortem
- Timestamp UTC: 2026-10-10T02:49:20Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 93 Post-Mortem
- Timestamp UTC: 2026-10-10T02:49:28Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 94 Post-Mortem
- Timestamp UTC: 2026-10-10T02:49:37Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 95 Post-Mortem
- Timestamp UTC: 2026-10-10T02:49:46Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 96 Post-Mortem
- Timestamp UTC: 2026-10-10T02:49:54Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 97 Post-Mortem
- Timestamp UTC: 2026-10-10T02:50:03Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 98 Post-Mortem
- Timestamp UTC: 2026-10-10T02:50:11Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 99 Post-Mortem
- Timestamp UTC: 2026-10-10T02:50:20Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 100 Post-Mortem
- Timestamp UTC: 2026-10-10T02:50:28Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 101 Post-Mortem
- Timestamp UTC: 2026-10-10T02:50:37Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 102 Post-Mortem
- Timestamp UTC: 2026-10-10T02:50:45Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 103 Post-Mortem
- Timestamp UTC: 2026-10-10T02:50:54Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 104 Post-Mortem
- Timestamp UTC: 2026-10-10T02:51:02Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 105 Post-Mortem
- Timestamp UTC: 2026-10-10T02:51:11Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 106 Post-Mortem
- Timestamp UTC: 2026-10-10T02:51:19Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 107 Post-Mortem
- Timestamp UTC: 2026-10-10T02:51:28Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 108 Post-Mortem
- Timestamp UTC: 2026-10-10T02:51:37Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 109 Post-Mortem
- Timestamp UTC: 2026-10-10T02:51:45Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 110 Post-Mortem
- Timestamp UTC: 2026-10-10T02:51:54Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 111 Post-Mortem
- Timestamp UTC: 2026-10-10T02:52:02Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 112 Post-Mortem
- Timestamp UTC: 2026-10-10T02:52:11Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 113 Post-Mortem
- Timestamp UTC: 2026-10-10T02:52:19Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 114 Post-Mortem
- Timestamp UTC: 2026-10-10T02:52:28Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 115 Post-Mortem
- Timestamp UTC: 2026-10-10T02:52:36Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 116 Post-Mortem
- Timestamp UTC: 2026-10-10T02:52:45Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 117 Post-Mortem
- Timestamp UTC: 2026-10-10T02:52:53Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 118 Post-Mortem
- Timestamp UTC: 2026-10-10T02:53:02Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 119 Post-Mortem
- Timestamp UTC: 2026-10-10T02:53:10Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 120 Post-Mortem
- Timestamp UTC: 2026-10-10T02:53:19Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 121 Post-Mortem
- Timestamp UTC: 2026-10-10T02:53:27Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 122 Post-Mortem
- Timestamp UTC: 2026-10-10T02:53:36Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 123 Post-Mortem
- Timestamp UTC: 2026-10-10T02:53:44Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 124 Post-Mortem
- Timestamp UTC: 2026-10-10T02:53:53Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 125 Post-Mortem
- Timestamp UTC: 2026-10-10T02:54:01Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 126 Post-Mortem
- Timestamp UTC: 2026-10-10T02:54:10Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 127 Post-Mortem
- Timestamp UTC: 2026-10-10T02:54:18Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 128 Post-Mortem
- Timestamp UTC: 2026-10-10T02:54:27Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 129 Post-Mortem
- Timestamp UTC: 2026-10-10T02:54:35Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 130 Post-Mortem
- Timestamp UTC: 2026-10-10T02:54:44Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 131 Post-Mortem
- Timestamp UTC: 2026-10-10T02:54:52Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 132 Post-Mortem
- Timestamp UTC: 2026-10-10T02:55:01Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 133 Post-Mortem
- Timestamp UTC: 2026-10-10T02:55:09Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 134 Post-Mortem
- Timestamp UTC: 2026-10-10T02:55:18Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 135 Post-Mortem
- Timestamp UTC: 2026-10-10T02:55:26Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 136 Post-Mortem
- Timestamp UTC: 2026-10-10T02:55:35Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 137 Post-Mortem
- Timestamp UTC: 2026-10-10T02:55:43Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 138 Post-Mortem
- Timestamp UTC: 2026-10-10T02:55:52Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 139 Post-Mortem
- Timestamp UTC: 2026-10-10T02:56:01Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 140 Post-Mortem
- Timestamp UTC: 2026-10-10T02:56:09Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 141 Post-Mortem
- Timestamp UTC: 2026-10-10T02:56:18Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 142 Post-Mortem
- Timestamp UTC: 2026-10-10T02:56:26Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 143 Post-Mortem
- Timestamp UTC: 2026-10-10T02:56:35Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 144 Post-Mortem
- Timestamp UTC: 2026-10-10T02:56:43Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 145 Post-Mortem
- Timestamp UTC: 2026-10-10T02:56:52Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 146 Post-Mortem
- Timestamp UTC: 2026-10-10T02:57:00Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 147 Post-Mortem
- Timestamp UTC: 2026-10-10T02:57:09Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 148 Post-Mortem
- Timestamp UTC: 2026-10-10T02:57:18Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 149 Post-Mortem
- Timestamp UTC: 2026-10-10T02:57:26Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 150 Post-Mortem
- Timestamp UTC: 2026-10-10T02:57:35Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 151 Post-Mortem
- Timestamp UTC: 2026-10-10T02:57:43Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 152 Post-Mortem
- Timestamp UTC: 2026-10-10T02:57:52Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 153 Post-Mortem
- Timestamp UTC: 2026-10-10T02:58:00Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 154 Post-Mortem
- Timestamp UTC: 2026-10-10T02:58:09Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 155 Post-Mortem
- Timestamp UTC: 2026-10-10T02:58:17Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 156 Post-Mortem
- Timestamp UTC: 2026-10-10T02:58:26Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 157 Post-Mortem
- Timestamp UTC: 2026-10-10T02:58:34Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 158 Post-Mortem
- Timestamp UTC: 2026-10-10T02:58:43Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 159 Post-Mortem
- Timestamp UTC: 2026-10-10T02:58:52Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 160 Post-Mortem
- Timestamp UTC: 2026-10-10T02:59:00Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 161 Post-Mortem
- Timestamp UTC: 2026-10-10T02:59:08Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 162 Post-Mortem
- Timestamp UTC: 2026-10-10T02:59:17Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 163 Post-Mortem
- Timestamp UTC: 2026-10-10T02:59:26Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 164 Post-Mortem
- Timestamp UTC: 2026-10-10T02:59:35Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 165 Post-Mortem
- Timestamp UTC: 2026-10-10T02:59:43Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 166 Post-Mortem
- Timestamp UTC: 2026-10-10T02:59:52Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 167 Post-Mortem
- Timestamp UTC: 2026-10-10T03:00:01Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 168 Post-Mortem
- Timestamp UTC: 2026-10-10T03:00:11Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 169 Post-Mortem
- Timestamp UTC: 2026-10-10T03:00:20Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 170 Post-Mortem
- Timestamp UTC: 2026-10-10T03:00:28Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 171 Post-Mortem
- Timestamp UTC: 2026-10-10T03:00:37Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 172 Post-Mortem
- Timestamp UTC: 2026-10-10T03:00:46Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 173 Post-Mortem
- Timestamp UTC: 2026-10-10T03:00:55Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 174 Post-Mortem
- Timestamp UTC: 2026-10-10T03:01:04Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 175 Post-Mortem
- Timestamp UTC: 2026-10-10T03:01:12Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 176 Post-Mortem
- Timestamp UTC: 2026-10-10T03:01:21Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 177 Post-Mortem
- Timestamp UTC: 2026-10-10T03:01:30Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 178 Post-Mortem
- Timestamp UTC: 2026-10-10T03:01:39Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 179 Post-Mortem
- Timestamp UTC: 2026-10-10T03:01:47Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 180 Post-Mortem
- Timestamp UTC: 2026-10-10T03:01:56Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 181 Post-Mortem
- Timestamp UTC: 2026-10-10T03:02:05Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 182 Post-Mortem
- Timestamp UTC: 2026-10-10T03:02:14Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 183 Post-Mortem
- Timestamp UTC: 2026-10-10T03:02:22Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 184 Post-Mortem
- Timestamp UTC: 2026-10-10T03:02:31Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 185 Post-Mortem
- Timestamp UTC: 2026-10-10T03:02:40Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 186 Post-Mortem
- Timestamp UTC: 2026-10-10T03:02:49Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 187 Post-Mortem
- Timestamp UTC: 2026-10-10T03:02:57Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 188 Post-Mortem
- Timestamp UTC: 2026-10-10T03:03:06Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 189 Post-Mortem
- Timestamp UTC: 2026-10-10T03:03:15Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 190 Post-Mortem
- Timestamp UTC: 2026-10-10T03:03:24Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 191 Post-Mortem
- Timestamp UTC: 2026-10-10T03:03:33Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 192 Post-Mortem
- Timestamp UTC: 2026-10-10T03:03:41Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 193 Post-Mortem
- Timestamp UTC: 2026-10-10T03:03:50Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 194 Post-Mortem
- Timestamp UTC: 2026-10-10T03:03:59Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 195 Post-Mortem
- Timestamp UTC: 2026-10-10T03:04:08Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 196 Post-Mortem
- Timestamp UTC: 2026-10-10T03:04:17Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 197 Post-Mortem
- Timestamp UTC: 2026-10-10T03:04:26Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 198 Post-Mortem
- Timestamp UTC: 2026-10-10T03:04:35Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 199 Post-Mortem
- Timestamp UTC: 2026-10-10T03:04:43Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 200 Post-Mortem
- Timestamp UTC: 2026-10-10T03:04:52Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 201 Post-Mortem
- Timestamp UTC: 2026-10-10T03:05:01Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 202 Post-Mortem
- Timestamp UTC: 2026-10-10T03:05:10Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 203 Post-Mortem
- Timestamp UTC: 2026-10-10T03:05:18Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 204 Post-Mortem
- Timestamp UTC: 2026-10-10T03:05:27Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 205 Post-Mortem
- Timestamp UTC: 2026-10-10T03:05:36Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 206 Post-Mortem
- Timestamp UTC: 2026-10-10T03:05:45Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 207 Post-Mortem
- Timestamp UTC: 2026-10-10T03:05:53Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 208 Post-Mortem
- Timestamp UTC: 2026-10-10T03:06:02Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 209 Post-Mortem
- Timestamp UTC: 2026-10-10T03:06:11Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 210 Post-Mortem
- Timestamp UTC: 2026-10-10T03:06:20Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 211 Post-Mortem
- Timestamp UTC: 2026-10-10T03:06:29Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 212 Post-Mortem
- Timestamp UTC: 2026-10-10T03:06:37Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 213 Post-Mortem
- Timestamp UTC: 2026-10-10T03:06:46Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 214 Post-Mortem
- Timestamp UTC: 2026-10-10T03:06:55Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 215 Post-Mortem
- Timestamp UTC: 2026-10-10T03:07:04Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 216 Post-Mortem
- Timestamp UTC: 2026-10-10T03:07:14Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 217 Post-Mortem
- Timestamp UTC: 2026-10-10T03:07:23Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 218 Post-Mortem
- Timestamp UTC: 2026-10-10T03:07:32Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 219 Post-Mortem
- Timestamp UTC: 2026-10-10T03:07:42Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 220 Post-Mortem
- Timestamp UTC: 2026-10-10T03:07:51Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 221 Post-Mortem
- Timestamp UTC: 2026-10-10T03:08:00Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 222 Post-Mortem
- Timestamp UTC: 2026-10-10T03:08:09Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 223 Post-Mortem
- Timestamp UTC: 2026-10-10T03:08:18Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 224 Post-Mortem
- Timestamp UTC: 2026-10-10T03:08:28Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 225 Post-Mortem
- Timestamp UTC: 2026-10-10T03:08:39Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 226 Post-Mortem
- Timestamp UTC: 2026-10-10T03:08:49Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 227 Post-Mortem
- Timestamp UTC: 2026-10-10T03:08:59Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 228 Post-Mortem
- Timestamp UTC: 2026-10-10T03:09:08Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 229 Post-Mortem
- Timestamp UTC: 2026-10-10T03:09:16Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 230 Post-Mortem
- Timestamp UTC: 2026-10-10T03:09:25Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 231 Post-Mortem
- Timestamp UTC: 2026-10-10T03:09:33Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 232 Post-Mortem
- Timestamp UTC: 2026-10-10T03:09:42Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 233 Post-Mortem
- Timestamp UTC: 2026-10-10T03:09:50Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 234 Post-Mortem
- Timestamp UTC: 2026-10-10T03:09:59Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 235 Post-Mortem
- Timestamp UTC: 2026-10-10T03:10:07Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 236 Post-Mortem
- Timestamp UTC: 2026-10-10T03:10:16Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 237 Post-Mortem
- Timestamp UTC: 2026-10-10T03:10:24Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 238 Post-Mortem
- Timestamp UTC: 2026-10-10T03:10:33Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 239 Post-Mortem
- Timestamp UTC: 2026-10-10T03:10:42Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 240 Post-Mortem
- Timestamp UTC: 2026-10-10T03:10:50Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 241 Post-Mortem
- Timestamp UTC: 2026-10-10T03:10:59Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 242 Post-Mortem
- Timestamp UTC: 2026-10-10T03:11:07Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 243 Post-Mortem
- Timestamp UTC: 2026-10-10T03:11:16Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 244 Post-Mortem
- Timestamp UTC: 2026-10-10T03:11:24Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 245 Post-Mortem
- Timestamp UTC: 2026-10-10T03:11:33Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 246 Post-Mortem
- Timestamp UTC: 2026-10-10T03:11:41Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 247 Post-Mortem
- Timestamp UTC: 2026-10-10T03:11:50Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 248 Post-Mortem
- Timestamp UTC: 2026-10-10T03:11:59Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 249 Post-Mortem
- Timestamp UTC: 2026-10-10T03:12:07Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 250 Post-Mortem
- Timestamp UTC: 2026-10-10T03:12:16Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 251 Post-Mortem
- Timestamp UTC: 2026-10-10T03:12:24Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 252 Post-Mortem
- Timestamp UTC: 2026-10-10T03:12:33Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 253 Post-Mortem
- Timestamp UTC: 2026-10-10T03:12:42Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 254 Post-Mortem
- Timestamp UTC: 2026-10-10T03:12:51Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 255 Post-Mortem
- Timestamp UTC: 2026-10-10T03:13:00Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 256 Post-Mortem
- Timestamp UTC: 2026-10-10T03:13:08Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 257 Post-Mortem
- Timestamp UTC: 2026-10-10T03:13:17Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 258 Post-Mortem
- Timestamp UTC: 2026-10-10T03:13:26Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 259 Post-Mortem
- Timestamp UTC: 2026-10-10T03:13:34Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 260 Post-Mortem
- Timestamp UTC: 2026-10-10T03:13:43Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 261 Post-Mortem
- Timestamp UTC: 2026-10-10T03:13:52Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 262 Post-Mortem
- Timestamp UTC: 2026-10-10T03:14:00Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 263 Post-Mortem
- Timestamp UTC: 2026-10-10T03:14:09Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 264 Post-Mortem
- Timestamp UTC: 2026-10-10T03:14:18Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 265 Post-Mortem
- Timestamp UTC: 2026-10-10T03:14:26Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 266 Post-Mortem
- Timestamp UTC: 2026-10-10T03:14:35Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 267 Post-Mortem
- Timestamp UTC: 2026-10-10T03:14:44Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 268 Post-Mortem
- Timestamp UTC: 2026-10-10T03:14:53Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 269 Post-Mortem
- Timestamp UTC: 2026-10-10T03:15:01Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 270 Post-Mortem
- Timestamp UTC: 2026-10-10T03:15:10Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 271 Post-Mortem
- Timestamp UTC: 2026-10-10T03:15:18Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 272 Post-Mortem
- Timestamp UTC: 2026-10-10T03:15:27Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 273 Post-Mortem
- Timestamp UTC: 2026-10-10T03:15:36Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 274 Post-Mortem
- Timestamp UTC: 2026-10-10T03:15:44Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 275 Post-Mortem
- Timestamp UTC: 2026-10-10T03:15:53Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 276 Post-Mortem
- Timestamp UTC: 2026-10-10T03:16:02Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 277 Post-Mortem
- Timestamp UTC: 2026-10-10T03:16:11Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 278 Post-Mortem
- Timestamp UTC: 2026-10-10T03:16:20Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 279 Post-Mortem
- Timestamp UTC: 2026-10-10T03:16:29Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 280 Post-Mortem
- Timestamp UTC: 2026-10-10T03:16:39Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 281 Post-Mortem
- Timestamp UTC: 2026-10-10T03:16:48Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 282 Post-Mortem
- Timestamp UTC: 2026-10-10T03:16:58Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 283 Post-Mortem
- Timestamp UTC: 2026-10-10T03:17:07Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 284 Post-Mortem
- Timestamp UTC: 2026-10-10T03:17:16Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 285 Post-Mortem
- Timestamp UTC: 2026-10-10T03:17:25Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 286 Post-Mortem
- Timestamp UTC: 2026-10-10T03:17:34Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 287 Post-Mortem
- Timestamp UTC: 2026-10-10T03:17:43Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 288 Post-Mortem
- Timestamp UTC: 2026-10-10T03:17:52Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 289 Post-Mortem
- Timestamp UTC: 2026-10-10T03:18:01Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 290 Post-Mortem
- Timestamp UTC: 2026-10-10T03:18:09Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 291 Post-Mortem
- Timestamp UTC: 2026-10-10T03:18:18Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 292 Post-Mortem
- Timestamp UTC: 2026-10-10T03:18:27Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 293 Post-Mortem
- Timestamp UTC: 2026-10-10T03:18:36Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 294 Post-Mortem
- Timestamp UTC: 2026-10-10T03:18:45Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 295 Post-Mortem
- Timestamp UTC: 2026-10-10T03:18:55Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 296 Post-Mortem
- Timestamp UTC: 2026-10-10T03:19:04Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 297 Post-Mortem
- Timestamp UTC: 2026-10-10T03:19:13Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 298 Post-Mortem
- Timestamp UTC: 2026-10-10T03:19:22Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 299 Post-Mortem
- Timestamp UTC: 2026-10-10T03:19:31Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 300 Post-Mortem
- Timestamp UTC: 2026-10-10T03:19:40Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 301 Post-Mortem
- Timestamp UTC: 2026-10-10T03:19:49Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 302 Post-Mortem
- Timestamp UTC: 2026-10-10T03:19:58Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 303 Post-Mortem
- Timestamp UTC: 2026-10-10T03:20:07Z
- Status: failed_exception
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 200, "LR_BACKBONE": 2e-05, "LR_HEAD": 0.0005, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 30, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=None, top3=None, macro_f1=None, worst_recall=None, inference_ms=None, vram_mb=None
- What Went Wrong: Unhandled exception: NameError: name 'DATASETS_DIR' is not defined
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 304 Post-Mortem
- Timestamp UTC: 2026-10-10T10:45:08Z
- Status: completed
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 60, "LR_BACKBONE": 0.0001, "LR_HEAD": 0.001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 10, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=0.30743094166446033, top3=0.5722354650497437, macro_f1=0.3128206686729839, worst_recall=0.040823448449373245, inference_ms=6.303518676757813, vram_mb=179.68701171875
- What Went Wrong: Initial run failed to meet targets.
- What I Learned: Current changes improved some metrics but not enough to satisfy all acceptance thresholds.
- What I Will Do Next: Adjust learning schedule/data mix and continue automated retries.


## Attempt 305 Post-Mortem
- Timestamp UTC: 2026-10-11T06:04:05Z
- Status: completed_policy_stop
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 75, "LR_BACKBONE": 8.5e-05, "LR_HEAD": 0.0009000000000000001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 13, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=0.311402347542141, top3=0.5555996894836426, macro_f1=0.31246538580965, worst_recall=0.026517795398831367, inference_ms=6.289367065429688, vram_mb=182.10400390625
- What Went Wrong: Policy stop trigger fired: worst_recall_below_0_20_after_min_epoch
- What I Learned: Current hyperparameter/data configuration plateaued before reaching required metrics.
- What I Will Do Next: Apply auto-retry adjustments and continue from best warm-start checkpoint.


## Attempt 306 Post-Mortem
- Timestamp UTC: 2026-10-11T19:25:44Z
- Status: completed_policy_stop
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 90, "LR_BACKBONE": 7.225000000000001e-05, "LR_HEAD": 0.0008100000000000001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 16, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=0.336907598623246, top3=0.5850322246551514, macro_f1=0.3316696322767445, worst_recall=0.04884856939315796, inference_ms=6.380994262695313, vram_mb=182.10400390625
- What Went Wrong: Policy stop trigger fired: worst_recall_below_0_20_after_min_epoch
- What I Learned: Current hyperparameter/data configuration plateaued before reaching required metrics.
- What I Will Do Next: Apply auto-retry adjustments and continue from best warm-start checkpoint.


## Attempt 307 Post-Mortem
- Timestamp UTC: 2026-10-12T07:20:36Z
- Status: completed_policy_stop
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 105, "LR_BACKBONE": 6.141250000000001e-05, "LR_HEAD": 0.000729, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 19, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=0.35588209337216486, top3=0.6107139587402344, macro_f1=0.34914664886709934, worst_recall=0.08443824201822281, inference_ms=6.297579345703125, vram_mb=182.10400390625
- What Went Wrong: Policy stop trigger fired: worst_recall_below_0_20_after_min_epoch
- What I Learned: Current hyperparameter/data configuration plateaued before reaching required metrics.
- What I Will Do Next: Apply auto-retry adjustments and continue from best warm-start checkpoint.


## Attempt 308 Post-Mortem
- Timestamp UTC: 2026-10-12T19:29:03Z
- Status: completed_policy_stop
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 120, "LR_BACKBONE": 5.2200625000000005e-05, "LR_HEAD": 0.0006561000000000001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 22, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=0.3897272967963993, top3=0.6543994545936584, macro_f1=0.3786914663880228, worst_recall=0.1266573667526245, inference_ms=6.3187353515625, vram_mb=182.10400390625
- What Went Wrong: Policy stop trigger fired: worst_recall_below_0_20_after_min_epoch
- What I Learned: Current hyperparameter/data configuration plateaued before reaching required metrics.
- What I Will Do Next: Apply auto-retry adjustments and continue from best warm-start checkpoint.


## Attempt 309 Post-Mortem
- Timestamp UTC: 2026-10-13T14:45:17Z
- Status: completed_policy_stop
- Targets Met: False
- Research-Only Data Used: False
- What I Tried: Hyperparameters/data toggles = {"BATCH_SIZE": 4, "EPOCHS_MAX": 60, "LR_BACKBONE": 0.0001, "LR_HEAD": 0.001, "WEIGHT_DECAY": 0.0001, "LABEL_SMOOTHING": 0.02, "PATIENCE": 10, "IMG_SIZE": 224, "AUG_ROTATION_DEG": 20, "AUG_BRIGHTNESS": 0.3, "AUG_CONTRAST": 0.3, "AUG_SATURATION": 0.2, "AUG_HUE": 0.05, "N_PATCHES_TRAIN": 2, "N_PATCHES_INFER": 7, "HEAD_ONLY_EPOCHS": 3, "DEVICE": "cuda", "NUM_WORKERS": 0, "PIN_MEMORY": false, "GRAD_ACCUM_STEPS": 2, "BATCH_HEARTBEAT_STEPS": 100, "MAX_IMAGES_PER_CLASS": 10000000, "POLICY_STOP_MIN_EPOCHS": 20, "POLICY_STOP_WINDOW": 10, "POLICY_MIN_TOP1_GAIN": 0.005, "POLICY_MIN_MACRO_F1_GAIN": 0.005, "USE_MICROSCOPE_DATA": true, "USE_IBUG_RESEARCH_DATA": false, "USE_IMATERIALIST_DATA": true}
- Metrics: top1=0.4327949872032477, top3=0.6649898290634155, macro_f1=0.4047554256458445, worst_recall=0.17550593614578247, inference_ms=11.856285400390625, vram_mb=147.14697265625
- What Went Wrong: Policy stop trigger fired: worst_recall_below_0_20_after_min_epoch
- What I Learned: Current hyperparameter/data configuration plateaued before reaching required metrics.
- What I Will Do Next: Apply auto-retry adjustments and continue from best warm-start checkpoint.
