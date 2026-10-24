# Patch-strategy diagnostic

483 images from `data/external/eval` (≤150 per class). Weights: `backend/fabric_classifier/weights/fabric_clf_best.pt`.
Garment mask too small → centre-crop fallback on 0 images; garment covers 26% of a photo on average.

Chance level: balanced accuracy ≈ 1/13 = 7.7%, median rank ≈ 7, AUC = 0.5.

| Variant | Balanced acc. | Macro-F1 | Top-3 | Median true rank | Cotton-vs-Poly AUC | Balanced acc. (raw) | Single-crop fallbacks |
|---|---|---|---|---|---|---|---|
| legacy_orig | 21.6% | 13.0% | 54.9% | 3 | 0.606 | 21.9% | 1 |
| legacy_512 | 32.5% | 21.1% | 66.3% | 2 | 0.630 | 29.9% | 4 |
| centre_512 | 25.3% | 17.5% | 57.1% | 3 | 0.614 | 25.6% | 0 |
| garment_512 | 29.7% | 18.8% | 61.7% | 3 | 0.595 | 26.2% | 0 |
| whole | 25.9% | 17.1% | 60.5% | 3 | 0.661 | 29.0% | – |

Columns 2–5 are after undoing the training-prior inversion (no tuning on this data).

## Recall per class (prior-fixed)

| Class | n | legacy_orig | legacy_512 | centre_512 | garment_512 | whole |
|---|---|---|---|---|---|---|
| Cotton | 150 | 15% | 13% | 17% | 29% | 12% |
| Polyester | 150 | 14% | 26% | 21% | 17% | 18% |
| Silk | 43 | 9% | 35% | 30% | 16% | 26% |
| Denim | 7 | 71% | 86% | 43% | 57% | 57% |
| Linen | 20 | 10% | 25% | 25% | 30% | 25% |
| Wool | 27 | 0% | 26% | 15% | 15% | 19% |
| Leather | 5 | 60% | 80% | 40% | 60% | 60% |
| Velvet | 5 | 20% | 40% | 40% | 40% | 20% |
| Corduroy | 3 | 33% | 0% | 0% | 33% | 33% |
| Fleece | 23 | 26% | 39% | 43% | 22% | 22% |
| Nylon | 41 | 22% | 10% | 12% | 10% | 17% |
| Satin | 7 | 0% | 43% | 43% | 57% | 29% |
| Suede | 2 | 0% | 0% | 0% | 0% | 0% |
