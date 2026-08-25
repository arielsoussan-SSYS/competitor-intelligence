# Data schema

## Ad record — 17 fields, exact

Field names are load-bearing: the dashboard renderer and every historical file in
`data/` use these keys. Do not rename, add, or drop fields without migrating history.

| Field | Type | Meaning |
|---|---|---|
| `platform` | string | LinkedIn / Meta / Google |
| `format` | string | Video, Single Image, Carousel, Document |
| `theme` | string | Messaging theme, from the theme taxonomy |
| `headline` | string | Ad text plus headline, joined by ` / `. Diff key. |
| `cta` | string | Button text: Learn More, Register, Sign Up, Book a Meeting |
| `impr` | string | Impression band as the library reports it, e.g. `10K-50K` |
| `lo` | number | Low estimated monthly spend, USD |
| `hi` | number | High estimated monthly spend, USD |
| `first` | string | First seen, `Mon YYYY` |
| `last` | string | Last seen, `Mon YYYY` |
| `active` | string | Yes / No |
| `audience` | string | Inferred buying-committee roles targeted |
| `funnel` | string | Top / Mid / Bottom |
| `url` | string | Landing page |
| `owner` | string | e.g. `HP-owned`, `Partner-owned` |
| `status` | string | `NEW this week` / `Carried over` / `Changed` / `Dropped` |
| `notes` | string | Instance count, staleness flags, tags, context |

## Run file

`data/YYYY-MM-DD-<slug>.json`

```json
{
  "competitor": "HP Additive Manufacturing",
  "slug": "hp",
  "run_date": "2026-08-18",
  "baseline_date": "2026-08-10",
  "sources": {
    "linkedin": { "checked": true, "unique_creatives": 18, "live_instances": 36 },
    "meta":     { "checked": true, "ads": 0, "note": "Not found in keyword search" },
    "google":   { "checked": true, "note": "~50K ads on hp.com, AM not isolable" }
  },
  "ads": [],
  "themes":  { "Drones / UAV / defense": 14 },
  "formats": { "Video": 14 },
  "funnels": { "Top": 21 }
}
```

`themes`, `formats`, and `funnels` count **live instances**, not unique creatives.
That is why their totals exceed the length of `ads`. This has been misread before.

## Why data lives separately from the dashboard

Until Aug 2026 the dataset was embedded inside `index.html` as `const D={...}`. That
made the published page the only copy of the data, so diffing meant parsing last week's
HTML, and any render change risked the history. Data files are now the asset and
`index.html` is a view. History accumulates for free and trends become possible.
