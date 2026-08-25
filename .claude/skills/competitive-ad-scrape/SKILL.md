---
name: competitive-ad-scrape
description: Run the weekly additive-manufacturing competitive ad intelligence scan and rebuild the dashboard. Use when the user says "scrape competitor ads", "update ad intelligence", "refresh ad data", "pull HP ads", "ad library scrape", "HP ad watch", "competitive ad update", "competitor scan", "what changed this week", or asks for the weekly competitive ad report. Covers LinkedIn Ad Library, Meta Ad Library, and Google Ads Transparency Center, diffs against the previous run, and publishes the dashboard, workbook, and sales brief.
---

# Competitive ad intelligence: scrape, diff, build, publish

End-to-end weekly run. Audience is the Stratasys sales team.

Run the whole pipeline without stopping to ask permission at each step. Publishing is
pre-authorized. Stop only if a verification gate fails.

**Every output answers "what do I do with this on a call."** An observation with no
sales consequence does not ship.

## Read first

- `references/competitors.md` — who is tracked, at what depth, and why
- `references/standing-facts.md` — carry-forward intel and refuted claims. **Verify, do not re-derive.**
- `references/collection.md` — source-by-source tradecraft. Saves an hour of rediscovery.
- `references/schema.md` — the 17-field record, verbatim. Do not invent fields.
- `references/spend-model.md` — CPM/CPC constants

Deliverables, into the repo:

| File | What |
|---|---|
| `data/YYYY-MM-DD-<slug>.json` | The run dataset. **The asset.** |
| `index.html` | Dashboard, published to GitHub Pages |
| `briefs/YYYY-MM-DD-sales-brief.md` | One page, for sales |
| `ad-intelligence.xlsx` | Workbook, for anyone who wants to filter and sort |
| `README.md` | Snapshot table refreshed |

Live site: https://arielsoussan-ssys.github.io/competitor-intelligence/
Repo: `arielsoussan-SSYS/competitor-intelligence`, Pages from `main`, files at root.

---

## Phase 1: baseline

List `data/`, load the most recent file per competitor in scope. Note its `run_date`.
That is the comparison set.

If no prior file exists for a competitor, this is a **baseline run**: collect normally,
report no diff, label the run `baseline`.

> Baseline used to be recovered by scraping the published dashboard, because the dataset
> lived inside `index.html`. It no longer does. Do not parse the live site for data.

---

## Phase 2: collect

Per competitor, in tier order. Follow `references/collection.md` for each source.

**LinkedIn** — primary and the only reliable creative-level source.
**Meta** — keyword search. **Zero results is a finding**, recorded explicitly, never omitted.
**Google** — parent-domain totals are not isolable by business unit. Say so. The real
signal is `jumpid` campaign codes on trade-site display banners; a new code means a
newly funded flight.

Record only what you observed. Reasoning is `[Inference]`. Advertiser claims that are
uncorroborated are `[Unverified]`. Spend is `[Estimate]`. Every claim carries a source link.

---

## Phase 3: dedupe and count

**One row = one unique creative.** LinkedIn lists the same creative many times. Collapse
them; put "N instances" in `notes`.

Count instances by hand and make them sum to the reported total. Report unique creatives
and live instances as two separate numbers, always. Conflating them has produced false
week-over-week swings.

---

## Phase 4: research the trailing 7 days

Run in parallel with Phase 2/3. Cover: product/pricing/availability news; partnerships,
events, verticals; drone/UAV/defense; orthotics and prosthetics; metal and sintering;
earnings, exec changes, hiring; channel and reseller changes; landing page and offer changes.

Require a source URL and publication date for every claim, separate last-7-days from
older context, and flag anything unconfirmed.

**Also update the account watch.** Research whether any competitor has gained a foothold
in a target account. Move at least one entry in `data/account-watch.json` from
`[Unverified]` toward `Confirmed` or `Refuted`. This is the highest-value output of the
scan, because it is the one thing advertising data alone cannot tell you.

---

## Phase 5: diff and headline

Match on `headline` + `platform`:

| Condition | Status |
|---|---|
| Absent in baseline | `NEW this week` |
| Absent now | `Dropped` — dropped table, not the ad log |
| Same headline, changed CTA/format/spend band | `Changed` — name the field that moved |
| Otherwise | `Carried over` |

Instance-count movement on a carried-over creative is a change in **weight**, not status.
Note it; do not mark the creative changed.

**Key headline this week**: one sentence, ~20 words, the single most important thing that
happened. Plus a one-line "so what" for Stratasys, tied to live programs where honest.
No hype language.

**What changed**, four fixed categories, every entry sourced: ad-level changes;
company/market moves; messaging/positioning shift; landing page/funnel changes.

Always call out **stale creative** and how long it has been running. See
`references/standing-facts.md`.

---

## Phase 6: write data, then build

Write `data/YYYY-MM-DD-<slug>.json` **first**. If a run dies halfway, the data must
already be on disk. The dashboard is a view of the data, never the other way round.

**index.html** — single file, Chart.js from cdnjs only, no localStorage, navy `#1f3864`
and red `#c8102e`. Header with week label, run date, baseline date. Pinned weekly card
above the KPIs: red top border, headline at 24px, amber "so what" box, then the four
change categories as a colour-coded grid with source links. Tabs: Dashboard (6 KPI cards,
4 charts — theme mix horizontal bar with top theme in red, format mix doughnut, funnel
bar, spend-by-theme grouped bar — plus the dropped-creatives table), Ad Log (searchable,
NEW badges, funnel tags), Messaging Themes, Watch (source link per bullet, explicit
"Unverified and refuted" section), Collection Notes. Escape all interpolated strings.
Write LF line endings; confirm with `file index.html`.

**ad-intelligence.xlsx** — openpyxl, Arial. Tabs: Weekly Change Log (newest at top),
Ad Log (17 columns, navy header, auto-filter, frozen top row, green fill on NEW rows,
real `SUM`/`COUNTIF` formulas never hardcoded results), Summary (this week vs baseline
vs change, plus numbered "what this means for Stratasys"), Messaging Themes,
Collection Notes.

If LibreOffice recalc hangs, kill it rather than retrying, verify formula ranges cover
exactly the data rows, cross-check against a Python-side computation, and say in the
summary that recalc did not complete.

**briefs/YYYY-MM-DD-sales-brief.md** — one page maximum. For most reps this is the only
thing they will read.

1. The one thing to know this week, in a sentence
2. What they will hear from prospects, with the counter for each
3. Where the competitor is vulnerable — stale creative, missing verticals, unproven
   claims, slipped ship dates
4. Where we are exposed — messaging ground they are taking that we consider ours. Say it
   plainly, do not soften it.
5. Accounts to look at — every `Contested` account from the account watch

---

## Phase 7: verify before publishing (gate — do not skip)

1. **Arithmetic reconciliation.** Theme, format, and funnel instance counts must each sum
   to the reported platform total. KPI spend totals must equal the sum of ad-level bands.
   Every percentage in prose must recompute from its stated denominator.
   *This caught three inconsistencies on the Aug 10 run. It is not optional.*
2. **Scope.** Every competitor present in the output is in `references/competitors.md`,
   at the depth its tier specifies.
3. **No placeholders.** `grep -o '__[A-Z]*__'` returns nothing.
4. **No stale numbers** carried from an earlier draft.
5. **JS valid.** Extract the script block, stub `Chart`/`document`, `node --check`.
6. **Tags balanced** for div, section, table, ul, li, tr, td.
7. **Sourcing.** Every factual claim has a URL. Inference, unverified, and estimate
   labels applied.
8. **Data file parses** and its counts match the rendered dashboard.

---

## Phase 8: publish

```bash
git add -A && git commit -m "<Competitor> tracker: <Mon DD YYYY> scrape" && git push
```

Commit body: the headline plus the bullet summary of changes.

> The Cowork sandbox blocked `git push` (HTTP 403 on CONNECT to github.com), which forced
> a gzip/base64/chunk/SHA-verify injection into GitHub's CodeMirror web editor. That
> workaround corrupted a character on the Aug 10 run. It is gone. In Claude Code, GitHub
> traffic uses a dedicated proxy independent of the network policy. If a push ever fails,
> fix the environment; do not rebuild the injection path.

---

## Phase 9: verify live

Confirm the new commit on `main`. Wait 45-60s for Pages. Load the live site. Confirm
programmatically that the four canvases actually painted (sample `getImageData` alpha),
that the Ad Log row count matches the unique creative count, and that tabs switch.

Write `Last successful scan: <date>` into the footer. A run that completes without
collecting is worse than one that fails loudly, because stale data reads as current.

---

## Phase 10: report

The headline, the four change categories in brief, unique creatives and live instances
per competitor, new/dropped/changed counts, any source that returned nothing, the live
URL, the commit SHA, and everything labelled `[Unverified]`.

---

## Style

Terse, bullets over prose. No em dashes, plain punctuation only. No hype words. Frame
around buying committees, multi-touch cycles, and pipeline language rather than vanity
metrics. Mark speculation `[Inference]`, unconfirmed claims `[Unverified]`, spend
`[Estimate]`. Zero results are findings, not failures.

Spend figures are directional and never presented as a competitor's real budget.
Absence of evidence is not evidence of absence: say "not found in search", not "none".
Do not paste competitor ad copy into anything customer-facing — summarize the claim and
counter it.
