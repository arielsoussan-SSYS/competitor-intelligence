# Competitive Ad Intelligence

Weekly competitive advertising intelligence for Stratasys additive manufacturing, built
for the sales team.

**Live dashboard:** https://arielsoussan-ssys.github.io/competitor-intelligence/

Tracks what competitors are advertising across LinkedIn, Meta, and Google, diffs each run
against the last, and publishes a dashboard plus a one-page sales brief. Every output
answers "what do I do with this on a call."

## How it is put together

```
data/                       # the asset: one JSON file per competitor per run
data/gauntlet.json          # the 19 Gauntlet II companies, tracked as prospects
tools/build_dashboard.py    # renders index.html from the latest run file
index.html                  # published dashboard (generated, do not hand-edit)
briefs/                     # one-page sales brief per run
.claude/skills/             # the competitive-ad-scrape skill that runs the whole thing
```

**Data is separate from presentation.** Until Aug 2026 the dataset lived inside
`index.html` as a JavaScript object, which made the published page the only copy, forced
each run to scrape its own dashboard to find the baseline, and put the history at risk
on every render change. Run files are now the asset and the dashboard is a view of them.

Rebuild the dashboard after editing a data file:

```bash
python3 tools/build_dashboard.py
```

## Running a scan

The skill lives in `.claude/skills/competitive-ad-scrape/`. From a Claude Code session in
this repo, say **"scrape competitor ads"**, "update ad intelligence", or "HP ad watch".

Claude reads the previous run from `data/`, collects from all three ad libraries, dedupes
and reconciles the counts, diffs against the baseline, writes a new run file, rebuilds
the dashboard and the sales brief, runs the verification gate, and pushes.

Because the skill is committed here, it is backed up, portable to any machine, and
available to Claude Code cloud routines, which run skills from the cloned repository.

## Coverage

| Tier | Competitors | Depth |
|---|---|---|
| 1 | HP Additive Manufacturing | Full ad log, Watch, diff, company research |
| 2 | 3D Systems, Formlabs, Bambu Lab | Ad log and diff |
| 3 | Drone Gauntlet field, UxS suppliers | Account penetration watch, no ad scraping |

Tier 3 answers a sales question rather than a marketing one: **which companies we want to
sell into does a competitor already have a foothold in?** Accounts carry a displacement
posture of `Open`, `Contested`, or `Locked`. Contested accounts surface into every brief.

The **Gauntlet** section tracks the 19 companies advancing to Drone Dominance Gauntlet II
(Fort Carson, August 2026, from a $1.1B program). Each must deliver 120 drones in roughly
five weeks, which is the additive manufacturing pitch restated as a procurement
requirement. Researched from public sources only: company sites, press releases, executive
social posts, trade press.

## Navigation

**Home** gives the cross-competitor read and the signals worth acting on.
**Competitors** holds a full dashboard per competitor.
**Gauntlet** holds the drone prospect field.

## Data sources

| Source | What we capture | Reality |
|---|---|---|
| [LinkedIn Ad Library](https://www.linkedin.com/ad-library/) | Creatives, impression bands, formats, CTAs | Primary source. The only reliable creative-level data. |
| [Meta Ad Library](https://www.facebook.com/ads/library/) | Active ads by keyword | Zero HP-owned ads. Recorded as a finding, not a failure. |
| [Google Ads Transparency](https://adstransparency.google.com/) | Ad counts, formats, landing pages | Not isolable by business unit. Real signal is `jumpid` campaign codes on trade-site banners. |

Company intelligence comes from trade press, newsrooms, landing pages, and investor calls.

## Rules that keep the numbers honest

- **One row equals one unique creative.** LinkedIn serves the same creative as many
  library entries. Unique creatives and live instances are reported separately, always.
- **Spend is a directional `[Estimate]`**, never a competitor's real budget. Impression
  figures are bands, so midpoint arithmetic compounds error.
- **Absence of evidence is not evidence of absence.** "Not found in search", never "none".
- **Labels are mandatory:** `[Inference]` for reasoning, `[Unverified]` for uncorroborated
  claims, `[validation-needed]` for anything sales-facing that is not proven.
- The verification gate reconciles theme, format, and funnel instance counts against the
  reported platform total before anything publishes. It has caught real errors.

## Current snapshot

**Formlabs, run 2026-08-25 — baseline run, no prior data.**

| Metric | This run |
|---|---|
| Unique creatives | 15 |
| Live instances (LinkedIn) | 38 |
| Drone share of volume | 11% (4 of 38) |
| Funnel mix | 68% top (26 of 38) |
| Est monthly LinkedIn spend | $18.5-66.6K `[Estimate]` |
| Google, own advertiser account | 106 ads (88 Text / 10 Image / 8 Video) |
| Platforms checked | LinkedIn, Google. Meta out of scope this run. |

**Headline:** Formlabs is selling large-format industrial SLS into drone manufacturing,
and it ships the Fuse X1 in Q4 2026, ahead of HP's MJF 1200 in early 2027.

**Bambu Lab, run 2026-08-25 — baseline run, no prior data.**

| Metric | This run |
|---|---|
| LinkedIn owned ads | **0** (verified, 5 name variants + control) |
| Google ads, own account | 1,700 (700 Text / 600 Image / 400 Video) |
| Google ads, all Bambu entities | ~2,100 |
| Third-party LinkedIn mentions | 75 ads across 45 advertisers |
| Defense addressable market | Zero, NDAA FY2026 s849 and s880 |
| Platforms checked | LinkedIn, Google. Meta out of scope this run. |

**Headline:** Bambu buys no B2B advertising at all. The threat is price and volume, not
marketing. NDAA FY2026 bars them from defense entirely, which makes every Bambu printer
on a defense floor a forced replacement.

> Bambu's chart buckets use **Google** counts, not LinkedIn instances, because they have
> no LinkedIn programme. Every run file carries a `bucket_basis` string stating its
> denominator, and the dashboard prints it above the charts.

**HP Additive, run 2026-08-18, baseline 2026-08-10.**

| Metric | This run | Baseline |
|---|---|---|
| Unique creatives | 18 | 18 |
| Live instances | 36 | 37 |
| New / dropped | 1 / 1 | - |
| Drone share of volume | 39% (14 of 36) | 38% (14 of 37) |
| Est monthly spend | $35-94K `[Estimate]` | $35-94K |
| Platforms in use | LinkedIn only | LinkedIn only |

**Headline:** HP held steady on volume. The drone share increase is a denominator effect,
not growth: the absolute drone count did not move.

**Gauntlet tracker, updated 2026-08-25.** All 19 Gauntlet II teams carry location,
financial backing, production scale, technology and a sales hook. 14 of 19 are now
`Confirmed`, up from 1. One account is `Locked` (ORQA US LLC, Formlabs installed and
case-studied) and two are `Contested` (Neros, Skycutter).

3D Systems last ran 2026-08-18. All four tracked competitors now have real data; there
are no `pending` stubs left.

## Tech

Single self-contained HTML file, one dependency (Chart.js from CDN), GitHub Pages. No
backend, no build step for viewers, no browser storage. Light theme only, by request:
the dashboard is used in meetings and on shared screens.

---

Internal use, Stratasys marketing and sales.
