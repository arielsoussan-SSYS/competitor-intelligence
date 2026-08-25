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

## Known limitations, restate every run

- Impression figures are **bands**, not counts. Midpoint arithmetic compounds that error.
- Google spend on a parent domain cannot be split by business unit. Report the total
  and say it is not isolable.
- A keyword search returning nothing does not prove absence of advertising.
- Some first-seen dates are inferred from creative content rather than reported.
- Instance counts move with ad rotation, which is not the same as budget moving.

## Reading the output

The useful signal is **direction and mix**, not magnitude. "Drone share of live
instances rose from 21% to 38%" is defensible. "HP spends $94K a month" is not.
