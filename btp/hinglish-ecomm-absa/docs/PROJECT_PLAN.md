# Hinglish Review Sentiment Project: Complete Plan and Status

**Team:** Arpita (lead and lead writer), Harsh (data lead), Punit (experiments lead)
**Type:** B.Tech Project (BTP)
**Main target:** 🎯 **Publish a research paper at the BHASHA Workshop, ICON 2026**

> Read this file fully once. It explains what the project is, why it matters, what is already done, and exactly what is left. Our team rule: **no internal deadlines, we finish everything as early as we can.** The only fixed dates are the conference dates below.

---

## 1. The project in 2 minutes

### The problem
Indian customers write app reviews in **Hinglish**, a mix of Hindi and English typed in English letters:

> *"ye to achhi baat hai isme exact 10 mint k andar delevery ho jata hai but isme lagbhag sare product mehnge dete hai"*

This one review says two things: **delivery is good**, **prices are bad**. Most AI tools give one label for the whole review ("negative" or "mixed"), so a company cannot tell **what to fix**.

### Our solution
A system that reads a Hinglish review and gives a separate sentiment for **each topic (aspect)** the customer talks about:

| Aspect | Sentiment |
|---|---|
| Delivery | Positive |
| Price_Charges | Negative |

This is called **Aspect-Based Sentiment Analysis (ABSA)**.

### Why this is research (what is new)
1. **New dataset:** the first (to our knowledge) aspect-level dataset of *real, romanised* Hinglish e-commerce app reviews. Existing Hinglish ABSA data is about restaurants and laptops, and the base paper's Hindi-English data is *translated* and written in *Devanagari script*.
2. **Annotation study:** we found *where* labelling Hinglish reviews is hard (people agree on the feeling, but not always on the category) and fixed the rules.
3. **Benchmark results:** first baseline scores for this task, with analysis (learning curve, SHAP word explanations).
4. **Honest negative results:** inconsistent labels can mislead a model; a general retriever finds similar *wording*, not similar *topics*; the base paper's released code could not reproduce its results.

---

## 2. Main target: the research paper

### The venue: BHASHA Workshop at ICON 2026

| | |
|---|---|
| **Full name** | 2nd Workshop on BHASHA: Benchmarks, Harmonization, Annotation, and Standardization for Human-Centric AI in Indian Languages |
| **Part of** | ICON 2026 (flagship conference of the NLP Association of India) |
| **Where / when** | Gauhati University, Guwahati, Assam, **20 December 2026** (in person) |
| **Website** | https://bhasha-workshop.github.io/ |
| **Submission portal** | https://cmt3.research.microsoft.com/BHASHA2026 |
| **Contact** | bhashaworkshop@gmail.com |
| **Published in** | ACL Anthology (the main archive of NLP research: good for resumes and higher studies) |

**Fixed external dates (Anywhere on Earth time):**

| Event | Date |
|---|---|
| **Paper submission deadline** | **15 October 2026** |
| Notification (reviews come back) | 10 November 2026 |
| Camera-ready (final version) | 25 November 2026 |
| Workshop | 20 December 2026 |

**Why BHASHA fits us perfectly:** its topics include creating datasets for Indian languages, annotation schemes and guidelines, and domain-specific tasks for India. It also explicitly welcomes **negative results**. That is exactly our work.

**Format:**
- **Short paper: 4 pages** ← our target. Long paper: 8 pages (only if the dataset becomes much bigger).
- **ACL Rolling Review template** (LaTeX, on Overleaf).
- Must not be published or under review anywhere else.
- If accepted, at least one author must register and present in person.

**Why the reviews matter for college:** reviews come back on 10 November, so we can show real reviewer feedback to our teachers before the final evaluation.

### Paper outline (4-page short paper)

| Section | Content | Space | Writer |
|---|---|---|---|
| Abstract | Problem, dataset, key numbers, main findings | about 150 words | Arpita |
| 1. Introduction | Hinglish reviews, why one label is not enough, contributions | about 0.5 page | Arpita |
| 2. Related Work | ABSA (SemEval), code-mixed sentiment (SentiMix), code-mixed ABSA (ABSA-MIX, CMF_HIT), multilingual models | about 0.4 page | Arpita |
| 3. Dataset | Collection, cleaning, 12 categories, annotation process, **agreement (kappa)**, statistics | about 1.3 pages | Harsh |
| 4. Experiments | Task setup, models (TF-IDF, XLM-R, MuRIL), results table with 3 seeds | about 0.9 page | Punit |
| 5. Analysis | Learning curve, label consistency lesson, SHAP examples, retriever negative result | about 0.6 page | Punit + Harsh |
| 6. Conclusion | Summary and future work | about 0.2 page | Arpita |
| Limitations, Ethics | Small data, one annotator for batches, Play Store data use, AI-tool use | as the template allows | All |
| References | All cited papers | not counted | Arpita |

> Check the template instructions for whether Limitations/Ethics count toward the 4 pages.

### Writing rules for the paper (very important)
- **The paper is written by us, in our own words.** It goes through Turnitin, and it represents our research.
- Claude's role: outline, explanations, code, figures, analysis, and **feedback on our drafts**. Claude does **not** write the paper's sentences.
- Our process: Claude gives the outline → **we write drafts** → Claude reviews → we revise → supervisor reviews → we submit.
- We **disclose AI tool use** (code and feedback) in the paper, as ACL venues require.
- Every citation must be checked on Google Scholar. Every claim of "first" uses "to the best of our knowledge".
- Before submitting: do one more literature search, in case a similar paper appeared recently.

---

## 3. The full pipeline and its status

| # | Stage | What it means | Status |
|---|---|---|---|
| 1 | **Data collection** | Download reviews from the Google Play Store | ✅ Pilot done · ✅ Round 2 collected |
| 2 | **Pre-processing** | Remove duplicates and short reviews, keep only Hinglish | ✅ Done (improved Hinglish detector) |
| 3 | **Annotation** | We label aspects + sentiment by hand | ✅ 464 labelled · ⏳ **Round 2: 600 to label** |
| 4 | **Modelling** | Train models: TF-IDF + LR, XLM-R, MuRIL | ✅ Prototype · ⏳ Final run with 3 seeds, fix MuRIL |
| 5 | **Evaluation** | F1 scores on a human-labelled test set | ✅ Prototype · ⏳ Final on bigger test set |
| 6 | **Explainability** | SHAP: which words drove each decision | ✅ Working |
| 7 | **Retrieval (RAG)** | Find similar past reviews to help the model | ✅ Retrieval step tested (negative result) · ⏳ Aspect-aware version after paper |
| 8 | **Business dashboard** | Complaints per app and aspect, review explorer | ✅ Working (v1) · ⏳ Update with final data |

---

## 4. What is DONE ✅

### 4.1 Research and planning
- [x] Literature review; research gap identified
- [x] Base paper (CMF_HIT, Expert Systems with Applications, 2026) found and studied
- [x] Base paper's code and data analysed: the released code is incomplete (random syntactic input, tokenizer output unused, simple concatenation instead of gated fusion, sentence-level outputs); the Hindi-English data is translated SemEval restaurant reviews in Devanagari script
- [x] Venue chosen: BHASHA @ ICON 2026

### 4.2 Pilot data (round 1)
- [x] 2,459 clean reviews from Meesho, Nykaa, Blinkit, Zepto
- [x] About 20% code-mixed (488 reviews)
- Findings: spelling varies a lot (bahut / bhot / bohot); the Hindi language setting found more than half of the Hinglish reviews; 5-star reviews are short (median 6 words) while 1-star reviews are long (median 18 words); reviews focus on service more than products

### 4.3 Annotation round 1
- [x] 12 aspect categories: Delivery, Price_Charges, Offers_Discounts, Product_Quality, Availability, Wrong_Missing_Item, Refund_Return, Payment_Wallet, Customer_Support, App_Experience, Packaging, Overall
- [x] Pilot agreement study on 100 reviews (all three of us, separately)

| Measure | Score | Meaning |
|---|---|---|
| Fleiss' kappa (category + sentiment) | 0.55 | Moderate |
| Sentiment only | **0.80** | Substantial |
| Without the "Overall" category | 0.69 | Substantial |
| "Overall" category alone | −0.02 | No agreement (we understood it differently) |

- [x] Rules updated to **v2** (Overall only for explicit general opinions; new Review_Sentiment column; 2 new categories)
- [x] **464 labelled reviews** (93 gold test, 315 train, 56 validation)

### 4.4 Prototype models (gold test set, 93 reviews)

| Model | Aspect + Sentiment F1 (all 12) | Aspect + Sentiment F1 (without Overall) |
|---|---|---|
| TF-IDF + Logistic Regression | **0.389** | 0.349 |
| XLM-R | 0.343 | **0.371** |
| MuRIL | 0.000 (did not learn) | 0.000 |

Key lessons:
- XLM-R is better at finding **specific aspects**; the simple baseline wins overall because XLM-R is weak on "Overall".
- **Label consistency matters:** one batch used "Overall" on 100% of reviews, and the model copied it (predicted Overall for 444 of 446 reviews). After excluding those labels, XLM-R improved from 0.289 to 0.343.
- **Learning curve:** baseline F1 rose from 0.22 (93 reviews) to 0.39 (371 reviews) and has not flattened. More data will help, which is why we are labelling more.

### 4.5 Explainability, retrieval, dashboard
- [x] SHAP explanations: the model uses sensible words ("acha", emojis), handles misspellings ("dilivery"), but also makes visible mistakes ("kharab" pushed towards Positive)
- [x] Retrieval test: the top similar review shared a specific aspect for only **30 of 93** test reviews (32%). A general retriever finds similar wording, not similar topics, so we need an aspect-aware retriever.
- [x] Interactive dashboard (single HTML file, works offline)

### 4.6 Round 2 data collection
- [x] 20,920 new clean reviews from **15 apps** (12 platforms + 3 D2C brands: Purplle, Lenskart, Bewakoof; Mamaearth did not load)
- [x] 1,667 clear Hinglish reviews (8%; varies by app, from Shopsy 19% to Bewakoof 6%)
- [x] **600 selected for labelling:** exactly 120 per star rating, 117 from D2C brands, spread over all 15 apps
- [x] Labelling files ready (rules v2 + 3 small additions)

### 4.7 College (mid-sem)
- [x] Full progress report draft (Word) with 9 figures, tables and references
- [x] Figures ready for PPT

---

## 5. What is LEFT ⏳ (in order)

### Step A: Label round 2 (all three) ← **we are here**
- [ ] Everyone re-reads the **Rules tab** (5 minutes)
- [ ] **Shared set (150 reviews): each person alone, no discussion** (`Round2_Shared150_<name>.xlsx`)
- [ ] Run `Step5_Final_Agreement.ipynb` → final kappa for the paper → send output to Claude
- [ ] Discuss disagreements together (do **not** edit the original files; the paper reports agreement before discussion)
- [ ] Own batch (150 reviews each): `Round2_Batch_<name>.xlsx`
- [ ] Send all files to Claude for a consistency check

**Result:** about 1,050 labelled reviews; test set of about 240 (old 93 gold + new 150 shared).

### Step B: Final experiments (Punit runs, Claude builds)
- [ ] Training notebook v3 (Claude): all data, 3 random seeds, mean ± standard deviation
- [ ] Fix MuRIL (or explain clearly why it does not converge)
- [ ] Learning curve on the full data
- [ ] SHAP examples and retriever test on the new test set
- [ ] Final tables and figures for the paper

### Step C: Write the paper (all three)
- [ ] Create the Overleaf project with the ACL template (anonymous version, unless the organisers say otherwise)
- [ ] Claude gives a detailed outline per section
- [ ] Each person drafts their sections (start now with parts that do not need final numbers: Introduction, Related Work, data collection, annotation process)
- [ ] Claude reviews drafts; we revise
- [ ] Supervisor reviews
- [ ] Final checks: page limit, anonymity, references, AI-use statement, Turnitin
- [ ] **Submit on CMT, well before 15 October**

### Step D: College mid-sem (runs alongside)
- [ ] Rewrite report sections in our own words; add the 8 screenshots; Turnitin check (AI detection must be under 20%)
- [ ] Supervisor signature; submit to Ms. Pooja, Computer Centre D101
- [ ] PPT (conference style, about 12 slides): Claude prepares the structure
- [ ] Practise the 10-minute talk and dashboard demo
- [ ] Q&A preparation: Claude prepares the 25 most likely questions with simple answers

### Step E: After submission (for final evaluation)
- [ ] **Aspect-aware retriever** (our new method idea: train the embedding model so reviews about the same aspect end up close together) and RAG experiments
- [ ] Dashboard v2 with final data and best model
- [ ] 10 Nov: reviews arrive → show teachers → improve paper (camera-ready by 25 Nov if accepted)
- [ ] Prepare dataset release on GitHub/HuggingFace (review IDs + labels + script, respecting Play Store terms)
- [ ] 20 Dec: present at BHASHA (if accepted)

### Decisions to settle now
- [ ] **Supervisor:** approval of the paper plan; co-authorship (usually yes)
- [ ] **Funding:** ask college about registration and travel support to Guwahati
- [ ] **Anonymity:** email bhashaworkshop@gmail.com to ask if submissions must be anonymous
- [ ] **Mid-sem presentation date:** confirm

---

## 6. Rules we must remember

### Annotation rules (v2, the most important points)
- **Overall** = only when the review *says* a general opinion in words ("accha app hai", "bekar app", "fraud"). It is **not** a summary.
- The whole-review feeling goes in **Review_Sentiment** (Positive / Negative / Neutral / Mixed).
- **App_Experience** = only technical things (bugs, login, ads/notifications, easy/hard to use).
- Fees and "free delivery only above ₹X" → **Price_Charges**. Cashback, coupons, referral points, free gifts → **Offers_Discounts**. "Not available in my area" → **Availability**.
- Requests ("discount do") → **Neutral**. Sarcasm → label the real meaning.
- Not really Hinglish, spam or unclear → write **"skip"** in Notes.
- Shared set: **alone, no discussion**. Never add new columns; write ideas in Notes.

### Integrity rules
- Paper and report text written by us. AI tool use disclosed in the paper.
- Report the numbers exactly as they came out. Never adjust results.
- Describe the base paper's code issues **neutrally** ("the released code differs from the paper's description"), never as an accusation.

---

## 7. Viva / Q&A: answers everyone should know

**What is new in your project?**
> We created the first (to our knowledge) aspect-level sentiment dataset of real Hinglish shopping-app reviews, with a tested annotation scheme, benchmark models, and an analysis of what makes this data hard, both for annotators and for models.

**What did you change from the base paper, and why?**

| What | Base paper | Ours | Why |
|---|---|---|---|
| Task level | One category and polarity per sentence | Sentiment per aspect | Reviews praise one thing and criticise another |
| Formulation | Joint multi-task model | (review, aspect) sentence pair → sentiment (Sun et al., 2019) | Same review, different answers per aspect |
| Data | Translated restaurant reviews, Devanagari | Real Play Store reviews, romanised Hinglish | How Indian users actually write |
| Categories | Restaurant categories | 12 e-commerce categories built from our data | Shopping reviews talk about delivery, refunds, charges |
| Evaluation | Sentence-level | Aspect detection F1, aspect + sentiment F1, macro F1 | Must match the per-aspect task |

**Did you change any formula?**
> No. F1, kappa, cross-entropy and SHAP are standard. Our research question is about the data and the task, not a new loss function. Standard metrics make our results comparable and easy to verify.

**Why did the simple TF-IDF model beat XLM-R overall?**
> With only about 300 training reviews, big models cannot adapt well; simple models often compete on tiny data. Without the inconsistent Overall category, XLM-R is already better. The learning curve shows scores rising with more data.

**Why is kappa important?**
> The model learns only from our labels. Kappa proves the labels are consistent across people, not just one person's opinion. Our pilot showed exactly why: one unclear rule (Overall) broke agreement and later misled the model.

**What does RAG do in your project?**
> It retrieves similar past reviews. We tested it honestly: a general retriever found reviews with similar wording but a matching aspect only 32% of the time. So our next step is an aspect-aware retriever.

---

## 8. File guide (what each file is)

### Notebooks (run on Google Colab)
| File | Purpose |
|---|---|
| `Step1_Pilot_Scrape.ipynb` | Pilot data collection (4 apps) |
| `Step2_Annotator_Agreement.ipynb` | Pilot kappa (round 1, 10 categories) |
| `Step3_Train_Evaluate.ipynb` | Training, evaluation, SHAP, retrieval, `results.json` |
| `Step4_Scrape_More_Data.ipynb` | Round 2 data collection (15 apps) |
| `Step5_Final_Agreement.ipynb` | **Round 2 kappa (for the paper)** |

### Data and labels
| File | Purpose |
|---|---|
| `pilot_reviews.csv` | Round 1 cleaned reviews |
| `Gold_100_Discussion.xlsx`, `Batch_<name>.xlsx` | Round 1 labels (464 usable) |
| `annotation_sample_key.csv`, `batch_key.csv` | Round 1 keys (stars, apps) |
| `new_reviews_all.csv`, `new_hinglish_candidates.csv` | Round 2 collected reviews |
| `Round2_Shared150_<name>.xlsx` | **Round 2 shared set (label alone)** |
| `Round2_Batch_<name>.xlsx` | **Round 2 own batch** |
| `round2_key.csv` | Round 2 key (do not open before labelling) |

### Results and outputs
| File | Purpose |
|---|---|
| `results.json` | Version 2 model results (used by the dashboard) |
| `hinglish_review_dashboard.html` | Dashboard (opens offline in any browser) |
| `BTP_MidSem_Progress_Report_Draft.docx` | Full mid-sem report draft |
| `Figure*.png` | All figures (report, PPT, paper) |

> Keep everything in our **GitHub repo**. Good repo + paper + dashboard link = strong resume.

---

## 9. Simple glossary

| Term | Meaning |
|---|---|
| **Hinglish / code-mixing** | Hindi and English mixed in one sentence, typed in English letters |
| **ABSA** | Aspect-Based Sentiment Analysis: sentiment for each topic in a review |
| **Aspect category** | One of our 12 topics (Delivery, Price_Charges, …) |
| **Annotation** | Labelling reviews by hand to create the "answer key" |
| **Gold / test set** | Carefully checked labels, never shown to the model while training |
| **Kappa (Cohen, Fleiss)** | Agreement between annotators, corrected for luck (0 = chance, 1 = perfect) |
| **F1 score** | Combines precision and recall into one model score |
| **TF-IDF + LR** | Classic ML: word/character counts + logistic regression |
| **XLM-R, MuRIL** | Pre-trained multilingual transformer models; MuRIL is made for Indian languages |
| **Fine-tuning** | Teaching a pre-trained model our specific task with our labels |
| **Random seed** | Controls randomness; running 3 seeds shows results are stable |
| **Learning curve** | How the score changes as training data grows |
| **SHAP** | Shows which words pushed the model towards its answer |
| **RAG / retrieval** | Looking up similar past reviews to support a decision |
| **Negative result** | An honest finding that something did *not* work; useful for other researchers |
| **Camera-ready** | The final corrected version of an accepted paper |
| **ACL Anthology** | The official online archive of NLP papers |
