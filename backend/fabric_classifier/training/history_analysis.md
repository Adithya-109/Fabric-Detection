# History Analysis

## Attempt Summary
| attempt | status | targets_met | top1 | top3 | macro_f1 | worst_recall | inference_ms | vram_mb | reason_for_retry |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Blocked | False | N/A | N/A | N/A | N/A | N/A | N/A |  |
| 2 | completed | False | 0.5653 | 0.7990 | 0.5480 | 0.2500 | 55.2100 | 139.8696 | Initial run failed to meet targets. |
| 3 | completed | False | 0.5228 | 0.7650 | 0.5127 | 0.2419 | 9.8947 | 150.5601 | Initial run failed to meet targets. |
| 4 | completed_with_policy_stop | False | 0.5576 | 0.8032 | 0.5449 | 0.3917 | N/A | N/A | Mandatory governance stop and diagnostics before next attempt. |
| 5 | completed_policy_stop | False | 0.5067 | 0.7724 | 0.5181 | 0.3423 | 8.1756 | 180.1597 | Policy stop trigger: {'rule': 'val_top1_5_epoch_improvement_below_0_01', 'start_epoch': 1, 'end_epoch': 5, 'improvement': 0.0013395847287340779, 'threshold': 0.01} |
| 6 | completed_policy_stop | False | 0.4946 | 0.7534 | 0.5028 | 0.3084 | 8.6360 | 179.6870 | Policy stop trigger: {'rule': 'val_top1_5_epoch_improvement_below_0_01', 'start_epoch': 2, 'end_epoch': 6, 'improvement': -0.03817314246762099, 'threshold': 0.01} |
| 7 | completed_policy_stop | False | 0.5026 | 0.7549 | 0.5016 | 0.2632 | 32.2063 | 180.8354 | Policy stop trigger: {'rule': 'val_top1_5_epoch_improvement_below_0_01', 'start_epoch': 1, 'end_epoch': 5, 'improvement': -0.011795543905635641, 'threshold': 0.01} |
| 8 | completed_policy_stop | False | 0.5490 | 0.7890 | 0.5449 | 0.1930 | 7.4299 | 180.2651 | Policy stop trigger: {'rule': 'val_top1_5_epoch_improvement_below_0_01', 'start_epoch': 1, 'end_epoch': 5, 'improvement': -0.01905387647831802, 'threshold': 0.01} |
| 9 | completed_policy_stop | False | 0.5433 | 0.7785 | 0.5418 | 0.2193 | 7.3824 | 181.5659 | Policy stop trigger: {'rule': 'val_top1_5_epoch_improvement_below_0_01', 'start_epoch': 1, 'end_epoch': 5, 'improvement': -0.03803278688524592, 'threshold': 0.01} |
| 10 | completed_policy_stop | False | 0.5220 | 0.7873 | 0.5186 | 0.1858 | 8.2593 | 180.2651 | Policy stop trigger: {'rule': 'val_top1_5_epoch_improvement_below_0_01', 'start_epoch': 1, 'end_epoch': 5, 'improvement': -0.03873933026920556, 'threshold': 0.01} |
| 11 | completed | False | 0.5182 | 0.7786 | 0.5161 | 0.2250 | 28.9187 | 150.7168 | Initial run failed to meet targets. |
| 12 | completed | False | 0.4928 | 0.7614 | 0.4903 | 0.1833 | 29.0943 | 180.6558 | Initial run failed to meet targets. |
| 13 | completed | False | 0.5391 | 0.7842 | 0.5362 | 0.2583 | 19.9620 | 180.9722 | Initial run failed to meet targets. |
| 14 | completed_policy_stop | False | 0.5420 | 0.7811 | 0.5386 | 0.2750 | 8.8497 | 181.9097 | Policy stop trigger: {'rule': 'val_metrics_plateau_window', 'start_epoch': 11, 'end_epoch': 20, 'top1_window_gain': -0.0013029315960911836, 'macro_f1_window_gain': 0.00050125179586 |
| 15 | completed_policy_stop | False | 0.5824 | 0.8352 | 0.5832 | 0.3250 | 9.8528 | 181.9097 | Policy stop trigger: {'rule': 'val_metrics_plateau_window', 'start_epoch': 11, 'end_epoch': 20, 'top1_window_gain': -0.008474576271186529, 'macro_f1_window_gain': -0.00234737301988 |
| 16 | completed_policy_stop | False | 0.5750 | 0.8201 | 0.5742 | 0.3000 | 9.3728 | 147.1470 | Policy stop trigger: {'rule': 'worst_recall_below_0_20_after_min_epoch', 'epoch': 20, 'value': 0.19166666269302368, 'threshold': 0.2} |

## Epoch Progress Diagnostics
| attempt | max_epoch | eval_rows | best_val_top1 | best_val_top3 | best_val_macro_f1 | best_val_worst_recall | policy_stop_triggers |
|---|---|---|---|---|---|---|---|
| 3 | 57 | 51 | 0.5316 | 0.7655 | 0.5273 | 0.3333 | 0 |
| 4 | 30 | 30 | 0.5160 | 0.7609 | 0.5120 | 0.3443 | 0 |
| 5 | 5 | 5 | 0.5385 | 0.7816 | 0.5317 | 0.3333 | 1 |
| 6 | 6 | 6 | 0.5235 | 0.7805 | 0.5183 | 0.3421 | 1 |
| 7 | 5 | 5 | 0.5446 | 0.7982 | 0.5417 | 0.2783 | 1 |
| 8 | 5 | 5 | 0.5296 | 0.7898 | 0.5307 | 0.3426 | 1 |
| 9 | 5 | 5 | 0.5102 | 0.7731 | 0.5066 | 0.2105 | 1 |
| 10 | 5 | 5 | 0.4990 | 0.7466 | 0.4921 | 0.2281 | 1 |
| 11 | 10 | 10 | 0.4971 | 0.7479 | 0.4884 | 0.2000 | 0 |
| 12 | 13 | 13 | 0.5176 | 0.7679 | 0.5139 | 0.2583 | 0 |
| 13 | 16 | 16 | 0.5280 | 0.7849 | 0.5172 | 0.1917 | 0 |
| 14 | 20 | 20 | 0.5759 | 0.8013 | 0.5723 | 0.2750 | 1 |
| 15 | 20 | 20 | 0.5802 | 0.8083 | 0.5788 | 0.3583 | 1 |
| 16 | 20 | 20 | 0.6151 | 0.8454 | 0.6125 | 0.3083 | 1 |
| 17 | 19 | 19 | 0.6265 | 0.8452 | 0.6231 | 0.2917 | 0 |

## Chronic Class Weakness
| class | mean_recall | min_recall | max_recall | attempts_recall_lt_0_40 | attempts_represented |
|---|---|---|---|---|---|
| Polyester | 0.2870 | 0.1833 | 0.4083 | 14 | 15 |
| Velvet | 0.3928 | 0.2895 | 0.5500 | 9 | 15 |
| Nylon | 0.4567 | 0.2833 | 0.6833 | 6 | 15 |
| Linen | 0.4709 | 0.3084 | 0.5854 | 2 | 15 |
| Fleece | 0.4778 | 0.2750 | 0.6333 | 3 | 15 |
| Cotton | 0.5182 | 0.3423 | 0.6216 | 2 | 15 |
| Knitted | 0.5263 | 0.3667 | 0.6917 | 1 | 15 |
| Satin | 0.5551 | 0.4667 | 0.6250 | 0 | 15 |
| Silk | 0.5622 | 0.4083 | 0.6833 | 0 | 15 |
| Wool | 0.6081 | 0.5057 | 0.8046 | 0 | 15 |
| Leather | 0.6359 | 0.5385 | 0.7083 | 0 | 15 |
| Suede | 0.6924 | 0.2419 | 0.8621 | 1 | 15 |
| Denim | 0.7139 | 0.6250 | 0.8083 | 0 | 15 |
| Corduroy | 0.7553 | 0.6418 | 0.9107 | 0 | 15 |

## Hyperparameter Change Impact
| transition | major_param_changes | delta_top1 | delta_macro_f1 | delta_worst_recall |
|---|---|---|---|---|
| 1 -> 2 | BATCH_SIZE: None -> 32; DEVICE: None -> cuda; EPOCHS_MAX: None -> 60; HEAD_ONLY_EPOCHS: None -> 3; IMG_SIZE: None -> 224; LABEL_SMOOTHING: None -> 0.05; ... | N/A | N/A | N/A |
| 2 -> 3 | BATCH_SIZE: 32 -> 4; GRAD_ACCUM_STEPS: None -> 2; PIN_MEMORY: None -> False; RAM_HARD_LIMIT_PERCENT: None -> 75.0; RESOURCE_MANAGER_ENABLED: None -> True | -0.0425 | -0.0352 | -0.0081 |
| 3 -> 4 | BATCH_SIZE: 4 -> None; DEVICE: cuda -> None; EPOCHS_MAX: 60 -> None; GRAD_ACCUM_STEPS: 2 -> None; HEAD_ONLY_EPOCHS: 3 -> None; IMG_SIZE: 224 -> None; ... | 0.0348 | 0.0321 | 0.1497 |
| 4 -> 5 | BATCH_SIZE: None -> 4; DEVICE: None -> cuda; EPOCHS_MAX: None -> 60; GRAD_ACCUM_STEPS: None -> 2; HEAD_ONLY_EPOCHS: None -> 3; IMG_SIZE: None -> 224; ... | -0.0509 | -0.0268 | -0.0493 |
| 5 -> 6 | no changes | -0.0121 | -0.0152 | -0.0339 |
| 6 -> 7 | no changes | 0.0081 | -0.0012 | -0.0453 |
| 7 -> 8 | EPOCHS_MAX: 60 -> 85; LR_BACKBONE: 0.0001 -> 0.00012; LR_HEAD: 0.001 -> 0.00125; PATIENCE: 10 -> 13 | 0.0464 | 0.0433 | -0.0702 |
| 8 -> 9 | EPOCHS_MAX: 85 -> 110; LR_BACKBONE: 0.00012 -> 0.000144; LR_HEAD: 0.00125 -> 0.0015625; PATIENCE: 13 -> 16 | -0.0057 | -0.0031 | 0.0263 |
| 9 -> 10 | EPOCHS_MAX: 110 -> 135; LR_BACKBONE: 0.000144 -> 0.0001728; LR_HEAD: 0.0015625 -> 0.001953125; PATIENCE: 16 -> 19 | -0.0213 | -0.0232 | -0.0335 |
| 10 -> 11 | EPOCHS_MAX: 135 -> 60; LR_BACKBONE: 0.0001728 -> 0.0001; LR_HEAD: 0.001953125 -> 0.001; PATIENCE: 19 -> 10; POLICY_MIN_MACRO_F1_GAIN: None -> 0.005; POLICY_MIN_TOP1_GAIN: None -> 0.005; ... | -0.0038 | -0.0025 | 0.0392 |
| 11 -> 12 | EPOCHS_MAX: 60 -> 75; LR_BACKBONE: 0.0001 -> 8.5e-05; LR_HEAD: 0.001 -> 0.0009000000000000001; PATIENCE: 10 -> 13 | -0.0254 | -0.0258 | -0.0417 |
| 12 -> 13 | EPOCHS_MAX: 75 -> 90; LR_BACKBONE: 8.5e-05 -> 7.225000000000001e-05; LR_HEAD: 0.0009000000000000001 -> 0.0008100000000000001; PATIENCE: 13 -> 16 | 0.0463 | 0.0459 | 0.0750 |
| 13 -> 14 | EPOCHS_MAX: 90 -> 105; LR_BACKBONE: 7.225000000000001e-05 -> 6.141250000000001e-05; LR_HEAD: 0.0008100000000000001 -> 0.000729; PATIENCE: 16 -> 19 | 0.0029 | 0.0024 | 0.0167 |
| 14 -> 15 | EPOCHS_MAX: 105 -> 125; HEAD_ONLY_EPOCHS: 3 -> 4; LR_BACKBONE: 6.141250000000001e-05 -> 4.298875e-05; LR_HEAD: 0.000729 -> 0.00054675; PATIENCE: 19 -> 23 | 0.0404 | 0.0446 | 0.0500 |
| 15 -> 16 | BATCH_HEARTBEAT_STEPS: None -> 100; EPOCHS_MAX: 125 -> 60; HEAD_ONLY_EPOCHS: 4 -> 3; LR_BACKBONE: 4.298875e-05 -> 0.0001; LR_HEAD: 0.00054675 -> 0.001; PATIENCE: 23 -> 10 | -0.0074 | -0.0091 | -0.0250 |

## Issues Log Summary
- Category counts: {'data_download': 1, 'data_gate': 4, 'stabilization': 2, 'process_control': 1}
- Severity counts: {'high': 3, 'medium': 5}
- Status counts: {'open': 6, 'resolved': 2}

### Latest 10 Issues
| timestamp_utc | category | severity | title | action_taken | status |
|---|---|---|---|---|---|
| 2026-04-19T03:29:21Z | data_download | high | Targeted class download failed | Will continue with available data and re-check counts. | open |
| 2026-04-19T04:20:54Z | data_gate | medium | Attempt 17 targeted top-up yielded no valid-count gain | Stopped further targeted download rounds to avoid prolonged pre-launch delay. | open |
| 2026-04-19T04:20:54Z | data_gate | high | Attempt 17 targeted data gate result | Proceeding with next attempt using refreshed target-class data. | open |
| 2026-04-19T04:20:54Z | stabilization | medium | Attempt 17 stabilization profile applied | Applied lower-LR, higher-accumulation, and softer-augmentation settings for attempt 17. | resolved |
| 2026-04-19T05:15:35Z | data_gate | medium | Attempt 17 targeted top-up yielded no valid-count gain | Stopped further targeted download rounds to avoid prolonged pre-launch delay. | open |
| 2026-04-19T05:15:35Z | data_gate | high | Attempt 17 targeted data gate result | Proceeding with next attempt using refreshed target-class data. | open |
| 2026-04-19T05:15:35Z | stabilization | medium | Attempt 17 stabilization profile applied | Applied lower-LR, higher-accumulation, and softer-augmentation settings for attempt 17. | resolved |
| 2026-04-19T07:45:52Z | process_control | medium | Attempt 17 interrupted by user | Stopped current launch cleanly; checkpoint/log artifacts retained. | open |

## HANDOFF Constraints Digest
- `backend/fabric_classifier/training/PROCESS_CONTEXT.json`
- Active training process:
- PID: `17752`
- Command: `"C:\Users\A0SKZ\miniconda3\envs\myenv\python.exe" -u backend/fabric_classifier/training/train.py`
- Start time: `2026-04-18 07:22:40 local`
- Note: duplicate writer PID `4464` was terminated to stop concurrent checkpoint writes.
- Runtime control flags:
- `backend/fabric_classifier/training/runtime_control/training_active.flag`
- `backend/fabric_classifier/training/runtime_control/downloads_paused.flag`
- `downloads_paused.flag` currently indicates `attempt_4_epoch_28_start` (latest observed flag write).

## Implications For New Datasets
- Weak-class pressure is concentrated in: Polyester, Velvet, Nylon, Linen, Fleece
- Microscope images of fabric mapped target counts -> Cotton:295, Nylon:121, Silk:120, Satin:62, Knitted:61, Linen:60, Polyester:60, Velvet:54
- The Fabrics Dataset by iBUG mapped target counts -> Cotton:2352, Polyester:904, Denim:648, Wool:376, Silk:304, Nylon:228, Linen:224, Fleece:136, Velvet:96, Corduroy:96, Satin:96, Leather:76, Suede:20
- Microscope dataset contributes texture-only views and lacks full 14-class coverage; best used as targeted augmentation for mapped classes only.
- iBUG dataset is research-only licensed and can be used only for experimentation; final production weights must be retrained without iBUG samples.
- Given weak recalls in Polyester/Velvet/Nylon family classes, limited iBUG class additions likely help short-term recall but introduce domain/licensing debt.
