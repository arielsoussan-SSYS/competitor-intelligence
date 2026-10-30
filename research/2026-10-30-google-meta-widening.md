# Widening the scan: LinkedIn, Google and Meta (2026-10-30)

Why: Ari asked whether LinkedIn is still the right place to watch competitors. This note holds the first look at Google and Meta next to a fresh LinkedIn pass. It is not a dashboard run. It is local only: not committed, not pushed (the repo is public).

Collected through Ari's Chrome (claude-in-chrome), US view unless stated. Counts are live ads or instances as each library reports them. Spend is not estimated here.

## What each competitor runs, by platform

| Competitor | LinkedIn (live instances) | Google (US, domain page) | Meta (US, active) |
|---|---|---|---|
| HP Additive | 24 (was 34 on Oct 4 and 12). 24 of 24 extracted | hp.com ~50K worldwide, not isolable from consumer HP | None found. "HP Additive Manufacturing" returns nothing; "HP Multi Jet Fusion" returns 1 unrelated bike brand ad |
| Formlabs | 13, 9 unique creatives (was 27 on Oct 12, 28 on Oct 4, 33 on Sep 15 and Sep 22, 38 before Sep 15). Control passed | 59 US (7 video); ~200 worldwide. One verified advertiser, Formlabs Inc. | ~13 keyword results. 6 from the Formlabs page, 2 from MatterHackers (reseller), the rest unrelated |
| 3D Systems | 1 (jobs ad only, same as before) | 9 US, 36 worldwide. Verified advertiser 3D Systems Corporation | Not isolable. Keyword "3D Systems" returns 50,000 results of unrelated advertisers. Needs a page-level check |
| Bambu Lab | 0 ("No results found") on `Bambu Lab` and `BambuLab`. The other three names (`Bambu Lab US`, `Bambu Japan`, `Tuozhu`) were not re-checked this run; they were zero on Oct 12 | ~3K worldwide, ~200 US, 29 US video. Advertiser is the legal entity 深圳拓竹科技有限公司 (Shenzhen Tuozhu Technology) | ~350 results. Page "Bambu Lab 3D" plus creator and retail partners (Best Buy, Target, AliExpress, named creators such as Chris Paul) |

LinkedIn control: `accountOwner=Formlabs` returned a count (13) before any zero was recorded.

## What this says

- Bambu Lab is not absent from advertising. It is absent from LinkedIn only. It runs about 3K Google ads worldwide and about 350 Meta ads in the US, with retail and creator partners. `[Inference]` The channel mix points at consumer and prosumer buyers, which fits the defense-ban angle: they are not pursuing B2B buyers through paid LinkedIn.
- Formlabs and HP LinkedIn volume has fallen since September (Formlabs 38 to 13, HP 36 to 24). `[Inference]` Could be rotation or a real pullback; two or three more points are needed before calling it a trend.
- Formlabs spreads across all three: LinkedIn 13, Google 59 US, Meta about 6 own ads plus reseller ads (MatterHackers).
- HP shows no Meta ads under the AM names searched. HP's Google total cannot be split from consumer HP.
- 3D Systems is the quietest: 1 LinkedIn jobs ad, 9 US Google ads. Meta unresolved.

## Method notes (for the skill)

- Google: `https://adstransparency.google.com/?region=US&domain=<domain>&hl=en`, add `&format=VIDEO|TEXT|IMAGE`. Counts over about 200 show as "~200", so they cap out. A domain page can include unrelated advertiser accounts (3dsystems.com showed a Japanese housing company).
- Meta: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q=<name>&search_type=keyword_unordered&media_type=all`. Works signed in. Read the "~N results" line and the advertiser names above each "Sponsored" tag. Keyword results mix in other advertisers, so always count by advertiser page name.
- Meta notice: a US restriction period (Oct 27 to Nov 4) blocks new ads on social issues, elections or politics. Not relevant to these advertisers.
- Per the repo rules, keyword results are discovery only and never go in the ad log.

## Not done yet

- Page-level Meta check for HP, 3D Systems (find the Page ID, then search by page).
- Bambu LinkedIn variants `Bambu Lab US`, `Bambu Japan`, `Tuozhu`, and the EU-country pass for Formlabs and HP. The batch that held them was interrupted.
- Creative-level capture (headlines, formats, run dates) for Google and Meta.
- No run file written to `data/`; the dashboard is unchanged.
