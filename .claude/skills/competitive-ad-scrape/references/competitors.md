# Tracked competitors

Tiering exists so the scan scales without every run becoming a full-depth study of
everyone. Tier determines depth, not importance.

## Tier 1 — full depth, every run

**HP Additive Manufacturing** (`hp`)
- LinkedIn advertiser: `HP Additive`
- Full ad log, full Watch section, full diff, company research
- Why: closest positioning overlap, actively contesting drones/UAV, and the competitor
  management most often cites as out-marketing us

Watch topics: MJF 1200 (Early Access mechanic, ships early 2027), IF 600 HT filament
printer, Metal Jet, drones/UAV/defense, orthotics and prosthetics, earnings and exec
changes, channel moves.

## Tier 2 — ad log and diff, abbreviated Watch

Collected every run. No standing Watch section unless something material moves.

| Competitor | Slug | LinkedIn advertiser | Why tracked |
|---|---|---|---|
| 3D Systems | `3dsystems` | 3D Systems | Direct industrial overlap, existing tracker |
| Formlabs | `formlabs` | Formlabs | Owns the workhorse/accessible segment, moving upmarket |
| Bambu Lab | `bambulab` | Bambu Lab | Prosumer disruption pressing up into professional; drone hobbyist crossover |

Formlabs and Bambu Lab were removed from the tracker on Aug 10 2026 when it narrowed to
HP-only, then reinstated at Tier 2. Tiering is what makes that sustainable: they get an
ad log and a diff, not the full HP treatment.

## Tier 3 - account penetration watch, no ad log

No ad scraping. This tier answers a sales question, not a marketing one:
**which companies we want to sell into does a competitor already have a foothold in?**

Maintained in `data/account-watch.json`. Each account carries the competitor present,
the evidence type and link, a confidence level, and a **displacement posture**:

| Posture | Meaning | Sales implication |
|---|---|---|
| `Open` | No incumbent found | Straight new-business pursuit |
| `Contested` | Competitor present, not locked in | Highest-value target. Move now. |
| `Locked` | Equipment installed and validated | Long play, or partner around it |

**Drone Dominance Gauntlet, Phase 2** - 19 teams, every one a live Stratasys prospect.
Intelligence indicates HP is supporting 14 of the 19 `[validation-needed]`.

The team names do not matter in themselves. What matters is that this is a
pre-qualified list of companies building drones at production intent, and a competitor
may have reached them first. If the 14-of-19 figure holds, HP is buying ecosystem
position ahead of its advertising, which is exactly the kind of move an ad scan alone
would never surface. That is the argument for this tier existing.

Each run should attempt to move at least one account from `[Unverified]` toward
`Confirmed` or `Refuted`, and surface every `Contested` account into the sales brief.

**Uncrewed systems (UxS) more broadly** - defense and commercial UAV primes and
suppliers adopting AM. Watch for supplier announcements naming a competitor, and add
any new company to the account watch.

## Adding a competitor

Add a row here, then run the scan. It is picked up automatically. Do not create a
bespoke HTML page per competitor: that is what forced `3dsystems.html` to be built by
hand and it does not scale past two.
