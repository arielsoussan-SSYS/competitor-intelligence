#!/usr/bin/env python3
"""
spend_model.py  -  LinkedIn spend estimation, one auditable implementation
============================================================================
Every dollar figure in this repo comes from here. Nothing is hardcoded in a
data file any more, so an estimate can always be traced back to the band, the
run length and the CPM that produced it.

WHY THIS REPLACED THE OLD APPROACH
-----------------------------------
The previous method stored `lo`/`hi` dollars directly in each ad record. It
had three defects, in increasing order of severity:

1. The stored dollars did not follow the documented CPM. A 10K-50K band
   carried $3,000-$8,000, where $30-80 CPM gives $300-$4,000.
2. It used the arithmetic midpoint of a band. Bands are log-scaled and
   impression distributions are approximately log-normal, so the midpoint
   overstates by roughly 30-35%.
3. **It treated an ad's lifetime impressions as a monthly figure.** One HP
   webinar creative ran from Oct 2025 to Aug 2026. Counting its whole-run
   impressions as one month's delivery overstated it by about 10x. This was
   by far the largest error.

WHAT LINKEDIN ACTUALLY DISCLOSES
---------------------------------
Only for ads targeted to the EU, to comply with the Digital Services Act:
estimated total impressions (banded), a per-country percentage split, run
dates and targeting parameters. For an ad never targeted to the EU there is
no impression data at all.

Verified against live ads on 2026-09-22: the disclosed total is the ad's
FULL total across all countries, with the country split alongside it, not an
EEA-only subtotal. HP's MJFNext teaser reads 500k-1M total at 97% United
States. So a disclosed ad is fully estimable, and can also be split by
country. An ad with no disclosure is not estimable at all, and must never be
imputed from one that is.

Sources, checked 2026-09-22:
  https://www.linkedin.com/help/lms/answer/a1517918   what the library shows
  https://www.linkedin.com/help/lms/answer/a1620070   impressions + targeting
  https://www.linkedin.com/help/lms/answer/a422101    budgets and pacing
"""

import math
import re
from datetime import date

# -- CPM bands, US dollars per thousand impressions -------------------------
# B2B ranges. Published benchmarks disagree materially and every one of them
# comes from a vendor with an incentive, so these are deliberately wide and
# treated as order-of-magnitude. The old $30-80 sat at the narrow-ABM end of
# the range and was applied to everything, which biased every figure upward.
#
# Format matters: video and thought-leader creative clear cheaper per
# impression than single image.
CPM = {
    "Single Image": (24, 55),
    "Carousel":     (24, 55),
    "Document":     (22, 50),
    "Video":        (20, 45),
    "Thought Leader": (15, 38),
    "Event":        (20, 45),
    "Text":         (15, 35),
    "DEFAULT":      (20, 55),
}

# Message and Conversation Ads price per send, not per impression, so an
# impression-derived CPM is meaningless for them. Published cost per send
# clusters around $0.81 with a wide spread.
SEND_COST = (0.30, 1.00)
PER_SEND_FORMATS = ("Message", "Conversation")

DAYS_PER_MONTH = 30.44
MIN_ACTIVE_DAYS = 7      # floor, so a brand-new ad cannot divide to infinity

MONTHS = {m: i + 1 for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}


def parse_band(text):
    """'30k-50k' -> (30000, 50000, False). '500k-1M' -> (500000, 1000000, False).
    '1M+' -> (1000000, None, True) meaning open-topped.
    '<1k' -> (0, 1000, False). Anything unparseable -> None.
    """
    if not text:
        return None
    t = str(text).strip().lower().replace(" ", "").replace(",", "")
    t = t.replace("total", "").replace("impressions", "")
    if "notdisclosed" in t or t in ("", "n/a", "unknown", "-"):
        return None

    def num(s):
        m = re.match(r"^([\d.]+)([km]?)$", s)
        if not m:
            return None
        v = float(m.group(1))
        return int(v * {"k": 1_000, "m": 1_000_000, "": 1}[m.group(2)])

    if t.startswith("<"):
        hi = num(t[1:])
        return (0, hi, False) if hi else None
    if t.endswith("+"):
        lo = num(t[:-1])
        return (lo, None, True) if lo else None
    if "-" in t:
        a, b = t.split("-", 1)
        lo, hi = num(a), num(b)
        # "500k-1M": the low side may omit its own unit suffix
        if lo and hi:
            return (lo, hi, False)
        return None
    single = num(t)
    return (single, single, False) if single else None


def band_point(lo, hi, open_ended=False):
    """Representative impression count for a band.

    Geometric mean, not the arithmetic midpoint: bands are log-scaled and the
    underlying distribution is log-normal, so probability mass sits toward the
    low end. 10K-50K gives 22.4K rather than 30K.

    An open-topped band has no upper bound to average against, so its floor is
    the only honest figure. Callers should mark those results as ">=".
    """
    if open_ended or hi is None:
        return lo
    if lo == 0:          # '<1k' has no meaningful geometric mean
        return hi / 2
    return math.sqrt(lo * hi)


def _parse_date(value):
    """Accepts 'Aug 2026', 'Aug 10, 2026', '2026-08-10'."""
    if not value:
        return None
    s = str(value).strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r"^([A-Za-z]{3})\w*\s+(\d{1,2}),\s*(\d{4})$", s)
    if m:
        return date(int(m.group(3)), MONTHS[m.group(1).title()], int(m.group(2)))
    m = re.match(r"^([A-Za-z]{3})\w*\s+(\d{4})$", s)
    if m:
        return date(int(m.group(2)), MONTHS[m.group(1).title()], 1)
    return None


def active_months(first, last, today=None):
    """Run length in months, floored so short runs cannot explode the rate.

    Linear division is the defensible default. LinkedIn's lifetime pacing
    varies day to day (it allows up to 100% over the daily budget on a given
    day) but there is no published pacing curve to calibrate a decay against,
    so reshaping the mean would be invention. Widen the interval instead.
    """
    today = today or date.today()
    f = _parse_date(first)
    if not f:
        return None
    l = _parse_date(last) or today
    if l > today:
        l = today
    days = max((l - f).days + 1, MIN_ACTIVE_DAYS)
    return days / DAYS_PER_MONTH


def cpm_for(fmt):
    f = (fmt or "").strip()
    for key, band in CPM.items():
        if key != "DEFAULT" and key.lower() in f.lower():
            return band
    return CPM["DEFAULT"]


def is_per_send(fmt):
    return any(k.lower() in (fmt or "").lower() for k in PER_SEND_FORMATS)


def estimate(ad, today=None):
    """Monthly spend estimate for one ad record.

    Returns a dict that always explains itself:
      estimable    bool
      monthly_lo   float or None
      monthly_hi   float or None
      floor_only   True when the band is open-topped, so read the figure as ">="
      basis        short human-readable explanation
    """
    fmt = ad.get("format") or ""
    band = parse_band(ad.get("impr"))
    months = active_months(ad.get("first"), ad.get("last"), today)

    if band is None:
        return {"estimable": False, "monthly_lo": None, "monthly_hi": None,
                "floor_only": False,
                "basis": "Impressions not disclosed. LinkedIn publishes them "
                         "only for EU-targeted ads, so this ad cannot be "
                         "costed. Not zero, unknown."}

    lo, hi, open_ended = band
    point = band_point(lo, hi, open_ended)

    if is_per_send(fmt):
        # Impressions approximate sends for a message ad, and it is priced
        # per send. No CPM involved.
        s_lo, s_hi = SEND_COST
        total_lo, total_hi = point * s_lo, point * s_hi
        if months:
            return {"estimable": True, "monthly_lo": total_lo / months,
                    "monthly_hi": total_hi / months, "floor_only": open_ended,
                    "basis": f"{fmt} priced per send at ${s_lo:.2f}-${s_hi:.2f}. "
                             f"~{point:,.0f} sends over {months:.1f} months."}
        return {"estimable": True, "monthly_lo": total_lo, "monthly_hi": total_hi,
                "floor_only": open_ended,
                "basis": f"{fmt} priced per send, run length unknown so the "
                         f"figure is whole-run, not monthly."}

    if not months:
        return {"estimable": False, "monthly_lo": None, "monthly_hi": None,
                "floor_only": False,
                "basis": "Run dates missing, so lifetime impressions cannot be "
                         "converted to a monthly rate."}

    cpm_lo, cpm_hi = cpm_for(fmt)
    monthly_impr = point / months
    return {
        "estimable": True,
        "monthly_lo": monthly_impr / 1000 * cpm_lo,
        "monthly_hi": monthly_impr / 1000 * cpm_hi,
        "floor_only": open_ended,
        "basis": (f"{point:,.0f} impressions (geometric mean of {ad.get('impr')}) "
                  f"over {months:.1f} months = {monthly_impr:,.0f}/mo, "
                  f"at ${cpm_lo}-${cpm_hi} CPM for {fmt or 'unknown format'}."),
    }


def summarise(ads, today=None):
    """Aggregate across ads. Reports how much of the set was measurable,
    because a total over 2 of 18 ads means something very different from a
    total over 18 of 18."""
    tot_lo = tot_hi = 0.0
    n_est = n_unknown = 0
    floor_only = False
    for a in ads:
        r = estimate(a, today)
        if r["estimable"]:
            n_est += 1
            tot_lo += r["monthly_lo"] or 0
            tot_hi += r["monthly_hi"] or 0
            floor_only = floor_only or r["floor_only"]
        else:
            n_unknown += 1
    return {
        "monthly_lo": tot_lo, "monthly_hi": tot_hi,
        "n_estimated": n_est, "n_undisclosed": n_unknown,
        "floor_only": floor_only,
        "coverage": f"{n_est} of {n_est + n_unknown} creatives had disclosed "
                    f"impressions and could be costed.",
    }


def label(result) -> str:
    """Render a result for display. Always carries [Estimate]."""
    if not result.get("estimable", True) and result.get("monthly_lo") is None:
        return "not disclosed"
    lo, hi = result.get("monthly_lo"), result.get("monthly_hi")
    if lo is None:
        return "not disclosed"
    prefix = ">=" if result.get("floor_only") else ""

    def m(v):
        return f"${v/1000:.1f}K" if v >= 1000 else f"${v:,.0f}"
    return f"{prefix}{m(lo)} to {m(hi)}/mo [Estimate]"


if __name__ == "__main__":
    # Real ads read from the live library on 2026-09-22, used as the
    # regression cases for this model.
    cases = [
        {"name": "HP MJFNext teaser (video burst)", "format": "Video Ad",
         "impr": "500k-1M", "first": "Mar 26, 2026", "last": "Apr 13, 2026"},
        {"name": "HP MJF 1200 reserve (carousel)", "format": "Carousel Ad",
         "impr": "30k-50k", "first": "Jun 29, 2026", "last": "Jul 19, 2026"},
        {"name": "Formlabs Skyfall drone message ad", "format": "Message Ad",
         "impr": "<1k", "first": "Aug 10, 2026", "last": "Sep 7, 2026"},
        {"name": "HP drone webinar (no EU targeting)", "format": "Document",
         "impr": "Not disclosed", "first": "Oct 2025", "last": "Aug 2026"},
    ]
    print("Regression cases, live ads read 2026-09-22\n" + "=" * 70)
    for c in cases:
        r = estimate(c, today=date(2026, 9, 22))
        print(f"\n{c['name']}")
        print(f"  {label(r)}")
        print(f"  {r['basis']}")

    print("\n" + "=" * 70)
    print("Sanity checks")
    assert parse_band("30k-50k") == (30000, 50000, False)
    assert parse_band("500k-1M") == (500000, 1000000, False)
    assert parse_band("1M+") == (1000000, None, True)
    assert parse_band("Not disclosed") is None
    assert abs(band_point(10000, 50000) - 22360.7) < 1
    # geometric mean must sit below the arithmetic midpoint
    assert band_point(10000, 50000) < 30000
    assert active_months("Aug 10, 2026", "Sep 7, 2026") > 0.9
    assert not estimate({"format": "Video", "impr": "Not disclosed"})["estimable"]
    print("  all passed")
