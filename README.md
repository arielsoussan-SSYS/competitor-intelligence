# HP Ad Intelligence Dashboard

Live competitive ad tracking for Stratasys additive manufacturing. **HP Additive Manufacturing only.**

**Live dashboard:** https://arielsoussan-ssys.github.io/competitor-intelligence/

> **Scope change, Aug 10 2026:** Formlabs and Bambu Lab were removed from this tracker. Prior multi-competitor comparison tabs were replaced by HP-over-time views. The `competitive-ad-scrape` skill was rewritten to match.

## What's Inside

Single-file HTML dashboard (no backend, no build step).

**Pinned at the top, above everything else:**

- **Key Headline This Week** plus a one-line "so what" for Stratasys
- **What Changed This Week at HP** in four fixed categories: ad-level changes, company/market moves, messaging/positioning shift, landing page/funnel changes. Every entry carries a source link.

**Tabs:**

- **Dashboard** - KPI cards, four Chart.js visualizations (theme mix, format mix, funnel distribution, estimated spend by theme), plus a table of creatives dropped since the last run
- **Ad Log** - 18 unique HP creatives across 17 fields. Searchable. New-this-week creatives flagged.
- **Messaging Themes** - Theme, creative count, live instances, sample headline, funnel position, and which buying committee role each theme addresses
- **HP Watch** - Product, the MJF 1200 Early Access mechanic, drones/UAV/defense, earnings and exec, channel, competitive field, and an explicit unverified/refuted section
- **Collection Notes** - Methodology, spend estimation, known limitations

## Data Sources

| Source | What We Capture | Current state |
|---|---|---|
| [LinkedIn Ad Library](https://www.linkedin.com/ad-library/) | Ads, impression ranges, formats, CTAs | 37 live instances, 18 unique creatives |
| [Meta Ad Library](https://www.facebook.com/ads/library/) | Active ads by keyword | Zero HP-owned ads. Recorded as a finding. |
| [Google Ads Transparency](https://adstransparency.google.com/) | Ad counts, formats, landing pages | ~50K on hp.com, AM not isolable from parent entity |

HP Watch is sourced from trade press, HP newsroom, HP landing pages, and investor calls.

## Weekly Change Detection

Each run diffs against the previous run's dataset, matching on headline plus platform:

- Present now, absent before = **new**
- Present before, absent now = **dropped or paused**
- Changed CTA, format, or spend band = **changed**

Company-level moves are researched over the trailing 7 days only. Claims without a direct source are labelled `[Unverified]` or `[Inference]`.

## Spend Estimation

Directional estimates, not verified actuals. Do not present as HP's real budget.

- LinkedIn: impression range midpoint x B2B CPM ($30-$80)
- Google Search: estimated impressions x CPC ($1-$5)
- Google Display: estimated impressions x CPM ($5-$15)
- Meta: estimated reach x CPM ($10-$30)

## Deduplication Rule

One Ad Log row = one unique creative. LinkedIn serves the same creative as multiple separate library entries; instance counts live in the Notes column. Instance totals and unique-creative totals are reported separately because they are not interchangeable.

## Updating the Dashboard

A Cowork skill (`competitive-ad-scrape`) automates the full run. In any Claude Cowork session:

> "scrape competitor ads" or "update ad intelligence" or "HP ad watch"

Claude re-scrapes all three ad libraries, refreshes HP Watch, diffs against the prior run, and regenerates both the dashboard and `hp-ad-intelligence.xlsx`.

To deploy: replace `index.html` in this repo (Add file > Upload files > Commit), or commit from your local clone.

## Tech Stack

- Single HTML file, one dependency: [Chart.js CDN](https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js)
- GitHub Pages
- Data embedded as a JavaScript object. No database, no API calls, no browser storage.

## Current Snapshot (Aug 10 2026)

| Metric | This week | Baseline Aug 4 |
|---|---|---|
| Unique creatives | 18 | 14 |
| Live ad instances | 37 | not recorded |
| New creatives | 4 | - |
| Dropped creatives | 3 | - |
| Drone / UAV share of ad volume | 38% (14 of 37) | 3 of 14 creatives |
| Est monthly spend | $35K-$94K | $26K-$68K |
| Platforms in use | LinkedIn only | LinkedIn only |

**Headline:** HP added two new drone creatives this week. Drone and UAV work is now 38% of HP's live LinkedIn ad volume.

## Repository Structure

```
index.html          # The complete dashboard (self-contained)
README.md           # This file
```

## License

Internal use, Stratasys marketing team.

---

Built with Claude Cowork | Data: August 10, 2026 | Next refresh: Monday August 17, 2026
