# Project context

Background that does not live in the data files. Ported into the repo on 2026-08-27 so it
survives a move to another machine, because Claude Code memory is per-machine and does not
travel with a clone.

## Why this exists

Management repeatedly told the marketing team that **HP is out-marketing Stratasys**.
Ariel disputed it: HP has essentially one technology and one printer line, Stratasys has
many. This repo was built to answer that question with evidence rather than opinion.

The answer, as of Aug 2026: **HP does not sustain higher spend, it concentrates.** One
MJF 1200 teaser took 500K-1M impressions in nineteen days around launch, then went quiet.
Three of their live ads carry expired dates, one from October 2025. That is a budget
pattern, and it is buyable. Use the specifics rather than conceding the point.

The second finding matters more: **we were watching the wrong competitor.** Formlabs
reaches the accessible-industrial segment a quarter before HP, is advertising into drone
manufacturing by name, and is already installed inside a Drone Dominance finalist.

## Who this is for

Stratasys sales, SDRs and marketing, in the Aerospace & Defense / Uncrewed Systems
vertical. It has also been presented upward to business-unit leadership.

Ariel owns ABM strategy and execution. He does **not** own the strategic calls on
direction, budget, messaging or timeline, and he wants those escalated explicitly rather
than absorbed. If a piece of work implies a decision above his level, say so.

### Stakeholders, as of 2026-08-19

| Person | Role | Owns |
|---|---|---|
| **Nina** | VP Marketing | Budget-level and vertical-direction calls |
| **Amy** | Aerospace & Defense vertical owner, reports to Nina | Messaging sign-off, webinars and events |
| **Justin** | Ariel's manager | Budget, sales commitment, definition of a win |
| **Jim Huefner** | Head of Unmanned Systems, former USMC Cobra pilot | Routes questions to Conrad |
| **Conrad Smith** | Global Director, Aerospace / Defense / UxS | Claim clearance, sales follow-up on engaged accounts |
| **Arthur** | Head of Digital | Web, conversion tracking, SEO. Consulted, does not own the campaign. |
| **Effy** (he/him) | Copy | Landing page copy; Arthur pushes changes live |
| **Yosi** | Campaign manager at Moveo, the agency | Runs the LinkedIn account. Executes well but does not volunteer insight, so ask direct questions. |

Ariel prefers to route through Jim rather than going to Conrad directly.

## What marketing already has running

Do not propose these as new ideas; they are live. Build on them.

- **UxS application content** plus AI and LLM search optimisation, so buyer research on
  drone additive lands on Stratasys
- **LinkedIn ABM** targeting the Drone Dominance companies by name
- This dashboard, feeding both

The standing ask to sales and SDRs: open with the **NDAA fleet-audit question** in defense
accounts, and report competitor machines seen on customer floors. That field reporting is
the cheapest route to validating who is running whose printers.

## Hard-won lessons

**Skills belong in git.** In Aug 2026 Ariel's computer was corrupted and he believed the
`competitive-ad-scrape` skill was lost. It was recoverable two ways: Cowork skills are
stored on the Claude account under Customize → Skills rather than local disk, and the
published dashboard retained enough structure to reconstruct the dataset. The skill now
lives in this repo so a single disk failure cannot destroy it. **If Ariel says he lost
something, check cloud storage and published artifacts before rebuilding from scratch.**

**A wrong tradecraft note is worse than no note.** An earlier version of `collection.md`
claimed LinkedIn URL parameters did not work. They do, and the form is the unreliable part.
That single wrong line cost about an hour. When a note turns out to be wrong, correct it
loudly in place rather than adding a caveat elsewhere.

**Verify identity, not just counts.** `3D Systems` returned 33 ads belonging to a Croatian
dental company and a branding agency. `Bambu` returned 237 ads all belonging to Bambuser.
Both looked like plausible data. Always confirm the distinct advertiser names in results.

**Check the EU subset before calling anything a priority.** A Formlabs drone ad looked like
a major campaign until the EU disclosure record showed under 1,000 impressions over two
weeks, already ended. It was a message test. The claim was still the finding; the reach was
not.

## Related work in the wider workspace

This repo sits inside Ariel's Stratasys workspace at
`Work/Stratasys/Aerospace & Defense/Competitor Intelligence/` and is gitignored there
because it has its own remote. Sibling folders hold the Drone Dominance campaign brief,
UAV and UxS campaign material, the message bank and industry research. Stratasys external
copy conventions apply to anything customer-facing produced from this repo: check the brand
guide, avoid em dashes, and mark unproven claims `[validation-needed]`.
