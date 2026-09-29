# Data Card: Hinglish E-commerce ABSA Dataset

## Summary

1,018 Hinglish (code-mixed Hindi-English) reviews collected from 15 Indian e-commerce and quick-commerce Android applications, manually labelled for aspect category and sentiment.

## Files

- `final_dataset.csv` — the complete labelled dataset
- `keys/annotation_sample_key.csv`, `keys/batch_key.csv`, `keys/round2_key.csv` — internal bookkeeping (which review was assigned to which annotator, star rating, source app), useful for reproducing the exact train/validation/test split

## Columns in `final_dataset.csv`

| Column | Description |
|---|---|
| `ID` | Internal review identifier |
| `round` | 1 (pilot collection) or 2 (second, larger collection) |
| `App` | Source application name |
| `group` | `platform` (general shopping/quick-commerce app) or `d2c` (direct-to-consumer brand app) |
| `stars` | Star rating (1-5) given by the reviewer |
| `review_id` | Original Play Store review identifier |
| `Review` | The review text |
| `Review_Sentiment` | Overall sentiment of the review (Positive / Negative / Neutral / Mixed) |
| `Delivery`, `Price_Charges`, `Offers_Discounts`, `Product_Quality`, `Availability`, `Wrong_Missing_Item`, `Refund_Return`, `Payment_Wallet`, `Customer_Support`, `App_Experience`, `Packaging`, `Overall` | Sentiment for that aspect category (Positive / Negative / Neutral), blank if the review does not discuss it |
| `annotator` | Who labelled this review (or `gold (3 annotators)` / `shared (3 annotators)` for the double/triple-checked subsets) |
| `split` | `train`, `val`, or `test` |
| `mask_overall` | `True` for rows where the `Overall` label followed an earlier, superseded annotation guideline and should be excluded when training on the `Overall` category |

## Collection method

- Reviews were collected via the open-source [google-play-scraper](https://github.com/JoMingyu/google-play-scraper) library, which requires no login.
- Collected separately by star rating (1-5) to counteract the natural positive skew of app-store reviews, and under both the English and Hindi Play Store language settings, since Hinglish reviews appear under either.
- Only review text, star rating, and timestamp were retained. Usernames and profile photographs were **not** collected.

## What is NOT included

Raw, unlabelled candidate reviews collected during scraping (tens of thousands of rows) are not redistributed in this repository, in view of the Google Play Store's terms of use. Only the final labelled subset, identified by `review_id`, is released here. Researchers wishing to re-derive the larger raw candidate pool can do so with the same collection script and the app list documented in the notebooks.

## Annotation process

Twelve aspect categories were defined from the pilot data. Annotation guidelines went through two versions (v1 -> v2) after a pilot inter-annotator agreement study revealed inconsistent use of one category ("Overall"). See `docs/PROJECT_MASTER_GUIDE.md` for the full guideline text and the agreement study results.

## Intended use

Research on aspect-based sentiment analysis, code-mixed / Hinglish NLP, and low-resource annotation methodology. Not intended for any use that identifies or targets individual reviewers.

## License

Released for research use. See repository `LICENSE` for code licensing; the dataset itself is derived from publicly posted app reviews with personal identifiers removed.
