# Recalibration report

Weights: `fabric_clf_best.pt` (c8fa0616751bed94) · data: `data/external`

Settings chosen on `calib`; target class frequencies from: select-split.

Before = the model as it is today (argmax, no correction).

## Recalibration on calib (5235 images)

Settings: prior-correction strength **0.6**, temperature **10**

| Metric | Before | After | Change |
|---|---|---|---|
| Top-1 | 2.0% | 44.9% | +42.9 pts |
| Top-3 | 5.9% | 90.2% | +84.4 pts |
| Macro-F1 | 5.1% | 4.8% | -0.4 pts |
| Balanced acc. | 21.2% | 7.6% | -13.5 pts |
| Worst-class recall | 0.0% | 0.0% | -0.0 pts |
| Calibration error (ECE, lower is better) | 35.6% | 4.6% | -31.0 pts |

| Class | Recall before → after | Precision before → after | Images |
|---|---|---|---|
| Cotton | 0.0% → 99.3% | 50.0% → 45.2% | 2368 |
| Polyester | 0.3% → 0.0% | 75.0% → 14.3% | 2213 |
| Silk | 16.4% → 0.0% | 4.8% → 0.0% | 140 |
| Denim | 5.6% → 0.0% | 1.5% → 0.0% | 18 |
| Linen | 37.5% → 0.0% | 3.5% → 0.0% | 64 |
| Wool | 6.1% → 0.0% | 9.2% → 0.0% | 131 |
| Leather | 57.9% → 0.0% | 16.2% → 0.0% | 19 |
| Velvet | 8.3% → 0.0% | 0.3% → 0.0% | 12 |
| Corduroy | 75.0% → 0.0% | 0.1% → 0.0% | 4 |
| Fleece | 11.6% → 0.0% | 7.9% → 0.0% | 86 |
| Nylon | 11.3% → 0.0% | 2.1% → 0.0% | 133 |
| Satin | 2.5% → 0.0% | 2.2% → 0.0% | 40 |
| Knitted | 0.0% → 0.0% | 0.0% → 0.0% | 0 |
| Suede | 42.9% → 0.0% | 0.6% → 0.0% | 7 |

## Recalibration on eval (2931 images)

Settings: prior-correction strength **0.6**, temperature **10**

| Metric | Before | After | Change |
|---|---|---|---|
| Top-1 | 1.2% | 68.9% | +67.7 pts |
| Top-3 | 2.9% | 94.8% | +91.9 pts |
| Macro-F1 | 3.1% | 6.3% | +3.2 pts |
| Balanced acc. | 21.9% | 7.7% | -14.2 pts |
| Worst-class recall | 0.0% | 0.0% | +0.0 pts |
| Calibration error (ECE, lower is better) | 34.3% | 19.5% | -14.7 pts |

| Class | Recall before → after | Precision before → after | Images |
|---|---|---|---|
| Cotton | 0.0% → 100.0% | 0.0% → 69.0% | 2020 |
| Polyester | 0.0% → 0.1% | 0.0% → 50.0% | 728 |
| Silk | 16.3% → 0.0% | 4.8% → 0.0% | 43 |
| Denim | 0.0% → 0.0% | 0.0% → 0.0% | 7 |
| Linen | 40.0% → 0.0% | 1.6% → 0.0% | 20 |
| Wool | 0.0% → 0.0% | 0.0% → 0.0% | 27 |
| Leather | 40.0% → 0.0% | 5.3% → 0.0% | 5 |
| Velvet | 20.0% → 0.0% | 0.6% → 0.0% | 5 |
| Corduroy | 66.7% → 0.0% | 0.2% → 0.0% | 3 |
| Fleece | 13.0% → 0.0% | 6.5% → 0.0% | 23 |
| Nylon | 24.4% → 0.0% | 1.9% → 0.0% | 41 |
| Satin | 14.3% → 0.0% | 4.3% → 0.0% | 7 |
| Knitted | 0.0% → 0.0% | 0.0% → 0.0% | 0 |
| Suede | 50.0% → 0.0% | 0.4% → 0.0% | 2 |
