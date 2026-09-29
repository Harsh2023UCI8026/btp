# Annotation Guidelines

## Categories (v2, final)

| Category | What it covers | Example words |
|---|---|---|
| Delivery | Speed, late or failed delivery, delivery partner behaviour, address issues | delivery late, 10 min me aa gaya |
| Price_Charges | Product prices, delivery/handling/platform fees, minimum order for free delivery | mehnga, handling fee, sasta |
| Offers_Discounts | Discounts, offers, coupons, cashback, referral codes, free gifts | cashback nahi mila, discount kam |
| Product_Quality | Damaged, expired or fake items; good or bad quality generally | kharab saman, purane aate hai |
| Availability | Out of stock, product range, delivery coverage in an area | product nahi milte, sab mil jata hai |
| Wrong_Missing_Item | Wrong product, size or colour; items missing from an order | galat saman, item missing |
| Refund_Return | Refund, return, replacement, exchange | paise wapas nahi aaye |
| Payment_Wallet | UPI, cash on delivery, cards, wallet balance, failed payments | payment fail, paise kat gaye |
| Customer_Support | Customer care, help chat, complaint handling | customer care koi reply nahi |
| App_Experience | Technical/usability issues only: bugs, login, notifications, ease of use | app hang, bar bar notification |
| Packaging | Condition of the box or parcel | packing achhi thi |
| Overall | An explicit general opinion about the application or company (not a summary) | accha app hai, bekar app, fraud |

**Sentiment values:** Positive (clear praise), Negative (a complaint or problem), Neutral (mentioned without a clear feeling, or a plain request, e.g. "discount diya karo"). Sarcasm is labelled by its intended meaning, not its literal words. If a review expresses both praise and complaint for the same category, the stronger of the two is used; if equally weighted, Neutral.

## v1 -> v2 revision

A pilot round (100 reviews, all three annotators labelling independently) measured Fleiss' kappa at 0.55 on category+sentiment agreement overall, but essentially zero (kappa = -0.02) on the `Overall` category specifically. Inspection showed the three annotators had been applying it in three different ways: as a running summary of nearly every review, as a label reserved only for explicit statements, and as something in between.

Guidelines were revised as follows:

1. **Overall** redefined to apply only when a review makes an explicit general statement about the app or company ("accha app hai", "fraud", "bekar app") — not as a summary of the review's other aspects.
2. Added a separate **review-level sentiment** field, capturing "how does the whole review feel" independently of any specific aspect.
3. **App_Experience** narrowed to technical/usability issues only (bugs, login, notifications, ease of use), removing general praise/complaint that belongs under Overall.
4. Two categories added based on annotator feedback during the pilot: **Offers_Discounts** and **Availability**.

A second round (147 reviews, same independent-labelling protocol) under the revised guidelines raised agreement to 0.68 (category+sentiment), 0.84 (sentiment only), and 0.52 on the Overall category specifically (up from -0.02). See `docs/PROJECT_MASTER_GUIDE.md` for the full numeric breakdown.

## Annotation protocol

- Star ratings were hidden from annotators during labelling, so that labels depended only on the review text.
- A subset of reviews in each round was labelled independently by all three annotators (without discussion) specifically to measure agreement; the remainder were divided and labelled once each.
- Cases where all three labels disagreed (no majority) were resolved by a single designated adjudicator following the written guidelines above.
