# CLAUDE.md

Read this before doing anything in this repo. It is the operating manual; `README.md` is
the human-facing overview.

## What this is

Competitive advertising and account intelligence for Stratasys additive manufacturing.
It tracks what HP Additive, Formlabs, Bambu Lab and 3D Systems are advertising, diffs
each run against the last, and tracks which competitor is already inside each of the 19
Drone Dominance Gauntlet II accounts. It publishes a dashboard and a one-page sales brief
per competitor.

**Live dashboard:** https://arielsoussan-ssys.github.io/competitor-intelligence/
**Repo:** `arielsoussan-SSYS/competitor-intelligence`, GitHub Pages from `main`, files at root.

**Audience is the Stratasys sales team**, not marketing analysts. Every output answers
"what do I do with this on a call." An observation with no sales consequence does not ship.

This is Ariel's flagship visibility project, in his own words the one that "will put me on
the map." Treat it as high-stakes work, not a side utility. Ariel is a **marketer, not a
developer** — explain technical steps in plain language and prefer doing the technical
work over handing him instructions to run.

## The one command

Say **"scrape competitor ads"** (or "update ad intelligence", "run the competitor scan",
"what changed this week"). That invokes the `competitive-ad-scrape` skill in
`.claude/skills/`, which runs the whole pipeline end to end and is pre-authorised to
publish.

**The skill only loads if the Claude Code session is rooted in this folder.** Opening
Claude Code at the workspace root will not find it, because this repo is gitignored
inside the parent workspace. Open Claude Code *here*.

## Before the first run on a new machine

| Need | Why | Check |
|---|---|---|
| **Claude for Chrome extension**, connected | The entire collection phase drives Ariel's own browser through the `claude-in-chrome` connector. Without it there is no scrape. | Ask Claude to run `ToolSearch` for `mcp__claude-in-chrome__navigate`. If it is missing, stop and fix this first. |
| `python3` | Builds the dashboard. **Stdlib only**, works on 3.9+. No pip install needed. | `python3 tools/build_dashboard.py` |
| `git` push access | Publishing is a push to `main`. | `git push` |
| Node | **Only** for building slide decks. Not needed for a scan. | optional |

Everything else travels in this repo. There are no machine-specific paths.

## Architecture rule, do not break it

**`data/*.json` is the asset. `index.html` is a generated view.**

- Never hand-edit `index.html`. Rebuild it: `python3 tools/build_dashboard.py`
- Never embed the dataset inside `index.html`. That was the old design; it made the
  published page the only copy of the data and forced each run to scrape its own dashboard
  to find a baseline.
- Never create a per-competitor HTML page. Tiering exists to prevent that.
- Write the run file to `data/` **before** rendering. If a run dies halfway, the data must
  already be on disk.

## Collection rules that are not negotiable

These exist because breaking each one has already produced wrong data in this repo.

1. **Use Ariel's Chrome via the `claude-in-chrome` connector.** Not the sandbox browser.
2. **Search by Company or advertiser, never by keyword.** Keyword answers "who is talking
   about this brand." Advertiser answers "what is this company running." Only the second
   belongs in the ad log. Keyword results go in `partner_ads` and nowhere else.
3. **Use the URL parameter, not the form.** `?accountOwner=<Exact Name>` works reliably;
   the form's Search button intermittently returns "Failed to load" for every query.
4. **Use the exact registered advertiser name** from the table below. Matching is loose,
   so a short name silently returns a different company's ads.
5. **Run the control before recording any zero.** `?accountOwner=Formlabs` must return a
   count. A zero without a passing control is an unknown, not a finding.
6. **Confirm advertiser identity in the results,** not just the count.
7. **Run the EU disclosure pass.** Impressions, run dates, country split and targeting are
   disclosed only for EU-served ads. Find them with `&countries=DE,FR,NL,IT,ES,IE,SE,PL`.
   This is the only way to tell a funded campaign from a message test.

### Verified advertiser names

Confirmed 2026-08-25. Re-confirm every run and update this table.

| Competitor | `?accountOwner=` | Live instances | Warning |
|---|---|---|---|
| HP Additive | `HP Additive Manufacturing (AM) Solutions - 3D Printing` | 36 | `HP Additive` also resolves correctly |
| Formlabs | `Formlabs` | 38 | clean, use as the control |
| 3D Systems | `3D Systems Corporation` | 1 | **`3D Systems` returns 33 ads that are NOT them** (3D Dental Systems d.o.o., FGS Media) |
| Bambu Lab | no account exists | 0 | **`Bambu` returns 237 ads that are all Bambuser**, unrelated |

**Never quote an agency's total ad count as a competitor's.** ATREVIA COMUNICACIÓN SL
(124 ads) and Sinointeractive (100K ads) are their whole client books, not HP's or Bambu's.
The same trap applies to HP's ~50K Google total, which cannot be split from consumer printers.

## Honesty rules

- **One row is one unique creative.** Ad libraries serve the same creative as many entries.
  Unique creatives and live instances are reported separately, always, and are not
  interchangeable.
- **Spend is always `[Estimate]`.** Impression bands come from the platform; the dollar
  conversion is ours and the range is wide by construction. Never present it as a
  competitor's real budget.
- **`[Inference]`** for reasoning, **`[Unverified]`** for uncorroborated advertiser claims,
  **`[validation-needed]`** for anything sales-facing that is not proven.
- **"Not found in search", never "none."** Absence of evidence is not evidence of absence.
  Meta is currently out of scope and recorded as *not checked*, which is not the same as zero.
- **Corrections stay in the record.** When a run gets something wrong, log the correction in
  that run file's `unverified` list rather than quietly editing it away.
- **Baseline runs carry no "NEW this week" flags.** Nothing can be new when there is no
  prior week to compare against.
- The **verification gate in SKILL.md Phase 7 is not optional.** It has caught real
  arithmetic errors and a JavaScript syntax error that would have shipped a blank dashboard.

## Reference files

All in `.claude/skills/competitive-ad-scrape/references/`:

| File | What it holds |
|---|---|
| `collection.md` | Source-by-source tradecraft. Read before any scraping. |
| `standing-facts.md` | Carry-forward intel per competitor, and known bad claims. **Verify, do not re-derive.** |
| `competitors.md` | Who is tracked, at what depth, and why |
| `schema.md` | The 17-field ad record, verbatim. Do not invent fields. |
| `spend-model.md` | CPM/CPC constants, impression bands, format efficiency |
| `creative-rubric.md` | How to score creative quality, including ours |
| `context.md` | Why this exists, stakeholders, what marketing already has running, hard-won lessons |

## Cadence

**Monthly is the defensible default for the ad log.** Weekly mostly re-reads the same
rotation. Run weekly only while a launch or live campaign makes it worth it, and say which
mode a run is in. The **Gauntlet account tracker is what rewards a faster cycle**, because
that is where things actually move.

## Publishing

Publishing is pre-authorised. `git add -A && git commit && git push`, then confirm the
live site. Commit messages: what changed and why, in plain English.

> A previous Cowork sandbox blocked `git push`, which forced a gzip/base64 injection into
> GitHub's web editor. That workaround corrupted a character on the Aug 10 2026 run. It is
> gone. If a push ever fails, fix the environment. Do not rebuild the injection path.

## Where things stand

Current as of 2026-08-25. All four competitors carry real data; there are no pending stubs.

- **HP Additive** — 18 creatives, 36 live instances. Buys launch bursts, not always-on
  presence: one MJF 1200 teaser took 500K-1M impressions in nineteen days.
- **Formlabs** — ships the Fuse X1 in Q4 2026, ahead of HP's early-2027 MJF 1200. The
  nearest-term threat, and the one we had not planned for.
- **Bambu Lab** — buys zero LinkedIn advertising. NDAA FY2026 §849/§880 bar them from
  defense entirely, which makes every Bambu machine on a defense floor a forced replacement.
- **3D Systems** — third consecutive run at zero marketing creative.
- **Gauntlet** — 19 accounts, 16 confirmed. ORQA is `Locked` to Formlabs; Neros and
  Skycutter are `Contested`.

### Open items

- **Meta** is out of scope by Ariel's decision. Recorded as not checked.
- **"HP supports 14 of 19"** remains `[validation-needed]`. No public evidence, which is
  the *expected* result since supplier relationships are not published. Do **not** record it
  as refuted, and do not cite the figure externally. The cheapest route to validating it is
  the field team, not the internet.
- **Creative rubric** has not yet been applied to Stratasys's own ads.
- **Automation** is deliberately deferred. Collection needs a live browser, so cloud
  routines cannot run it as built. Automating means swapping the browser for an API-based
  scraper. Do not attempt this without asking first.

## Legally sensitive

**Stratasys is in active litigation with Bambu Lab.** Summarise status factually if asked,
never characterise the case or predict outcomes, and route every customer-facing question
to Legal. This applies to anything published from this repo.
