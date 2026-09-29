# Project Master Guide: Everything About This Project

**One-line pitch:** We built the first (to our knowledge) dataset and model for finding *per-topic* sentiment in real, romanised Hinglish e-commerce reviews — not just one positive/negative label for the whole review — and we are honestly documenting what works, what doesn't, and why.

Use this file to answer **any** question about the project: in the mid-term viva, in front of the supervisor, or about the BHASHA paper plan. Everything is written in short points, in plain English.

---

## 1. The Problem, in Plain Words

- Indian shoppers write reviews mixing Hindi and English in one sentence, typed in English letters (Roman script). This is called **Hinglish** or **code-mixing**.
  - Example: *"delivery fast thi but product ki quality bekar hai"* (delivery was fast, but product quality was bad).
- Most sentiment tools give **one label for the whole review** (positive/negative). This hides useful information: the review above is BOTH positive (delivery) and negative (quality).
- A business reading "this review is negative" cannot tell **what to fix**. A business reading "Delivery: Positive, Product Quality: Negative" can act on it directly.
- This finer approach is called **Aspect-Based Sentiment Analysis (ABSA)**: find every topic ("aspect") a review discusses, and give each one its own sentiment.

**Why this specific problem is new / a gap:**
- Existing Hinglish sentiment data (e.g. SentiMix) gives only one label per message, and is from Twitter, not reviews.
- Existing ABSA data for Hindi-English (ABSA-MIX, and the base paper CMF_HIT's data) is about **restaurants and laptops**, not shopping apps — and CMF_HIT's data turned out to be **translated from English and written in Devanagari script**, not the way people actually type Hinglish.
- No one had built this for Indian e-commerce apps, with real user-written Hinglish, before.

---

## 2. The Full Pipeline (What We Built, Step by Step)

| # | Stage | In plain words | Status |
|---|---|---|---|
| 1 | **Data Collection** | Download real reviews from the Google Play Store | ✅ Done (15 apps) |
| 2 | **Pre-processing** | Remove duplicates/spam, keep only Hinglish reviews | ✅ Done |
| 3 | **Annotation** | We label each review by hand: which topic, what sentiment | ✅ Done (1,018 reviews) |
| 4 | **Modelling** | Train AI models to do this labelling automatically | ✅ Done (3 models) |
| 5 | **Evaluation** | Measure how good the models are, honestly | ✅ Done |
| 6 | **Explainability** | Show *why* the model decided something (which words) | ✅ Working prototype |
| 7 | **Retrieval (RAG)** | Look up similar past reviews to help the decision | ✅ Tested (early prototype, honest negative result) |
| 8 | **Business Dashboard** | Turn results into something a company can actually use | ✅ Working |

---

## 3. What We Actually Did — With Real Numbers

### 3.1 Data
- Collected reviews from **15 apps**: 12 shopping/quick-commerce platforms (Meesho, Nykaa, Blinkit, Zepto, Flipkart, Amazon, Myntra, AJIO, BigBasket, Swiggy, Snapdeal, Shopsy) + **3 D2C brands** (Lenskart, Purplle, Bewakoof) added specifically to get more product-focused reviews.
- Used **google-play-scraper** (no login needed), pulling reviews **separately by star rating (1–5)** — because shopping apps get mostly 5-star reviews, and pulling randomly would give us almost no negative examples to learn from.
- Queried in **both English and Hindi store-language settings** — Hinglish reviews show up under either one; using only English would have missed over half of them.
- **1,018 reviews labelled** in total (668 train / 118 validation / 232 test).

### 3.2 Annotation (Labelling)
- **12 aspect categories**: Delivery, Price_Charges, Offers_Discounts, Product_Quality, Availability, Wrong_Missing_Item, Refund_Return, Payment_Wallet, Customer_Support, App_Experience, Packaging, Overall.
- **Pilot round** (100 reviews, all 3 of us labelled independently): agreement (Fleiss' kappa) = **0.55** (moderate). Sentiment-only agreement = **0.80** (almost perfect) — meaning we agreed on the *feeling*, but not always on *which category*.
- Found the problem: the "Overall" category was being used differently by each person (one used it as a summary for every review; another only for explicit statements). Agreement on "Overall" alone was **−0.02** (no agreement at all).
- **Fixed the guidelines (v2)**: Overall now means only an explicit general statement ("accha app hai"); added a separate "how does the whole review feel" field; added 2 new categories (Offers_Discounts, Availability) the team asked for.
- **Final round** (147 reviews, same independent-labelling method): agreement jumped to **0.68** overall, **0.84** on sentiment, and Overall's own agreement rose from −0.02 to **0.52**.
- 7 leftover disagreements (all 3 labels different) were settled by one designated adjudicator following the written rules.

### 3.3 Models
- **Task setup**: each (review, one category) pair is one example; the model says None / Positive / Negative / Neutral for that one category. This lets one review get different answers for different topics.
- **3 models compared** on the 232-review gold test set (never seen during training), each transformer run with **3 random seeds** and reported as mean ± standard deviation:

| Model | Aspect + Sentiment F1 (all categories) | Same, Overall excluded |
|---|---|---|
| TF-IDF + Logistic Regression (classic ML) | 0.494 | 0.451 |
| **XLM-R** (transformer) | 0.481 ± 0.005 | **0.481 ± 0.011** |
| MuRIL (transformer, made for Indian languages) | 0.323 ± 0.092 | 0.228 ± 0.170 |

- **Key finding**: once the inconsistently-labelled "Overall" category is excluded, XLM-R is clearly the best and very stable across seeds. The simple model wins only when Overall is included, because XLM-R struggles specifically with that one messy category.
- **MuRIL problem found & partly fixed**: it first predicted nothing at all (F1 = 0.000). We found the cause (it was drowned out by the majority "None" class) and fixed it with a class-weighted loss — it now learns, but its scores vary a lot across seeds (still an open problem for later).
- **Learning curve**: trained on 12.5% to 100% of the data; F1 rose steadily (0.30 → 0.49) but with **diminishing returns** — doubling the data from ~390 to 786 reviews only added 0.04 F1. This tells us *where to focus next* (fixing weak spots, not just collecting endlessly more data).

### 3.4 Explainability (SHAP)
- For every test review, we can show which words pushed the model toward its answer.
- Found the model correctly uses sensible words (e.g. "acha", emojis) and handles misspellings (e.g. "dilivery").
- Also found a real mistake: for one review with "kharab" (bad), the word actually pushed the prediction *toward* positive — a genuine bug made visible by the explanation, which a plain accuracy score would have hidden.

### 3.5 Retrieval (RAG) — an honest negative result
- Built a system that finds the 3 most similar past reviews for any new review (using multilingual sentence embeddings + FAISS).
- Tested it: only **39%** of test reviews had a top match that shared the same topic. Using only these matches to predict labels gave F1 = 0.30, well below the model's own 0.481.
- **Conclusion**: the retriever finds similar *wording*, not similar *topics*. This is a real, useful negative result — it tells us exactly what to build next (an aspect-aware retriever), instead of pretending RAG already works.

### 3.6 Business Dashboard
- One interactive webpage showing: complaints by app and category, top-3 complaints per app, model vs. human label comparison, and a searchable review explorer with word highlights and similar reviews.
- Works fully offline (single HTML file).

### 3.7 Base Paper Analysis (CMF_HIT)
- We studied the released code/data of CMF_HIT (the current best method for this kind of task) hoping to use it as a baseline.
- Found: the released Hindi-English data is **restaurant reviews translated from English**, written in Devanagari script (not how people actually type Hinglish); the released code does **not** implement the full architecture described in the paper (missing syntactic features, no real gated fusion, sentence-level not aspect-level output).
- We reported this **factually, without accusing anyone** — a more complete version may exist privately. This is why we could not reproduce it directly, and why our own dataset is needed.

---

## 4. Every Change We Made — and Why (viva-ready)

| # | What we changed | Why |
|---|---|---|
| 1 | Task level: one sentiment **per aspect**, not per sentence (unlike the base paper) | Real reviews praise one thing and criticise another — one label can't show both |
| 2 | Used the **sentence-pair formulation** (review + category name → sentiment), following Sun et al. 2019 | Lets one review get a different answer for each category, cleanly |
| 3 | Categories **built from our own data**, not copied from the base paper's restaurant categories | Shopping-app reviews talk about delivery/charges/refunds, not "food" or "ambience" |
| 4 | Guidelines **v1 → v2** after the pilot | The pilot showed "Overall" was being used inconsistently (agreement = −0.02); we fixed the definition and added 2 categories the team found missing |
| 5 | **Capped "None" examples at 3× the real examples** during training | Most (review, category) pairs are "None"; without capping, the model just learns to always say "None" |
| 6 | Added a **class-weighted loss** for the transformers | An early run showed MuRIL predicting nothing at all — the loss was rebalanced so rare classes matter too |
| 7 | Excluded one annotator's "Overall" labels **from training only** (kept everything else) | That batch had used the old v1 rule; the labels themselves weren't edited, just not used to train on, to avoid silently overriding a person's own work |
| 8 | Report all model results **with and without "Overall"** | Overall was inconsistently labelled even after revision, so hiding this would be misleading |
| 9 | Reported the **CMF_HIT code/data problems neutrally**, not as an accusation | We can't know if a more complete version exists privately; the goal is an honest account, not a criticism |
| 10 | Did **not** invent a new loss function or new formula | Our contribution is the **dataset, task framing, and honest analysis** — not a new algorithm. Using standard, well-known metrics (F1, Cohen's/Fleiss' kappa) keeps our results comparable and checkable by others |
| 11 | Trimmed references from 33 → 15 in the report | Kept only what's directly used (base paper, comparison datasets, the exact method/models/metrics we use) — every kept reference is actually cited in the text, and nothing cited is missing from the list |

---

## 5. Progress-Report / Viva Questions — Ready Answers

**Q: What is new/original in your project?**
> We created (to our knowledge) the first aspect-level sentiment dataset of real, romanised Hinglish e-commerce reviews, with a tested annotation process, benchmark models, and an honest analysis of what makes this data hard — for both annotators and models.

**Q: What exactly did you change compared to the base paper (CMF_HIT)?**
> See Section 4 above — task level, category set, training details, and evaluation are all different, all for stated reasons tied to our data and goal.

**Q: Why didn't you invent a new formula/algorithm?**
> Our research question is about the data and the task, not a new method. Standard metrics (F1, kappa) make our results comparable and verifiable. The dataset, the task reformulation (per-aspect vs per-sentence), and the honest failure analysis are the actual contribution.

**Q: Why does the simple TF-IDF model beat XLM-R sometimes?**
> With only ~700 training reviews, big models don't always beat small ones — this is a known pattern. Once the noisy "Overall" category is excluded, XLM-R is already ahead and far more stable across seeds. The learning curve shows scores are still rising with more data.

**Q: Why is kappa (agreement) important?**
> The model only learns from our labels. Kappa proves those labels are consistent between people, not just one person's opinion. Our own pilot showed exactly why it matters: one unclear rule (Overall) broke agreement and later confused the model until we fixed it.

**Q: What does RAG/retrieval actually do in your project right now?**
> It finds similar past reviews. We tested it honestly: it currently finds similar *wording*, not similar *topics* (39% aspect-match rate), so it doesn't yet improve predictions. That's a real finding, not a hidden failure, and it directly motivates our next step (an aspect-aware retriever).

**Q: What is left / future work?**
> Growing the dataset further (especially rare categories), fixing MuRIL's instability, building an aspect-aware retriever, re-implementing CMF_HIT properly from its paper, and submitting the work as a research paper.

**Q: What are the limitations?**
> Small test set (232 reviews) so small score differences may not be meaningful; most training reviews were labelled by only one annotator; several categories have very few examples; MuRIL's variance isn't fully understood yet; retrieval isn't used to change predictions yet, only evaluated.

---

## 6. "Why a Research Paper?" — Generic Questions

**Q: Why turn a college project into a research paper?**
> It's real, original work: a new dataset, a tested annotation process, and honest benchmark results. Publishing it validates the work externally, is valuable for our resumes/further studies, and gives the wider community (especially Hinglish NLP researchers in India) a resource that doesn't currently exist.

**Q: Isn't a B.Tech project usually not "publishable"?**
> Not all are, but ours has three things reviewers look for in a resource paper: (1) a new, carefully-annotated dataset, (2) a measured annotation process with before/after agreement scores, (3) benchmark results with proper multi-seed evaluation and honest negative results. That combination is exactly what a dataset/resource-focused venue wants.

**Q: What if the paper gets rejected?**
> We still get real reviewer feedback (by 10 Nov, before our final college evaluation), which we can act on. We can revise and submit to another venue. Either way, the dataset and results still count as genuine project output for the final evaluation.

**Q: Who are the authors?**
> Arpita, Harsh, Punit as the student authors; our supervisor is expected to be a co-author (standard practice) — to be confirmed with him directly.

---

## 7. "Why BHASHA / Why This Conference?" — Generic Questions

**Q: What is BHASHA?**
> The 2nd Workshop on BHASHA (Benchmarks, Harmonization, Annotation, and Standardization for Human-Centric AI in Indian Languages), held as part of **ICON 2026** (the flagship conference of the NLP Association of India), at Gauhati University, Guwahati, on **20 December 2026**.

**Q: Why this venue specifically, and not a bigger international conference?**
> BHASHA is explicitly focused on **datasets, annotation, and benchmarks for Indian languages** — exactly what our contribution is. It's realistic for a first paper (workshop-level, not a massive top-tier conference), it's in India (feasible to attend), and papers are published in the **ACL Anthology**, the main NLP research archive — good for visibility and resumes.

**Q: Is a workshop paper "less important" than a conference paper?**
> It's a smaller, more focused venue than the main ICON conference, but still peer-reviewed and archived in the ACL Anthology. For a first publication with a dataset contribution, it's an appropriate and respected target.

**Q: What are the deadlines?**
> Submission: **15 October 2026**. Reviews back: **10 November 2026**. Camera-ready (final version, if accepted): **25 November 2026**. Workshop: **20 December 2026**.

**Q: What format is required?**
> A short paper (up to 4 pages) using the **ACL Rolling Review template** in LaTeX/Overleaf, plus a references/limitations/ethics section as the template allows.

**Q: Does BHASHA welcome "negative results" like your retrieval finding?**
> Yes — the call for papers explicitly invites negative results. Our retrieval finding and our honest report on the base paper's code issues both fit this well.

**Q: What happens if we get accepted?**
> At least one author must register and present in person in Guwahati on 20 December. We should check with college about travel/registration support.

**Q: Is the paper written by AI?**
> No — the paper text must be written by us (Arpita, Harsh, Punit), reviewed by our supervisor, and checked with Turnitin. Any AI assistance used (for code, explanations, or feedback on drafts) will be disclosed, as ACL-affiliated venues require.

---

## 8. Notebook & File Guide

| File | What it does |
|---|---|
| `Step1_Pilot_Scrape.ipynb` | First data collection (4 apps) |
| `Step2_Annotator_Agreement.ipynb` | Pilot kappa calculation (round 1, 10 categories) |
| `Step3_Train_Evaluate.ipynb` | Mid-sem prototype training/evaluation |
| `Step4_Scrape_More_Data.ipynb` | Second, larger data collection (15 apps) |
| `Step5_Final_Agreement.ipynb` | **Final kappa calculation** (round 2, 12 categories) — *run this yourself for a real screenshot* |
| `Step6_Final_Experiments.ipynb` | Final training: 3 seeds, learning curve, SHAP, retrieval — produces the numbers in the report |
| `final_dataset.csv` | The complete 1,018-review labelled dataset (train/val/test) |
| `results_v3.json` | Final model results, explanations, and retrieval data (feeds the dashboard) |
| `hinglish_review_dashboard.html` | The business dashboard (works offline) |
| `BTP_MidTerm_Report_v4.docx` | The mid-term progress report (11 pages) |

---

## 9. Simple Glossary

| Term | Meaning |
|---|---|
| Hinglish / code-mixing | Hindi + English mixed in one sentence, typed in English letters |
| ABSA | Aspect-Based Sentiment Analysis — sentiment for each topic, not the whole review |
| Aspect category | One of our 12 topics (Delivery, Price_Charges, etc.) |
| Annotation | Labelling data by hand to create the "correct answers" |
| Gold / test set | Carefully checked labels, never used in training, used only to measure the model |
| Kappa (Cohen's, Fleiss') | Agreement between people, corrected for lucky guesses (0 = chance, 1 = perfect) |
| F1 score | A single number combining precision and recall |
| XLM-R, MuRIL | Pre-trained multilingual AI models we fine-tune on our data |
| Fine-tuning | Teaching a pre-trained model our specific task using our labels |
| Random seed | A setting controlling randomness; running 3 seeds shows a result isn't luck |
| SHAP | A method that shows which words caused a model's decision |
| RAG / Retrieval | Looking up similar past examples to support a decision |
| Negative result | An honest "this didn't work as hoped" finding — still valuable to report |
| ACL Anthology | The main online archive/library of NLP research papers |
