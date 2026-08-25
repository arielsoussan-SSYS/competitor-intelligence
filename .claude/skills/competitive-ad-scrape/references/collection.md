# Collection tradecraft

Source-specific detail that is expensive to rediscover. Applies to browser-driven runs;
where a scraping API is used instead, the field mappings still hold.

## LinkedIn Ad Library

Primary source, and the only one that reliably yields creative-level data.

- Advertiser: **"HP Additive Manufacturing (AM) Solutions - 3D Printing"**
- **URL query parameters return "No results found."** Click the "Company or advertiser"
  field, type the name, then click Search. If typing does not register, click the field
  again and retype: the first click sometimes only focuses the page.
- Read the **"N ads match your search criteria"** count. That is the **instance** count
  and the source of truth for reconciliation.
- Results lazy-load. Capture page text, scroll ~25 ticks, wait, scroll again, capture
  again to get the remainder.
- No login required.

## Meta Ad Library

Keyword search, not advertiser search: `Multi Jet Fusion`, `HP 3D printing`,
`HP Metal Jet`. Filter active, ad_type=all, country=US.

Historically returns a handful of unrelated third-party ads and **zero HP-owned ads**.
Record as a finding. Never report it as proof HP runs no Meta ads.

## Google Ads Transparency Center

`adstransparency.google.com/?region=anywhere&domain=hp.com` returns ~50,000 ads across
all HP advertiser accounts, dominated by consumer PC and printer creative. **HP AM
cannot be isolated from the parent corporate entity.** Record the limitation.
**Never present the 50K figure as AM activity.**

### The higher-value Google signal: display flights on trade sites

Check trade press for HP display banners: 3dprintingindustry.com, tctmagazine.com,
voxelmatters.com.

Inspect banner destination URLs for `jumpid=...cm######...` campaign codes.
**A new code means a newly funded flight** — the earliest available signal that HP has
put budget behind something.

Known codes:

| Code | Campaign |
|---|---|
| `cm019626` | April RAPID launch |
| `cm019629` | August MJF 1200 display |
| `cm016808` | Drones learning center |

Any code not on this list is a finding. Add it here when confirmed.

## Counting rule

Count instances **by hand** from the raw list and make them sum to the reported
"N ads match" total. Do not estimate.

Compute theme shares off instances and state the denominator inline:
"38% of ad volume (14 of 37)".

If a prior run recorded only unique-creative counts, say "not recorded" for the prior
instance figure rather than inventing a comparison.
