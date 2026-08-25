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
- Results lazy-load, and **scrolling alone stops early**. On the Aug 25 run scrolling
  plateaued at 24 of 38 results. The remainder sits behind a hidden loader:

  ```js
  const b=document.querySelector('.infinite-scroller__show-more-button');
  b.style.cssText='display:block;width:200px;height:40px;position:fixed;top:300px;left:400px;z-index:99999';
  ```
  Then click it with a **real mouse event** at those coordinates. A programmatic
  `.click()` does not register. Re-check the unique-ID count until it equals the
  reported total.
- Extract per-card by walking up from each `a[href*="/ad-library/detail/"]` to the
  first ancestor with >80 chars of `innerText`. Dedupe on the numeric detail ID.
- Detail pages can be **batch-fetched same-origin**: `fetch('/ad-library/detail/'+id)`
  then `DOMParser`. Far faster than navigating. Gives format ("Single Image Ad",
  "Video Ad", "Document Ad", "Conversation") and the full untruncated body.
- **Rate limiting is real.** After ~10 rapid detail fetches the search XHR starts
  returning "Failed to load" and stays broken for minutes. Space out searches, or
  batch detail fetches after all searches are done.
- Advertiser and keyword fields **AND together**. Clear the keyword field before an
  advertiser-only count, or the total is silently narrowed. Advertiser-only "Formlabs"
  returned 38; with keyword "Formlabs" still set it returned 36.
- Search state is a POST, not a URL parameter, so a search cannot be linked or reloaded.
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

### Isolability varies by competitor

`hp.com` cannot be isolated because HP AM shares the parent corporate entity with
consumer PCs and printers. **This is not true of every competitor.** `formlabs.com`
resolves to a single verified advertiser account, `Formlabs Inc.`
(`AR04252334007510892545`), so the numbers are clean. Check for a single advertiser
before assuming the HP limitation applies.

Useful mechanics:

- Append `&hl=en`. The UI otherwise renders in the browser's locale.
- Format counts come from the URL: `?region=anywhere&format=TEXT|IMAGE|VIDEO&hl=en`.
  Read the "N ads" figure off each. The headline "~200 ads" on the domain page is
  rounded and domain-wide. **Report the summed format counts, not the rounded figure.**
- Creative content renders in a **cross-origin iframe**, so it cannot be read by JS.
  Screenshot the creative detail page instead.
- The creative detail page gives "Last shown", which is how you prove an account is
  live today rather than merely listed.

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
