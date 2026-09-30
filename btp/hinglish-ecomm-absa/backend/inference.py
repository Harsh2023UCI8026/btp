"""Load the exported notebook checkpoint and run the same aspect-pair model."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_DIR = PROJECT_ROOT / "artifacts" / "best_model"
DEFAULT_CATEGORIES = [
    "Delivery",
    "Price_Charges",
    "Offers_Discounts",
    "Product_Quality",
    "Availability",
    "Wrong_Missing_Item",
    "Refund_Return",
    "Payment_Wallet",
    "Customer_Support",
    "App_Experience",
    "Packaging",
    "Overall",
]
DEFAULT_LABELS = ["None", "Positive", "Negative", "Neutral"]


def category_text(category: str) -> str:
    """Match notebook 06's category text exactly."""
    return category.replace("_", " ").lower()


class AspectSentimentModel:
    """A single four-way classifier queried once for each review/aspect pair."""

    def __init__(self, model_dir: str | Path | None = None) -> None:
        self.model_dir = Path(model_dir or os.getenv("ABSA_MODEL_DIR", DEFAULT_MODEL_DIR)).expanduser()
        manifest_path = self.model_dir / "manifest.json"
        if not manifest_path.is_file():
            raise FileNotFoundError(
                f"Model artifact not found at {self.model_dir}. Train/export it from notebook "
                "06_final_experiments.ipynb, then place its files in this directory."
            )

        self.manifest: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.categories = self.manifest.get("categories", DEFAULT_CATEGORIES)
        self.labels = self.manifest.get("labels", DEFAULT_LABELS)
        if self.labels != DEFAULT_LABELS:
            raise ValueError(f"Unexpected checkpoint class order: {self.labels!r}")
        if not self.categories or not all(isinstance(c, str) for c in self.categories):
            raise ValueError("Checkpoint manifest must list its aspect categories.")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.max_length = int(self.manifest.get("max_length", 128))
        self.batch_size = int(self.manifest.get("inference_batch_size", 32))
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir, local_files_only=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_dir, local_files_only=True
        ).to(self.device)
        self.model.eval()
        if self.model.config.num_labels != len(self.labels):
            raise ValueError(
                f"Checkpoint has {self.model.config.num_labels} outputs, but its manifest "
                f"lists {len(self.labels)} labels."
            )

    @torch.inference_mode()
    def predict(self, reviews: list[str]) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = [
            {"index": i, "text": review, "labels": {}, "confidence": {}}
            for i, review in enumerate(reviews)
        ]
        pairs = [
            (review_index, category, review)
            for category in self.categories
            for review_index, review in enumerate(reviews)
        ]
        for start in range(0, len(pairs), self.batch_size):
            batch = pairs[start : start + self.batch_size]
            encoded = self.tokenizer(
                [review for _, _, review in batch],
                [category_text(category) for _, category, _ in batch],
                truncation=True,
                max_length=self.max_length,
                padding=True,
                return_tensors="pt",
            ).to(self.device)
            probabilities = torch.softmax(self.model(**encoded).logits.float(), dim=-1)
            scores, indices = probabilities.max(dim=-1)
            for (review_index, category, _), score, index in zip(
                batch, scores.tolist(), indices.tolist()
            ):
                sentiment = self.labels[index]
                if sentiment != "None":
                    results[review_index]["labels"][category] = sentiment
                    results[review_index]["confidence"][category] = round(float(score), 4)
        return results
