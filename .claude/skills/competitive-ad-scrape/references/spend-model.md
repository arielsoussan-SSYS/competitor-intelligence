# Spend estimation

**The implementation is `tools/spend_model.py`. This file explains it. If the two
ever disagree, the code is right and this file is stale.**

Dollars are **never stored in a data file**. `data/*.json` holds observations
(impression band, run dates, format, payer). Every dollar figure is derived at
render time, so an estimate can always be traced to the band, the run length and
the CPM that produced it. Same rule as the dashboard: the data is the asset, the
numbers are a view.

Everything here is labelled `[Estimate]`. LinkedIn never discloses spend.

---

## What LinkedIn actually discloses

Only for ads **targeted to the EU**, to comply with the Digital Services Act:

| Disclosed | Not disclosed |
|---|---|
| Estimated total impressions, banded | Spend, ever |
| Per-country percentage split | Exact impressions |
| Run dates (`Ran from X to Y`) | Engagement, CTR, conversions |
| Targeting parameters | Bid strategy or budget type |
| Payer of record | Anything at all for non-EU-targeted ads |

Three things about this that are easy to get wrong:

1. **The disclosed total is the ad's FULL total across all countries**, not an
   EU subtotal. Verified 2026-09-22: HP's MJFNext teaser reads `500k-1M` total
   with the split `US 97%, France 2%, Spain 1%`. So one EU-targeted ad gives you
   the whole ad, and the split lets you apportion by country.
2. **An ad with no EU targeting has no impression data at all.** That is missing
   data, not zero spend. Never impute it from an ad that does have a band.
3. **Most ads are not EU-targeted.** On 2026-09-22, HP had 2 EU-served ads out of
   36 instances; Formlabs had 1 of 33. Coverage is the exception, not the rule,
   so always publish how many creatives were actually costable.

## The method

```
1. Eligible?        No disclosed band -> "not disclosed". Stop. Do not impute.
2. Point estimate   impressions = sqrt(band_lo * band_hi)      <- geometric mean
                    Open band ("1M+"): use band_lo, mark the result ">=".
3. Run length       active_days   = min(last, today) - first + 1
                    active_months = max(active_days, 7) / 30.44
4. Monthly rate     monthly_impr  = impressions / active_months
5. Cost             lo = monthly_impr/1000 * cpm_lo[format]
                    hi = monthly_impr/1000 * cpm_hi[format]
6. Message ads      Priced per SEND, not per impression. Skip the CPM path
                    entirely: sends ~ impressions, cost = sends * $0.30-1.00.
7. Aggregate        Sum lo and hi. Publish n_estimated and n_undisclosed
                    alongside the total, always.
```

### Why the geometric mean, not the midpoint

Bands are log-scaled (`10K-50K`, `50K-100K`, `500K-1M`) and impression
distributions across advertisers are roughly log-normal, so the mass sits toward
the low end of a band. For `10K-50K` the geometric mean is 22.4K against an
arithmetic midpoint of 30K, so the midpoint overstates by about 34%.

### Why divide by run length

This was the single largest error in the old method. It treated an ad's
**lifetime** impressions as one month's delivery. HP's drone webinar creative ran
Oct 2025 to Aug 2026; counting its whole-run impressions as monthly overstated it
by roughly 10x.

Linear division is the defensible default. LinkedIn's lifetime pacing varies day
to day and allows up to 100% over the daily budget on a given day, but that is
day-level variance, not systematic front-loading, and it averages out over a
month. There is no published LinkedIn pacing curve to calibrate a decay against,
so applying one would be invention. If you want to hedge, widen the interval
rather than reshaping the mean.

## Constants

CPM bands, US dollars per thousand impressions, B2B:

| Format | CPM low | CPM high |
|---|---|---|
| Single Image / Carousel | 24 | 55 |
| Document | 22 | 50 |
| Video / Event | 20 | 45 |
| Thought Leader | 15 | 38 |
| Text | 15 | 35 |
| Unknown | 20 | 55 |

Message / Conversation Ads: **$0.30 to $1.00 per send** (published figures
cluster near $0.81). Minimum daily budget on any format is $10.

**Source quality warning, and it matters.** Only LinkedIn's own Help pages are
authoritative, and they publish no rates. Every CPM, CPC and per-send figure
above comes from vendor or affiliate content with a commercial incentive to
inflate. Published sources disagree materially, for instance CPC at $5.50-8.00
versus a claimed $8-14 median. Treat the whole benchmark layer as
order-of-magnitude. The previous `$30-80` single band sat at the narrow-ABM end
and was applied to every format, which biased every figure upward.

Authoritative sources, checked 2026-09-22:
- https://www.linkedin.com/help/lms/answer/a1517918 (what the library shows)
- https://www.linkedin.com/help/lms/answer/a1620070 (impressions and targeting)
- https://www.linkedin.com/help/lms/answer/a422101 (budgets and pacing)

## How to report it

- Always a range, never a point. Anything tighter than roughly a factor of two
  is false precision: a ~5x-wide impression band times a ~2-3x CPM range.
- Always with coverage: "$24K-54K/mo, from 2 of 18 creatives with disclosed
  impressions."
- Always labelled `[Estimate]`, and described as derived, not reported.
- Prefer **share and direction over magnitude**. "Drones are 40% of HP's live ad
  volume" is a far stronger and better-evidenced claim than any dollar figure.

## What cannot be inferred, ever

1. **Total or global spend**, when most ads carry no disclosure. What you have is
   a floor built from the disclosed subset.
2. **Spend itself.** Never published. Every figure is modelled.
3. **Exact impressions** (banded) or exact per-country impressions (percentages
   are rounded, `<1%` below one).
4. **Instance count as a budget proxy.** There is no evidence for this and it is
   the most tempting mistake in the whole dataset. One creative can appear as
   many library entries across campaigns and ad sets, and duplicating a creative
   is operationally free. Instance count measures testing and targeting
   granularity. **Report it as its own metric and never multiply it by anything.**
5. **Whether an ad is still live.** An old `last_seen` is not proof of a pause.
6. **Google spend by business unit.** The parent domain mixes everything.
7. **A zero from a keyword search** as proof of absence.

## Worked examples, live ads read 2026-09-22

These are the regression cases in `tools/spend_model.py`; run it to check them.

| Ad | Disclosed | Derived |
|---|---|---|
| HP MJFNext teaser, Video, ran Mar 26 to Apr 13 | `500k-1M`, US 97% | $22.7K-$51.0K/mo |
| HP MJF 1200 reserve, Carousel, ran Jun 29 to Jul 19 | `30k-50k`, FR 41% ES 37% | $1.3K-$3.1K/mo |
| Formlabs Skyfall drone Message Ad, ran Aug 10 to Sep 7 | `<1k`, US 98% | $157-$525/mo, per-send |
| HP drone webinar, Document, ran Oct 2025 to Aug 2026 | none, no EU targeting | not disclosed |

The last row is the important one. It is HP's heaviest drone creative by
instance count, and it cannot be costed at all.
