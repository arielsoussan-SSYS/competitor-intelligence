# Competitive Ad Intelligence

Competitive advertising and account intelligence for Stratasys additive manufacturing,
built for the sales team.

**Live dashboard:** https://arielsoussan-ssys.github.io/competitor-intelligence/

Tracks what HP Additive, Formlabs, Bambu Lab and 3D Systems are advertising across
LinkedIn and Google, diffs each run against the last, and tracks which competitor is
already inside each of the 19 Drone Dominance Gauntlet II accounts. Publishes a dashboard
plus a one-page sales brief. Every output answers "what do I do with this on a call."

The dashboard has three sections: **Home** for the cross-competitor read, **Competitors**
for the per-competitor dashboards, and **Gauntlet** for account penetration.

## Start here

**Claude reads [`CLAUDE.md`](CLAUDE.md) automatically when you open a session in this
folder.** That file is the operating manual: setup requirements, collection rules,
verified advertiser names, honesty rules and current state. This README is the human
overview.

## How to run it, in one line

Open a Claude Code session **in this folder** and say **"scrape competitor ads"**.

> The session must be rooted here. This repo is gitignored inside the parent Stratasys
> workspace, so opening Claude Code at the workspace root will not find the skill.

### First time on a new machine

```bash
git clone https://github.com/arielsoussan-SSYS/competitor-intelligence.git
cd competitor-intelligence
```

Then check one thing before anything else: **the Claude for Chrome extension must be
installed and connected.** The entire collection phase drives your own browser through it.
Without it there is no scrape, though everything downstream still works. `python3` and
`git` are the only other requirements, and the dashboard builder uses the standard library
only, so there is nothing to install.

It is not automated by design: collection needs a live browser, so your machine has to be
on. Automating it means swapping the browser for an API-based scraper, which is a later
project.

## Collection rules that matter

These exist because breaking them has already produced wrong data:

- **Search by Company or advertiser, never by keyword.** Keyword tells you who is talking
  about a brand. Advertiser tells you what a company is running. Only the second belongs
  in the ad log.
- **Use the exact registered advertiser name.** Matching is loose. `3D Systems` returns 33
  ads belonging to a Croatian dental company and a branding agency; `3D Systems
  Corporation` returns the correct 1.
- **Run a control before recording any zero.** `?accountOwner=Formlabs` must return a
  count. A zero without a control is an unknown, not a finding.
- **Impressions and targeting are disclosed for EU-served ads only.** Find them with the
  `countries=` filter. This is the only way to tell a funded campaign from a message test.
- **Never quote an agency's total ad count as a competitor's.** ATREVIA's 124 ads and
  Sinointeractive's 100K are their whole client books, not HP's or Bambu's.

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

Claude reads the previous run from `data/`, collects through Ariel's Chrome, dedupes and
reconciles instance counts against each library's reported total, runs the EU disclosure
pass for impressions and targeting, diffs against the baseline, researches the Gauntlet
accounts, writes a new run file, rebuilds the dashboard and the sales brief, runs the
verification gate, and pushes.

**Cadence:** monthly is the defensible default for the ad log; weekly mostly re-reads the
same rotation. The Gauntlet account tracker is what rewards a faster cycle.

Because the skill is committed here, it is backed up, portable to any machine, and
available to Claude Code cloud routines, which run skills from the cloned repository.

## Coverage

| Tier | Competitors | Depth |
|---|---|---|
| 1 | HP Additive Manufacturing | Full ad log, Watch, diff, company research |
| 2 | Formlabs, Bambu Lab, 3D Systems | Ad log and diff |
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
| [LinkedIn Ad Library](https://www.linkedin.com/ad-library/) | Creatives, formats, CTAs, and for EU-served ads: run dates, impression bands, country split, targeting | Primary source. Search by advertiser via `?accountOwner=`. |
| [Google Ads Transparency](https://adstransparency.google.com/) | Ad counts by format, advertiser entities, last-shown dates | Isolable for Formlabs (one account) and Bambu (three), **not** for HP, where AM shares the corporate entity with consumer PCs. |
| Meta Ad Library | Active ads by keyword | **Out of scope by request.** Recorded as not checked, which is not the same as zero. |

Company intelligence comes from trade press, newsrooms, landing pages, and investor calls.

**Verified advertiser names.** Confirmed 2026-10-12. Re-confirm every run.

| Competitor | `?accountOwner=` | Live instances |
|---|---|---|
| HP Additive | `HP Additive Manufacturing (AM) Solutions - 3D Printing` | 34 |
| Formlabs | `Formlabs` | 27 |
| 3D Systems | `3D Systems Corporation` | 1 |
| Bambu Lab | no account exists | 0 |

## Rules that keep the numbers honest

- **One row equals one unique creative.** LinkedIn serves the same creative as many
  library entries. Unique creatives and live instances are reported separately, always.
- **Spend is a directional `[Estimate]`**, never a competitor's real budget, and it is
  derived rather than stored. `tools/spend_model.py` computes every dollar from the
  disclosed impression band (geometric mean, not midpoint), divided by the ad's real run
  length, times a format-specific B2B CPM. Message Ads are costed per send instead.
  LinkedIn discloses impressions **only for EU-targeted ads**, so most creatives cannot
  be costed at all and are reported as "not disclosed" rather than zero. Every total is
  published with its coverage, e.g. "from 2 of 18 creatives". See
  `.claude/skills/competitive-ad-scrape/references/spend-model.md`.
- **Absence of evidence is not evidence of absence.** "Not found in search", never "none".
- **Labels are mandatory:** `[Inference]` for reasoning, `[Unverified]` for uncorroborated
  claims, `[validation-needed]` for anything sales-facing that is not proven.
- **Corrections are logged, not quietly edited away.** When a run gets something wrong,
  the correction goes into that run file's `unverified` list so the record shows it.
- The verification gate reconciles theme, format, and funnel instance counts against the
  reported platform total before anything publishes. It has caught real errors, including
  a JavaScript syntax error that would have shipped a blank dashboard.

## Current snapshot

All four competitors carry real data. No pending stubs. Latest run **2026-10-12** (eight-day check after the Oct 4 scan).

**HP Additive, run 2026-10-12, baseline 2026-10-04**

| Metric | This run | Baseline |
|---|---|---|
| Unique creatives | 16 | 16 |
| Live instances | 34 | 34 |
| New / dropped | 0 / 0 | - |
| Drone share of volume | 35% (12 of 34) | 35% (12 of 34) |
| Stale dated creatives | 4 | 4 |
| Est. monthly rate, costable ads | $24.0K to $54.1K/mo `[Estimate]`, from 2 of 16 creatives | same 2 ads |
| EU-served creatives | 2 of 34 | 2 of 34 |

**Headline:** HP changed nothing on LinkedIn in eight days, and the MJF 1200 Open House ad is
still running 11 days after the event.

**Formlabs, run 2026-10-12, baseline 2026-10-04**

| Metric | This run | Baseline |
|---|---|---|
| Unique creatives / live instances | 12 / 27 | 12 / 28 |
| Google ads, own account | 119 (99 Text / 12 Image / 8 Video) | 121 (99 / 14 / 8) |
| Drone-specific creative | 4 of 27 | 4 of 28 |
| EU-served creatives | 1 of 27 | 1 of 28 |

**Headline:** Same 12 creatives, one fewer instance. The LinkedIn pullback has paused.

**Bambu Lab, run 2026-10-12, baseline 2026-10-04**

| Metric | This run |
|---|---|
| LinkedIn owned ads | **0** (verified, 5 name variants + control) |
| Google ads, own account | ~1,800 carried from Oct 4, not re-pulled (domain page shows ~3K across accounts) |
| Defense addressable market | Zero, NDAA FY2026 s849 and s880 |

**Headline:** Still no B2B advertising. Litigation and product news not re-checked this run.
Legally sensitive, route to Legal.

**3D Systems, run 2026-10-12, baseline 2026-10-04**

Still zero marketing creative on LinkedIn (one recruitment ad). 35 Google ads on 3dsystems.com,
unchanged. The US corporate Google account (9 ads) was not re-sampled this run.

**Gauntlet tracker, updated 2026-10-12**

No tracker upgrades. 17 of 19 teams are `Confirmed`. One account is `Locked` (ORQA US LLC,
Formlabs) and two are `Contested` (Neros, Skycutter). Vector's printing and Hyperscale's
metal-AM claims are single-source `[Unverified]`. Gauntlet 2.5 still only scheduled.

> Bambu's chart buckets use **Google** counts, not LinkedIn instances, because they have
> no LinkedIn programme. Every run file carries a `bucket_basis` string stating its
> denominator, and the dashboard prints it above the charts.

## Tech

Single self-contained HTML file, one dependency (Chart.js from CDN), GitHub Pages. No
backend, no build step for viewers, no browser storage. Light theme only, by request:
the dashboard is used in meetings and on shared screens.

Collection runs through the `claude-in-chrome` connector against Ariel's own browser.
That is the reason this is not yet automated, and the thing to replace first if it ever
should be.

---

Internal use, Stratasys marketing and sales.
