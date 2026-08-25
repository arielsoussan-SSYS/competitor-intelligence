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

Maintained in `data/gauntlet.json`. Each account carries the competitor present,
the evidence type and link, a confidence level, and a **displacement posture**:

| Posture | Meaning | Sales implication |
|---|---|---|
| `Open` | No incumbent found | Straight new-business pursuit |
| `Contested` | Competitor present, not locked in | Highest-value target. Move now. |
| `Locked` | Equipment installed and validated | Long play, or partner around it |

**Drone Dominance Gauntlet II** - 19 companies, Fort Carson CO, August 2026, from a
$1.1B program. Every one is a live Stratasys prospect. Names, program structure and
selection funnel are confirmed in `data/gauntlet.json`.

Intelligence indicates HP supports 14 of the 19 `[validation-needed]`. If it holds, HP is
buying ecosystem position ahead of its advertising, which an ad scan alone would never
surface. That is the argument for this tier existing.

**The standing counter-signal:** Neros CEO Soren Monroe-Anderson argues publicly that 3D
printing does not solve the drone supply-chain problem, and that mass production means
designing the product around manufacturing. Neros was a Gauntlet 1 award winner running
250+ drones/day. This is the strongest objection in the market to the entire drone
additive pitch, ours as much as HP's. Track whether it spreads to other teams.

Each run should attempt to move at least one account from `[Unverified]` toward
`Confirmed` or `Refuted`, and surface every `Contested` account into the sales brief.

**Uncrewed systems (UxS) more broadly** - defense and commercial UAV primes and
suppliers adopting AM. Watch for supplier announcements naming a competitor, and add
any new company to the account watch.

## Adding a competitor

Add a row here, then run the scan. It is picked up automatically. Do not create a
bespoke HTML page per competitor: that is what forced `3dsystems.html` to be built by
hand and it does not scale past two.
