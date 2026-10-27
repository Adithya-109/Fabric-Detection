# Fabric-Detection

Identify the fabric of a garment (Cotton, Polyester, Silk, Denim, Linen, Wool, Leather, Velvet,
Corduroy, Fleece, Nylon, Satin, Knitted, Suede) from an ordinary photo of clothing.

## Run the web app

**On Google Colab (no setup):**
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Adithya-109/Fabric-Detection/blob/main/notebooks/run_web_app.ipynb)
— click, then **Runtime → Run all**; the last cell prints the link to the app.

**On a Mac / PC:**
```bash
git clone https://github.com/Adithya-109/Fabric-Detection.git && cd Fabric-Detection
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_web.py          # then open http://127.0.0.1:5050
```

## Status
The app uses a **CLIP + linear-head** model (best in EXP-404: ~58% balanced accuracy on everyday clothing
photos; the old EfficientNet-B0 weights scored ~32%). Set `FABRIC_MODEL=efficientnet` to use the old weights.
Known limits: the head never saw "Knitted" and has few Corduroy/Suede/Velvet examples. See
`docs/IMPROVEMENT_PLAN.md`, `memory/records/EXP-40*.md`; a proper retraining is planned on Google Colab
(`docs/COLAB_TRAINING_PLAN.md`).

## Tests
```bash
pytest        # or: python -m unittest discover -s tests -t .
```
