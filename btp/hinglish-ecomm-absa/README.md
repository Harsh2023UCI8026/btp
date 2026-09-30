# Hinglish E-commerce ABSA

**Aspect-Based Sentiment Analysis of Code-Mixed Hinglish E-commerce Reviews: A Dataset, Benchmark Models, and an Explainable, Retrieval-Aware Pipeline**

B.Tech Project — [University Name] · [Semester/Year]
Team: Arpita, Harsh, Punit · Supervisor: [Supervisor Name]

---

## What this is

Indian shoppers write app reviews mixing Hindi and English in one sentence ("Hinglish"), for example:

> *"delivery fast thi but product ki quality bekar hai"*

Most sentiment tools give this ONE label for the whole review. We instead find **every topic** a review discusses and give **each one its own sentiment** — Delivery: Positive, Product Quality: Negative — because that's what a business can actually act on.

This repo contains:
- **A labelled dataset** of 1,018 real Hinglish e-commerce reviews across 15 apps, with 12 aspect categories
- **An annotation study**: guidelines, a pilot agreement round, a revision, and a final agreement round
- **Benchmark models**: TF-IDF baseline, fine-tuned XLM-R, fine-tuned MuRIL (3 seeds each)
- **Explainability** (SHAP) and an early **retrieval (RAG)** prototype, evaluated honestly
- **An interactive dashboard** turning results into business-readable insights

## Repository structure

| Folder | Contents |
|---|---|
| `data/` | The final labelled dataset + a data card describing it |
| `annotation/` | Guidelines (v1 → v2), agreement scores, raw label files |
| `notebooks/` | All Colab notebooks, in pipeline order |
| `results/` | Model metrics, learning curve, all figures |
| `dashboard/` | The interactive dashboard (single HTML file, works offline) |
| `report/` | Mid-term progress report |
| `slides/` | Presentation deck |
| `docs/` | Extended project notes and Q&A reference |

## Key results (232-review held-out test set)

| Model | Aspect + Sentiment F1 |
|---|---|
| TF-IDF + Logistic Regression | 0.494 |
| **XLM-R** (best, most stable) | **0.481 ± 0.005** |
| MuRIL | 0.323 ± 0.092 |

Full results, the annotation agreement study (κ: 0.55 → 0.68 after guideline revision), and an honest evaluation of our retrieval prototype are in `report/` and `results/`.

## Dataset summary

- **1,018** labelled reviews (668 train / 118 validation / 232 test)
- **15** apps: 12 shopping/quick-commerce platforms + 3 D2C brands
- **12** aspect categories: Delivery, Price_Charges, Offers_Discounts, Product_Quality, Availability, Wrong_Missing_Item, Refund_Return, Payment_Wallet, Customer_Support, App_Experience, Packaging, Overall
- Collected via [google-play-scraper](https://github.com/JoMingyu/google-play-scraper); only review text, star rating, and timestamp were kept (no usernames/photos)
- See `data/DATA_CARD.md` for full column definitions and our data-release policy

## Quick start

```bash
# View the dataset
import pandas as pd
df = pd.read_csv("data/final_dataset.csv")

# Reproduce experiments
# Open notebooks/06_final_experiments.ipynb in Google Colab (T4 GPU recommended)

# View the dashboard
# Open dashboard/index.html in any browser — no server needed
```

## Live inference dashboard

The static dashboard can look up saved predictions offline, but new reviews need the trained checkpoint and the API. The final export cell in `notebooks/06_final_experiments.ipynb` now saves the validation-selected model and tokenizer. Follow [`backend/README.md`](backend/README.md) to copy that artifact into `artifacts/best_model/`, install `requirements-api.txt`, and run the dashboard/API on one local origin. Without the checkpoint, the site clearly marks new-review outputs as keyword estimates. Model weights are intentionally excluded from Git.

## Status

This is ongoing work. Current focus: an aspect-aware retriever, a proper re-implementation of the base paper (CMF_HIT) as an additional baseline, and preparing a short paper describing the dataset and findings.

## Citation

If you use this dataset or code, please cite this repository (a formal citation will be added once the accompanying paper is available).

## License

Code: MIT License (see `LICENSE`). Dataset: see `data/DATA_CARD.md` for terms.
