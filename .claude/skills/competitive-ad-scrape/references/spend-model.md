# Spend estimation

Directional estimates only. Always labelled `[Estimate]`. Never presented as a
competitor's actual budget, in the dashboard or in anything sales-facing.

## Constants

| Platform | Method | Rate |
|---|---|---|
| LinkedIn | impression range midpoint x B2B CPM | $30 - $80 CPM |
| Google Search | estimated impressions x CPC | $1 - $5 CPC |
| Google Display | estimated impressions x CPM | $5 - $15 CPM |
| Meta | estimated reach x CPM | $10 - $30 CPM |

Every ad record carries `lo` and `hi`. Report a range; never report a point estimate.

## Impression band to monthly spend

Source: ZenABM, *LinkedIn Ad Library* guide. Uses the same $30-80 B2B CPM.

| Impression band | Est. monthly spend | Read as |
|---|---|---|
| Under 1K | Under $80 | A test, not a campaign |
| 1K - 5K | $80 - $400 | Small |
| 10K - 50K | $800 - $4,000 | Real budget commitment |
| 500K+ | $40,000+ | Enterprise-level |

**Weight by format before summing.** A flat per-instance estimate is wrong, because
formats differ by roughly 5x on cost. Benchmarks from the same source, drawn from
2,828 ads across 211 companies:

| Format | CTR | CPC |
|---|---|---|
| Thought Leader Ad | 2.68% | $3.06 |
| Single Image | 0.42% | $13.23 |
| Video | 0.24% | $15.61 |

Thought Leader Ads get roughly **6x the CTR at a fifth of the cost per click**. That
changes the read on a competitor's mix, not just their total: a competitor leaning on
TLAs is buying attention far more efficiently than one leaning on video. Formlabs runs
4 Thought Leader instances fronted by their CRO; note that as efficiency, not vanity.

These are third-party medians, not measured competitor data. Label `[Estimate]` and do
not present them as any competitor's actual performance.

## Known limitations, restate every run

- Impression figures are **bands**, not counts. Midpoint arithmetic compounds that error.
- Google spend on a parent domain cannot be split by business unit. Report the total
  and say it is not isolable.
- A keyword search returning nothing does not prove absence of advertising.
- Some first-seen dates are inferred from creative content rather than reported.
- **Impressions are only disclosed for ads served in the EU.** For US-only ads the band
  is genuinely absent, so `impr` is "Not disclosed" and the spend estimate rests on
  instance count and format alone. Say which basis was used.
- Instance counts move with ad rotation, which is not the same as budget moving.

## Reading the output

The useful signal is **direction and mix**, not magnitude. "Drone share of live
instances rose from 21% to 38%" is defensible. "HP spends $94K a month" is not.
