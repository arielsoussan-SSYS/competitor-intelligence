# Competitive Ad Intelligence Dashboard

Live competitive ad tracking for Stratasys additive manufacturing. Monitors paid media activity across HP 3D Printing, Formlabs, and Bambu Lab.

**Live dashboard:** [https://arielsoussan-ssys.github.io/competitor-intelligence/](https://arielsoussan-ssys.github.io/competitor-intelligence/)

## What's Inside

Single-file HTML dashboard (no backend, no build step) with six tabs:

- **Dashboard** -- KPI cards, competitor filters, four Chart.js visualizations (platform mix, spend range, ad format, funnel stage), summary table
- **Ad Log (Full Data)** -- All 34 tracked ads across 16 columns. Searchable. Headlines link to source ad libraries. Screenshot placeholder column for future image capture.
- **HP Watch** -- Strategic intelligence brief for the sales team. Drone/UAV partnerships (Unusual Machines, Blueflite, Eye Above Project), 2026 product launches (MJF 1200, IF 600 HT), healthcare/O&P milestones, trade show presence, hiring signals. Includes a chronological activity timeline with sourced entries.
- **Competitor Summary** -- High-level comparison: ad counts, primary platforms, themes, audiences, spend ranges
- **Platform Strategy** -- 12-dimension side-by-side matrix (target market, platform strategy, formats, CTAs, funnel focus, content style, geography, spend)
- **Collection Notes** -- Methodology, spend estimation formulas, known limitations, instructions for adding screenshots

## Data Sources

All data collected from public ad transparency tools (no login required):

| Source | What We Capture |
|--------|----------------|
| [LinkedIn Ad Library](https://www.linkedin.com/ad-library/) | Company ads, impression ranges, formats, CTAs |
| [Meta Ad Library](https://www.facebook.com/ads/library/) | Active ads by keyword, creative themes |
| [Google Ads Transparency Center](https://adstransparency.google.com/) | Ad counts, formats, landing pages |

HP Watch tab is sourced from trade publications, press releases, and company newsrooms.

## Spend Estimation

Figures are directional estimates, not verified actuals:

- LinkedIn: impression range midpoint x CPM ($30-80 B2B)
- Google Search: estimated impressions x CPC ($1-5)
- Google Display: estimated impressions x CPM ($5-15)
- Meta: estimated reach x CPM ($10-30)

## Updating the Dashboard

A Cowork skill (competitive-ad-scrape) automates the full scrape. In any Claude Cowork session, say:

> "scrape competitor ads" or "update ad intelligence"

Claude will re-scrape all three ad libraries, refresh HP Watch intel, and regenerate the dashboard. A weekly scheduled task runs every Monday at 8:00 AM.

To deploy updates: replace index.html in this repo via GitHub web UI (Add file > Upload files > Commit).

## Tech Stack

- Single HTML file, zero dependencies beyond [Chart.js CDN](https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js)
- Hosted on GitHub Pages (free)
- Data embedded as JavaScript array (no database, no API calls)
- Works offline once loaded

## Key Findings (as of July 2026)

| Competitor | Platform Focus | Est. Monthly Spend | Strategy |
|-----------|---------------|-------------------|----------|
| HP 3D Printing | LinkedIn only (20 ads) | $15K-$50K | B2B verticals: healthcare, drones, O&P. Thought leadership + webinars. |
| Formlabs | LinkedIn (37) + Google (38) | $25K-$80K | Speed + price disruption. CRO personality-driven. Dental/medical dominant. |
| Bambu Lab | Google (~3K global) + Meta | $50K-$150K+ | B2C consumer machine. Multilingual. Lifestyle. Best Buy retail. |

## Repository Structure

```
index.html          # The complete dashboard (self-contained)
README.md           # This file
```

## License

Internal use -- Stratasys marketing team.

---

Built with [Claude Cowork](https://claude.ai) | Data: July 27, 2026 | Next refresh: Monday auto-scrape
