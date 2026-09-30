# Live model inference

The browser dashboard is a static HTML page. This small API loads the fine-tuned sequence classifier exported by notebook 06 and runs the same review/category text-pair prediction used during training. Without the checkpoint, the service still serves the dashboard, but `/api/analyze` returns `503` and the page clearly falls back to its offline keyword estimate.

## 1. Export the checkpoint

Open `notebooks/06_final_experiments.ipynb` in Google Colab and run the experiment through the final export cells. The updated notebook saves the validation-selected model, tokenizer, and `manifest.json` under the persistent Drive directory:

```text
/content/drive/MyDrive/hinglish_absa_runs/best_model
```

Download that entire folder and place it in this repository as:

```text
artifacts/best_model/
```

The folder must contain the Hugging Face model config, tokenizer files, model weights, and `manifest.json`. Keep large model weights out of Git; this repository's `.gitignore` excludes `artifacts/`.

## 2. Install and run locally

From the repository root:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux:       source .venv/bin/activate
python -m pip install -r requirements-api.txt
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000/>. The browser and API share an origin, so no CORS setup or API key is needed. API health and interactive docs are at `/api/health` and `/docs`.

To store the model elsewhere, set `ABSA_MODEL_DIR` to the folder containing the checkpoint manifest. CPU inference works but is slower; a CUDA-enabled PyTorch installation is recommended for batches.

## API

`POST /api/analyze` accepts `{"reviews": ["review one", "review two"]}` (up to 100 reviews per call). It returns one set of aspect labels and each detected label's raw softmax confidence per review. Those scores are not calibrated probabilities of correctness. The class order and aspect text construction are taken from the checkpoint manifest and the model's four classes are `None`, `Positive`, `Negative`, and `Neutral`.

## Current limitation

This repo contains evaluation predictions, not trained weights. The first Colab training/export run is required to produce the checkpoint. API and UI wiring can be prepared without it, but a new review cannot receive an actual trained-model prediction until `artifacts/best_model/` is installed. The static Vercel configuration only publishes the HTML dashboard; deploy this Python API and checkpoint to a Python-capable host separately if you need hosted live inference.
