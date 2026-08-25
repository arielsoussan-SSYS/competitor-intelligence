#!/usr/bin/env python3
"""Build index.html from the latest run file per competitor in data/.

The data files are the asset. This script is only a view of them.
Usage: python3 tools/build_dashboard.py
"""
import json, sys, glob, os, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDER = ["hp", "bambulab", "formlabs", "3dsystems"]

def load():
    latest = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "20*-*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception as ex:
            sys.exit("Bad JSON in %s: %s" % (p, ex))
        slug = d.get("slug")
        if not slug:
            continue
        latest[slug] = d          # sorted by filename, so last wins
    if not latest:
        sys.exit("No run files with a slug in data/")
    order = [s for s in ORDER if s in latest] + [s for s in latest if s not in ORDER]
    return latest, order

C, order = load()
built = datetime.date.today().isoformat()

# reconciliation: instance buckets must agree, per competitor
for s, d in C.items():
    if d.get("status") == "pending":
        continue
    tot = {k: sum(d.get(k, {}).values()) for k in ("themes", "formats", "funnels")}
    # an empty bucket is a declared gap, not a disagreement; only compare populated ones
    tot = {k: v for k, v in tot.items() if v}
    if len(set(tot.values())) > 1:
        print("WARN %s: instance buckets disagree %s" % (s, tot), file=sys.stderr)

GPATH = os.path.join(ROOT, "data", "gauntlet.json")
G = json.load(open(GPATH, encoding="utf-8")) if os.path.exists(GPATH) else None

PAYLOAD = {"competitors": C, "order": order, "built": built, "gauntlet": G}

TPL = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="color-scheme" content="light">
<title>Competitive Ad Intelligence &middot; Stratasys</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --ink:#101725; --ink2:#414b60; --ink3:#6f7889;
  --glass:rgba(255,255,255,.88); --glass2:rgba(255,255,255,.72);
  --stroke:rgba(255,255,255,.95); --edge:rgba(16,23,37,.07); --hair:rgba(16,23,37,.09);
  --shadow:0 1px 2px rgba(16,23,37,.05),0 10px 28px rgba(16,23,37,.08);
  --navy:#1f3864; --red:#c8102e; --amber:#a86400; --green:#1c6b45; --slate:#4a5464;
  --r:22px;
}
html{-webkit-text-size-adjust:100%}
body{
  font:15px/1.5 -apple-system,BlinkMacSystemFont,"SF Pro Text","SF Pro Display",
       "Segoe UI",Inter,system-ui,sans-serif;
  color:var(--ink); background:#f4f7fc; letter-spacing:-.011em;
  -webkit-font-smoothing:antialiased; min-height:100vh; padding-bottom:60px;
}
body::before{
  content:""; position:fixed; inset:0; z-index:-1; background:
    radial-gradient(56vw 46vw at 4% -8%, rgba(31,56,100,.13), transparent 62%),
    radial-gradient(50vw 44vw at 98% 2%, rgba(58,132,196,.15), transparent 60%),
    radial-gradient(54vw 46vw at 52% 106%, rgba(96,160,190,.13), transparent 62%),
    linear-gradient(172deg,#f8fafd 0%,#eef3fa 55%,#e9eff8 100%);
}
.wrap{max-width:1200px;margin:0 auto;padding:0 18px}
.glass{background:var(--glass);
  -webkit-backdrop-filter:blur(22px) saturate(155%);backdrop-filter:blur(22px) saturate(155%);
  border:1px solid var(--stroke);outline:1px solid var(--edge);outline-offset:-1px;
  border-radius:var(--r);box-shadow:var(--shadow)}
header{padding:32px 0 14px}
.eyebrow{font-size:11px;font-weight:660;letter-spacing:.1em;text-transform:uppercase;color:var(--ink3)}
h1{font-size:clamp(25px,4.2vw,36px);font-weight:700;letter-spacing:-.028em;margin:6px 0 8px}
.sub{color:var(--ink2);font-size:14px;max-width:74ch}
/* competitor switcher */
.who{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0 6px}
.co{flex:1 1 190px;text-align:left;cursor:pointer;font:inherit;padding:13px 16px;
  border-radius:18px;border:1px solid var(--stroke);outline:1px solid var(--edge);outline-offset:-1px;
  background:var(--glass2);-webkit-backdrop-filter:blur(18px) saturate(150%);
  backdrop-filter:blur(18px) saturate(150%);box-shadow:var(--shadow);
  transition:transform .18s cubic-bezier(.22,.9,.3,1),box-shadow .18s,background .18s}
.co:hover{transform:translateY(-1px)}
.co .n{font-size:15px;font-weight:660;letter-spacing:-.018em;color:var(--ink);display:block}
.co .m{font-size:12px;color:var(--ink3);margin-top:3px;display:block}
.co[aria-pressed=true]{background:#fff;box-shadow:0 2px 4px rgba(16,23,37,.07),0 12px 30px rgba(31,56,100,.16);
  border-color:#fff;outline-color:rgba(31,56,100,.28)}
.co[aria-pressed=true] .n{color:var(--navy)}
.co.pend .n{color:var(--ink3)}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:7px;vertical-align:1px}
.dot.live{background:var(--green)}.dot.pend{background:#c4ccd8}
.pills{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.pill{font-size:12px;font-weight:600;padding:6px 12px;border-radius:999px;background:var(--glass2);
  border:1px solid var(--stroke);outline:1px solid var(--edge);outline-offset:-1px;color:var(--ink2);
  -webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.pill b{color:var(--ink)}
.hero{padding:24px 26px 22px;margin:16px 0;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;inset:0 0 auto 0;height:3px;
  background:linear-gradient(90deg,var(--red),var(--navy))}
.hero .lab{font-size:11px;font-weight:660;letter-spacing:.1em;text-transform:uppercase;color:var(--red)}
.hero h2{font-size:clamp(18px,2.6vw,24px);font-weight:660;letter-spacing:-.022em;margin:10px 0 14px;line-height:1.34}
.sowhat{padding:14px 16px;border-radius:15px;background:rgba(255,252,245,.9);
  border:1px solid var(--stroke);outline:1px solid var(--edge);outline-offset:-1px;
  border-left:3px solid var(--amber);font-size:14px;color:var(--ink2)}
.sowhat b{color:var(--ink)}
nav.tabs{position:sticky;top:10px;z-index:30;margin:16px 0;padding:5px;display:flex;gap:3px;
  overflow-x:auto;scrollbar-width:none}
nav.tabs::-webkit-scrollbar{display:none}
.tab{flex:0 0 auto;border:0;cursor:pointer;font:inherit;font-size:13.5px;font-weight:600;
  color:var(--ink2);background:transparent;padding:9px 15px;border-radius:15px;transition:background .18s,color .18s}
.tab:hover{color:var(--ink)}
.tab[aria-selected=true]{background:#fff;color:var(--navy);box-shadow:0 1px 2px rgba(16,23,37,.06),0 4px 14px rgba(16,23,37,.09)}
.panel{display:none;animation:in .3s cubic-bezier(.22,.9,.3,1)}
.panel.on{display:block}
@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.panel{animation:none}.co{transition:none}}
.card{padding:20px 22px;margin-bottom:16px}
.card h3{font-size:16px;font-weight:660;letter-spacing:-.018em;margin-bottom:4px}
.card .cap{font-size:13px;color:var(--ink3);margin-bottom:16px}
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(205px,1fr))}
.kpi{padding:16px 18px}
.kpi .k{font-size:11px;font-weight:660;letter-spacing:.06em;text-transform:uppercase;color:var(--ink3)}
.kpi .v{font-size:29px;font-weight:700;letter-spacing:-.03em;margin:6px 0 4px;font-variant-numeric:tabular-nums}
.kpi .d{font-size:12.5px;color:var(--ink2);line-height:1.42}
.dir{display:inline-block;font-weight:700;margin-right:5px}
.dir.down{color:var(--red)}.dir.up{color:var(--green)}.dir.flat{color:var(--ink3)}
.tt{padding:18px 20px}
.tt .tag{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.07em;
  text-transform:uppercase;color:var(--red);margin-bottom:9px}
.tt .claim{font-size:14.5px;font-weight:600;line-height:1.45;margin-bottom:11px;color:var(--ink)}
.tt .arrow{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--green);display:block;margin-bottom:5px}
.tt .ctr{font-size:14px;color:var(--ink2);line-height:1.55}
.chg{margin-bottom:14px;padding:16px 18px}
.chg .cat{font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--navy);
  margin-bottom:12px;display:flex;align-items:center;gap:8px}
.chg .cat span{font-size:10.5px;background:var(--glass2);border:1px solid var(--edge);
  border-radius:999px;padding:2px 8px;color:var(--ink3)}
.chg li{list-style:none;padding:12px 0;border-top:1px solid var(--hair)}
.chg li:first-of-type{border-top:0;padding-top:0}
.chg .t{font-weight:600;font-size:14px;margin-bottom:5px;line-height:1.45}
.chg .d{font-size:13.5px;color:var(--ink2);line-height:1.55}
a.src{font-size:12px;color:var(--navy);text-decoration:none;font-weight:600;
  border-bottom:1px solid transparent;transition:border-color .15s}
a.src:hover{border-bottom-color:currentColor}
ul.plain li{list-style:none;padding:11px 0;border-top:1px solid var(--hair);font-size:14px;
  color:var(--ink2);line-height:1.55}
ul.plain li:first-child{border-top:0;padding-top:0}
ul.plain b{color:var(--ink)}
.tools{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
input.search{flex:1;min-width:220px;font:inherit;font-size:14px;padding:11px 15px;border-radius:14px;
  border:1px solid var(--edge);background:rgba(255,255,255,.9);color:var(--ink);outline:none}
input.search:focus{border-color:var(--navy);box-shadow:0 0 0 3.5px rgba(31,56,100,.15)}
input.search::placeholder{color:var(--ink3)}
.scroll{overflow-x:auto;border-radius:15px;border:1px solid var(--edge);background:rgba(255,255,255,.62)}
table{border-collapse:collapse;width:100%;font-size:13px;min-width:760px}
th{background:rgba(244,247,252,.95);text-align:left;padding:11px 13px;font-size:11px;font-weight:660;
  letter-spacing:.06em;text-transform:uppercase;color:var(--ink3);position:sticky;top:0;
  -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}
td{padding:12px 13px;border-top:1px solid var(--hair);vertical-align:top;color:var(--ink2)}
td.hl{color:var(--ink);font-weight:550;max-width:340px}
tr.new td{background:rgba(28,107,69,.08)}
.badge{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.05em;padding:3px 8px;
  border-radius:999px;white-space:nowrap}
.b-new{background:rgba(28,107,69,.14);color:var(--green)}
.b-carry{background:rgba(16,23,37,.06);color:var(--ink3)}
.f{font-size:11px;font-weight:660;color:var(--ink3)}
canvas{max-height:270px}
.sect{display:flex;gap:4px;padding:5px;margin:18px 0 4px;width:fit-content;max-width:100%;overflow-x:auto;scrollbar-width:none}
.sect::-webkit-scrollbar{display:none}
.sb{flex:0 0 auto;border:0;cursor:pointer;font:inherit;font-size:14px;font-weight:640;color:var(--ink2);
  background:transparent;padding:10px 20px;border-radius:16px;transition:background .18s,color .18s}
.sb:hover{color:var(--ink)}
.sb[aria-pressed=true]{background:#fff;color:var(--navy);box-shadow:0 1px 2px rgba(16,23,37,.06),0 5px 16px rgba(16,23,37,.10)}
.view{display:none}.view.on{display:block}
.sig{padding:18px 20px;border-left:3px solid var(--red)}
.sig .l{font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--red);margin-bottom:8px}
.sig .h{font-size:15px;font-weight:640;line-height:1.45;margin-bottom:7px}
.sig .b{font-size:13.5px;color:var(--ink2);line-height:1.55}
.nav2{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));margin-top:4px}
.ncard{padding:20px 22px;cursor:pointer;text-align:left;font:inherit;border:1px solid var(--stroke);
  outline:1px solid var(--edge);outline-offset:-1px;background:var(--glass);border-radius:var(--r);
  box-shadow:var(--shadow);-webkit-backdrop-filter:blur(22px) saturate(155%);
  backdrop-filter:blur(22px) saturate(155%);transition:transform .18s cubic-bezier(.22,.9,.3,1),box-shadow .18s}
.ncard:hover{transform:translateY(-2px);box-shadow:0 2px 4px rgba(16,23,37,.07),0 14px 34px rgba(31,56,100,.15)}
.ncard .t{font-size:16px;font-weight:660;letter-spacing:-.018em;margin-bottom:6px;color:var(--ink)}
.ncard .d{font-size:13.5px;color:var(--ink2);line-height:1.5}
.ncard .go{font-size:12.5px;font-weight:660;color:var(--navy);margin-top:11px;display:block}
.gmeta{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));margin-bottom:16px}
.gm{padding:14px 16px}
.gm .k{font-size:10.5px;font-weight:660;letter-spacing:.06em;text-transform:uppercase;color:var(--ink3)}
.gm .v{font-size:14px;font-weight:600;color:var(--ink);margin-top:5px;line-height:1.4}
.pos{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.05em;padding:3px 9px;border-radius:999px;white-space:nowrap}
.pos.Open{background:rgba(28,107,69,.13);color:var(--green)}
.pos.Contested{background:rgba(200,16,46,.13);color:var(--red)}
.pos.Locked{background:rgba(16,23,37,.09);color:var(--ink3)}
.g1{font-size:10.5px;font-weight:700;padding:2px 7px;border-radius:999px;background:rgba(31,56,100,.11);color:var(--navy)}
.gcards{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}
.gcard{border:1px solid rgba(16,23,37,.1);border-radius:18px;padding:16px 17px;
 background:var(--glass2);border-left:4px solid rgba(16,23,37,.14)}
.gcard.Locked{border-left-color:var(--red)}
.gcard.Contested{border-left-color:var(--amber)}
.gcard.Open{border-left-color:var(--green)}
.gcard header{margin-bottom:11px}
.gcard h4{font-size:16.5px;font-weight:680;letter-spacing:-.01em;color:var(--ink);margin:0 0 8px}
.gcard .chips{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.gcard .warn{font-size:10.5px;font-weight:700;letter-spacing:.04em;padding:3px 9px;border-radius:999px;
 background:rgba(200,16,46,.12);color:var(--red)}
.gbody{display:grid;gap:7px;margin-bottom:12px}
.gr{display:grid;grid-template-columns:82px 1fr;gap:10px;font-size:12.8px;line-height:1.5}
.gk{font-size:10.5px;font-weight:700;letter-spacing:.055em;text-transform:uppercase;color:var(--ink3);padding-top:2px}
.gv{color:var(--ink2)}
.hook{padding:11px 13px;border-radius:13px;background:rgba(255,252,245,.92);
 border:1px solid rgba(168,100,0,.24);font-size:13px;line-height:1.55;color:var(--ink);margin-bottom:10px}
.hook b{color:var(--amber)}
.gnote{font-size:12.4px;line-height:1.6;color:var(--ink3);margin:0}
.empty{padding:44px 26px;text-align:center}
.empty h3{font-size:17px;font-weight:660;margin-bottom:8px}
.empty p{font-size:14px;color:var(--ink2);max-width:56ch;margin:0 auto 6px;line-height:1.6}
.empty .why{font-size:13px;color:var(--ink3);margin-top:14px}
footer{margin-top:24px;padding:20px 22px;font-size:12.5px;color:var(--ink3);line-height:1.7}
footer b{color:var(--ink2)}
@media(max-width:640px){.wrap{padding:0 14px}.hero{padding:20px 18px}.card{padding:17px 18px}
  nav.tabs{top:6px}.co{flex:1 1 100%}}
</style>
</head>
<body>
<div class="wrap">

<header>
  <div class="eyebrow">Stratasys competitive intelligence</div>
  <h1>Competitive Ad Intelligence</h1>
  <p class="sub">What competitors are advertising, what changed this week, and what to say about it on a call. Sources: LinkedIn Ad Library, Meta Ad Library, Google Ads Transparency Center, trade press.</p>
</header>

<div class="sect glass" role="group" aria-label="Section">
  <button class="sb" data-v="home" aria-pressed="true">Home</button>
  <button class="sb" data-v="competitors" aria-pressed="false">Competitors</button>
  <button class="sb" data-v="gauntlet" aria-pressed="false">Gauntlet</button>
</div>

<section class="view on" id="v-home">
  <div class="grid g3" id="homeKpis" style="margin:16px 0"></div>
  <div class="glass card"><h3>Signals this week</h3>
    <p class="cap">The few things worth acting on, across every tracked source.</p>
    <div class="grid g2" id="signals"></div></div>
  <div class="nav2" id="nav2"></div>
</section>

<section class="view" id="v-gauntlet">
  <div class="glass hero" style="margin-top:16px">
    <div class="lab">Why this matters</div>
    <h2 id="gHead"></h2>
    <div class="sowhat"><b>So what:</b> <span id="gWhy"></span></div>
  </div>
  <div class="gmeta" id="gMeta"></div>
  <div class="glass card"><h3>The 19 companies in Gauntlet II</h3>
    <p class="cap">Every one is a Stratasys prospect. Posture is displacement difficulty, not importance. Confidence is how well the competitor presence is evidenced.</p>
    <div class="tools"><input class="search" id="gq" placeholder="Search company, location, backer, technology, hook..." autocomplete="off"></div>
    <div class="gcards" id="gRows"></div>
    <p class="cap" style="margin:12px 0 0" id="gCount"></p></div>
  <div class="glass card"><h3>Sources</h3><p class="cap">Public reporting only. No non-public information.</p>
    <ul class="plain" id="gSrc"></ul></div>
</section>

<section class="view" id="v-competitors">
<div class="who" id="who" role="group" aria-label="Select competitor" style="margin-top:16px"></div>
<div class="pills" id="pills"></div>

<section class="glass hero" id="hero">
  <div class="lab">Key headline this week</div>
  <h2 id="hHead"></h2>
  <div class="sowhat"><b>So what:</b> <span id="hSo"></span></div>
</section>

<nav class="tabs glass" id="tabs" role="tablist">
  <button class="tab" role="tab" aria-selected="true"  data-p="brief">Sales Brief</button>
  <button class="tab" role="tab" aria-selected="false" data-p="changed">What Changed</button>
  <button class="tab" role="tab" aria-selected="false" data-p="ads">Ad Log</button>
  <button class="tab" role="tab" aria-selected="false" data-p="themes">Messaging</button>
  <button class="tab" role="tab" aria-selected="false" data-p="charts">Charts</button>
  <button class="tab" role="tab" aria-selected="false" data-p="watch">Watch</button>
  <button class="tab" role="tab" aria-selected="false" data-p="notes">Notes</button>
</nav>

<div id="pending" style="display:none">
  <div class="glass empty">
    <h3 id="peH"></h3>
    <p id="peB"></p>
    <p class="why" id="peW"></p>
  </div>
</div>

<div id="live">
<section class="panel on" id="p-brief">
  <div class="glass card"><h3>If they bring up this competitor, say this</h3>
    <p class="cap">Claims currently live in market, and the counter for each. Angles, not scripts.</p>
    <div class="grid g2" id="tt"></div></div>
  <div class="glass card"><h3>Where we are exposed</h3>
    <p class="cap">Ground they are taking that we consider ours.</p>
    <ul class="plain" id="expo"></ul></div>
  <div class="glass card"><h3>Where they are vulnerable</h3>
    <p class="cap">Gaps visible in their own live advertising.</p>
    <ul class="plain" id="vuln"></ul></div>
</section>

<section class="panel" id="p-changed">
  <div class="grid g3" id="kpis" style="margin-bottom:16px"></div>
  <div id="chg"></div>
  <div class="glass card"><h3>Creatives dropped since baseline</h3>
    <p class="cap">Present in the prior run, absent today. Paused, expired, or rotated out.</p>
    <div class="scroll"><table><thead><tr><th>Headline</th><th>CTA</th><th>Funnel</th><th>Note</th></tr></thead>
    <tbody id="drop"></tbody></table></div></div>
</section>

<section class="panel" id="p-ads">
  <div class="glass card"><h3>Ad Log</h3>
    <p class="cap" id="adCap">One row per unique creative. The same creative is served as multiple library entries; instance counts are in Notes.</p>
    <div class="tools"><input class="search" id="q" placeholder="Search headline, theme, audience, landing page..." autocomplete="off"></div>
    <div class="scroll"><table><thead><tr><th>Status</th><th>Theme</th><th>Headline / hook</th><th>Format</th>
      <th>CTA</th><th>Funnel</th><th>Impr</th><th>Est $/mo</th><th>Audience</th><th>Notes</th></tr></thead>
      <tbody id="rows"></tbody></table></div>
    <p class="cap" style="margin:12px 0 0" id="count"></p></div>
  <div class="glass card" id="partnerCard" hidden><h3>Partner and reseller ads</h3>
    <p class="cap">Ads run by resellers and distributors promoting this competitor's technology. Not counted in the instance totals above, because they are not the competitor's own spend. Often the more aggressive, bottom-funnel creative.</p>
    <div class="scroll"><table><thead><tr><th>Advertiser</th><th>Volume</th><th>What they are running</th></tr></thead>
      <tbody id="prows"></tbody></table></div></div>
</section>

<section class="panel" id="p-themes">
  <div class="glass card"><h3>Messaging themes</h3>
    <p class="cap">What they are actually claiming, and which buying committee role each theme speaks to.</p>
    <div class="scroll"><table><thead><tr><th>Theme</th><th>Unique</th><th>Live</th><th>Sample headline</th>
      <th>Funnel</th><th>Buying committee role</th></tr></thead><tbody id="th"></tbody></table></div></div>
</section>

<section class="panel" id="p-charts">
  <p class="cap" id="chartBasis" style="margin:16px 0 0"></p>
  <div class="grid g2">
    <div class="glass card"><h3>Theme mix</h3><p class="cap">Live instances by campaign theme</p><canvas id="c1"></canvas></div>
    <div class="glass card"><h3>Format mix</h3><p class="cap">Live instances by creative format</p><canvas id="c2"></canvas></div>
    <div class="glass card"><h3>Funnel distribution</h3><p class="cap">Where they are spending in the buying cycle</p><canvas id="c3"></canvas></div>
    <div class="glass card"><h3>Estimated spend by theme</h3><p class="cap">Low and high monthly bands. Directional only.</p><canvas id="c4"></canvas></div>
  </div>
</section>

<section class="panel" id="p-watch">
  <div class="glass card"><h3>Watch</h3>
    <p class="cap">Company and market intelligence behind the ads. Every claim carries a source.</p>
    <div id="watch"></div></div>
  <div class="glass card"><h3>Unverified and refuted</h3>
    <p class="cap">Tracked deliberately. Do not repeat these as fact.</p>
    <ul class="plain" id="unv"></ul></div>
</section>

<section class="panel" id="p-notes">
  <div class="glass card"><h3>Collection notes</h3>
    <p class="cap">Methodology and limitations. Read before quoting any number externally.</p>
    <div id="srcs"></div>
    <ul class="plain" style="margin-top:14px">
      <li><b>One row equals one unique creative.</b> LinkedIn serves the same creative as many separate library entries. Unique creatives and live instances are reported separately and are not interchangeable.</li>
      <li><b>Spend is a directional estimate</b>, never an actual budget. Impression figures are bands, not counts, so midpoint arithmetic compounds error.</li>
      <li><b>Google spend cannot be split by business unit.</b> The parent domain mixes all of a company's advertising together.</li>
      <li><b>Absence of evidence is not evidence of absence.</b> A keyword search returning nothing does not prove a competitor runs no ads there.</li>
      <li><b>Labels.</b> <code>[Inference]</code> is reasoning, <code>[Unverified]</code> is an uncorroborated claim, <code>[Estimate]</code> is modelled spend.</li>
    </ul></div>
</section>
</div>

</section>

<footer class="glass">
  <b>Last successful scan: <span id="fRun"></span></b> &middot; page built <span id="fBuilt"></span> &middot; next refresh Monday.<br>
  Internal use, Stratasys marketing and sales. Competitor ad copy is summarised, not reproduced, for customer-facing use.
</footer>

</div>
<script>
const P=%%DATA%%, CO=P.competitors, ORD=P.order, G=P.gauntlet;
const e=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const $=i=>document.getElementById(i);
const money=a=>a.lo||a.hi?"$"+(a.lo/1000)+"-"+(a.hi/1000)+"K":"n/a";
let cur=ORD[0], charts=[], drawnFor=null;

$("who").innerHTML=ORD.map(s=>{const d=CO[s],pend=d.status==="pending";
  return '<button class="co'+(pend?" pend":"")+'" data-s='+e(s)+' aria-pressed="'+(s===cur)+'">'+
  '<span class="n"><span class="dot '+(pend?"pend":"live")+'"></span>'+e(d.competitor)+"</span>"+
  '<span class="m">'+(pend?"Not yet scanned":
    (d.sources&&d.sources.linkedin&&d.sources.linkedin.unique_creatives!=null
      ? d.sources.linkedin.unique_creatives+(d.sources.linkedin.unique_creatives===1?" creative":" creatives")+" &middot; "+d.run_date
      : d.run_date))+"</span></button>";}).join("");

function render(s){
  cur=s; const D=CO[s];
  document.querySelectorAll(".co").forEach(b=>b.setAttribute("aria-pressed",b.dataset.s===s));
  $("hHead").textContent=D.headline; $("hSo").textContent=D.so_what;
  $("fRun").textContent=D.run_date; $("fBuilt").textContent=P.built;
  $("pills").innerHTML='<span class="pill">Tracking <b>'+e(D.competitor)+"</b></span>"+
    '<span class="pill">Run <b>'+e(D.run_date)+"</b></span>"+
    (D.baseline_date?'<span class="pill">vs baseline <b>'+e(D.baseline_date)+"</b></span>":"")+
    '<span class="pill">'+e(D.week_label||"")+"</span>";

  const pend=D.status==="pending";
  $("pending").style.display=pend?"block":"none";
  $("live").style.display=pend?"none":"block";
  $("tabs").style.display=pend?"none":"flex";
  if(pend){$("peH").textContent=D.headline;$("peB").textContent=D.so_what;
    $("peW").textContent=D.why_tracked||"";return;}

  $("tt").innerHTML=(D.talk_track||[]).map(t=>'<div class="glass tt"><span class="tag">'+e(t.tag)+
    '</span><div class="claim">'+e(t.claim)+'</div><span class="arrow">Counter</span><div class="ctr">'+
    e(t.counter)+"</div></div>").join("")||"<p class='cap'>No talk track recorded this run.</p>";
  $("expo").innerHTML=(D.exposure||[]).map(x=>"<li>"+e(x)+"</li>").join("")||"<li>Nothing flagged.</li>";
  const stale=(D.ads||[]).filter(a=>/stale|expired|passed|past the event|months? (stale|past)/i.test(a.notes||""));
  $("vuln").innerHTML=(stale.length?stale.map(a=>"<li><b>"+e(a.theme)+".</b> "+e(a.notes)+"</li>").join("")
    :"<li>No operational gaps flagged this run.</li>")+
    (D.sources&&D.sources.meta&&D.sources.meta.note?'<li><b>Platform concentration.</b> '+e(D.sources.meta.note)+"</li>":"");

  $("kpis").innerHTML=(D.kpis||[]).map(k=>{const g=k.dir==="down"?"&darr;":k.dir==="up"?"&uarr;":"&ndash;";
    return '<div class="glass kpi"><div class="k">'+e(k.label)+'</div><div class="v">'+e(k.value)+
    '</div><div class="d"><span class="dir '+e(k.dir)+'">'+g+"</span>"+e(k.delta)+"</div></div>";}).join("");
  $("chg").innerHTML=(D.changes||[]).map(c=>'<div class="glass chg"><div class="cat">'+e(c.cat)+
    "<span>"+c.items.length+"</span></div><ul>"+c.items.map(i=>'<li><div class="t">'+e(i.t)+
    '</div><div class="d">'+e(i.d)+(i.u?' <a class="src" href="'+e(i.u)+'" target="_blank" rel="noopener">source</a>':"")+
    "</div></li>").join("")+"</ul></div>").join("");
  $("drop").innerHTML=(D.dropped||[]).map(d=>"<tr><td class='hl'>"+e(d.headline)+"</td><td>"+e(d.cta)+
    '</td><td><span class="f">'+e(d.funnel)+"</span></td><td>"+e(d.note)+"</td></tr>").join("")
    ||'<tr><td colspan="4">Nothing dropped since the baseline.</td></tr>';

  $("q").value=""; rows("");
  $("th").innerHTML=(D.theme_detail||[]).map(t=>"<tr><td class='hl'>"+e(t[0])+"</td><td>"+t[1]+"</td><td>"+
    t[2]+"</td><td>"+e(t[3])+'</td><td><span class="f">'+e(t[4])+"</span></td><td>"+e(t[5])+"</td></tr>").join("");
  $("watch").innerHTML=(D.watch||[]).map(w=>'<div style="padding:12px 0;border-top:1px solid var(--hair)">'+
    '<div class="t" style="font-weight:600;font-size:14px;margin-bottom:5px">'+e(w.h)+
    '</div><div class="d" style="font-size:13.5px;color:var(--ink2)">'+e(w.b)+
    (w.u?' <a class="src" href="'+e(w.u)+'" target="_blank" rel="noopener">source</a>':"")+"</div></div>").join("");
  $("unv").innerHTML=(D.unverified||[]).map(u=>"<li>"+e(u)+"</li>").join("")||"<li>Nothing outstanding.</li>";
  $("srcs").innerHTML=Object.entries(D.sources||{}).map(([k,v])=>
    '<div style="padding:11px 0;border-top:1px solid var(--hair)">'+
    '<div style="font-weight:600;font-size:14px;text-transform:capitalize;margin-bottom:4px">'+e(k)+
    '</div><div style="font-size:13.5px;color:var(--ink2)">'+e(v.note||
    ((v.unique_creatives!=null?v.unique_creatives+" unique creatives, ":"")+
     (v.live_instances!=null?v.live_instances+" live instances.":"")))+"</div></div>").join("");

  drawnFor=null;
  if($("p-charts").classList.contains("on")) drawCharts();
}
function rows(f){
  const D=CO[cur], q=(f||"").toLowerCase();
  const r=(D.ads||[]).filter(a=>!q||JSON.stringify(a).toLowerCase().includes(q));
  $("rows").innerHTML=r.map(a=>{const isNew=/NEW/i.test(a.status||"");
    return "<tr"+(isNew?' class="new"':"")+'><td><span class="badge '+(isNew?"b-new":"b-carry")+'">'+
    (isNew?"NEW":"Carried")+'</span></td><td><span class="f">'+e(a.theme)+'</span></td><td class="hl">'+
    (a.url?'<a class="src" href="'+e(a.url)+'" target="_blank" rel="noopener">'+e(a.headline)+"</a>":e(a.headline))+
    "</td><td>"+e(a.format)+"</td><td>"+e(a.cta)+'</td><td><span class="f">'+e(a.funnel)+"</span></td><td>"+
    e(a.impr)+"</td><td>"+money(a)+"</td><td>"+e(a.audience)+"</td><td>"+e(a.notes)+"</td></tr>";}).join("")
    ||'<tr><td colspan="10">'+((D.ads||[]).length===0&&D.sources&&D.sources.linkedin&&D.sources.linkedin.checked
        ?"<b>Zero owned creatives found, and that is the finding.</b> "+e(D.sources.linkedin.note)
        :"No creatives match.")+'</td></tr>';
  const li=D.sources&&D.sources.linkedin;
  $("count").textContent=r.length+" of "+(D.ads||[]).length+" unique creatives shown."+
    (li&&li.live_instances!=null?" "+li.live_instances+" live instances total.":"");
  const cb=$("chartBasis");
  if(cb) cb.textContent = D.bucket_basis || "Counts are live LinkedIn ad instances, not unique creatives.";
  const pa=(D.partner_ads||[]);
  $("partnerCard").hidden=!pa.length;
  $("prows").innerHTML=pa.map(x=>"<tr><td class='hl'>"+e(x.advertiser)+"</td><td><span class='f'>"+
    e(x.count)+"</span></td><td>"+e(x.note)+(x.url?' <a class="src" href="'+e(x.url)+
    '" target="_blank" rel="noopener">source</a>':"")+"</td></tr>").join("");
}
$("q").addEventListener("input",ev=>rows(ev.target.value));
$("who").addEventListener("click",ev=>{const b=ev.target.closest(".co"); if(b) render(b.dataset.s);});
document.querySelectorAll(".tab").forEach(t=>t.addEventListener("click",()=>{
  document.querySelectorAll(".tab").forEach(x=>x.setAttribute("aria-selected",x===t));
  document.querySelectorAll(".panel").forEach(p=>p.classList.toggle("on",p.id==="p-"+t.dataset.p));
  if(t.dataset.p==="charts") drawCharts();
}));

function drawCharts(){
  if(drawnFor===cur) return; drawnFor=cur;
  charts.forEach(c=>c.destroy()); charts=[];
  const D=CO[cur];
  const PAL=["#c8102e","#1f3864","#2e7d4f","#d9a600","#1f6fb8","#d9701f","#7b5ea7","#4a5464"];
  const grid="rgba(16,23,37,.08)";
  Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'SF Pro Text',system-ui,sans-serif";
  Chart.defaults.color="#414b60"; Chart.defaults.borderColor=grid;
  const base={responsive:true,maintainAspectRatio:false,scales:{x:{grid:{color:grid}},y:{grid:{color:grid}}}},
        noL={plugins:{legend:{display:false}}};
  const mk=(id,cfg)=>{const el=$(id); if(el) charts.push(new Chart(el,cfg));};
  const th=Object.entries(D.themes||{}).sort((a,b)=>b[1]-a[1]);
  mk("c1",{type:"bar",data:{labels:th.map(x=>x[0]),datasets:[{data:th.map(x=>x[1]),
    backgroundColor:th.map((_,i)=>i?PAL[1]:PAL[0]),borderRadius:7}]},options:{...base,...noL,indexAxis:"y"}});
  const fm=Object.entries(D.formats||{}).sort((a,b)=>b[1]-a[1]);
  mk("c2",{type:"doughnut",data:{labels:fm.map(x=>x[0]),datasets:[{data:fm.map(x=>x[1]),
    backgroundColor:PAL,borderWidth:0}]},options:{responsive:true,maintainAspectRatio:false,cutout:"62%",
    plugins:{legend:{position:"right",labels:{boxWidth:11,usePointStyle:true,pointStyle:"circle"}}}}});
  const O=["Top","Mid","Bottom","n/a"],fu=Object.entries(D.funnels||{}).sort((a,b)=>O.indexOf(a[0])-O.indexOf(b[0]));
  mk("c3",{type:"bar",data:{labels:fu.map(x=>x[0]),datasets:[{data:fu.map(x=>x[1]),
    backgroundColor:PAL[1],borderRadius:7}]},options:{...base,...noL}});
  const sp={}; (D.ads||[]).forEach(a=>{const k=a.theme;sp[k]=sp[k]||[0,0];sp[k][0]+=a.lo||0;sp[k][1]+=a.hi||0;});
  const se=Object.entries(sp).sort((a,b)=>b[1][1]-a[1][1]);
  mk("c4",{type:"bar",data:{labels:se.map(x=>x[0]),datasets:[
    {label:"Low",data:se.map(x=>x[1][0]),backgroundColor:PAL[1],borderRadius:6},
    {label:"High",data:se.map(x=>x[1][1]),backgroundColor:PAL[0],borderRadius:6}]},
    options:{...base,plugins:{legend:{position:"top",labels:{boxWidth:11,usePointStyle:true,pointStyle:"circle"}}}}});
}

/* ---- section switching ---- */
document.querySelectorAll(".sb").forEach(b=>b.addEventListener("click",()=>{
  document.querySelectorAll(".sb").forEach(x=>x.setAttribute("aria-pressed",x===b));
  document.querySelectorAll(".view").forEach(v=>v.classList.toggle("on",v.id==="v-"+b.dataset.v));
  window.scrollTo({top:0,behavior:"smooth"});
  if(b.dataset.v==="competitors"&&$("p-charts").classList.contains("on")){drawnFor=null;drawCharts();}
}));
function go(v){document.querySelector('.sb[data-v="'+v+'"]').click();}

/* ---- home ---- */
function home(){
  const live=ORD.filter(s=>CO[s].status!=="pending");
  const ads=live.reduce((n,s)=>n+(CO[s].ads||[]).length,0);
  const inst=live.reduce((n,s)=>n+((CO[s].sources&&CO[s].sources.linkedin&&CO[s].sources.linkedin.live_instances)||0),0);
  const nw=live.reduce((n,s)=>n+(CO[s].ads||[]).filter(a=>/NEW/i.test(a.status||"")).length,0);
  const contested=G?G.teams.filter(t=>t.posture==="Contested").length:0;
  const K=[
   {label:"Competitors tracked",value:ORD.length,delta:live.length+" scanned, "+(ORD.length-live.length)+" awaiting first run",dir:"flat"},
   {label:"Unique creatives",value:ads,delta:"Across all scanned competitors",dir:"flat"},
   {label:"Live instances",value:inst||"n/a",delta:"LinkedIn, where reported",dir:"flat"},
   {label:"New this week",value:nw,delta:nw?"Flagged in the ad logs":"No new creatives",dir:nw?"up":"flat"},
   {label:"Gauntlet II field",value:G?G.teams.length:0,delta:"Pre-qualified drone prospects",dir:"flat"},
   {label:"Contested accounts",value:contested,delta:contested?"A competitor is already present":"None confirmed yet",dir:contested?"down":"flat"}];
  $("homeKpis").innerHTML=K.map(k=>{const g=k.dir==="down"?"&darr;":k.dir==="up"?"&uarr;":"&ndash;";
    return '<div class="glass kpi"><div class="k">'+e(k.label)+'</div><div class="v">'+e(k.value)+
    '</div><div class="d"><span class="dir '+k.dir+'">'+g+"</span>"+e(k.delta)+"</div></div>";}).join("");

  const sig=[];
  if(G&&G.headline_signal) sig.push({l:"Gauntlet",h:G.headline_signal,
    b:"This is the core objection to the entire drone additive pitch, ours and HP's alike, and it is coming from a Gauntlet 1 award winner. Have an answer before a prospect quotes it back."});
  live.forEach(s=>{const d=CO[s]; if(d.headline) sig.push({l:d.competitor,h:d.headline,b:d.so_what||""});});
  $("signals").innerHTML=sig.map(x=>'<div class="glass sig"><div class="l">'+e(x.l)+
    '</div><div class="h">'+e(x.h)+'</div><div class="b">'+e(x.b)+"</div></div>").join("");

  $("nav2").innerHTML=
   '<button class="ncard" data-go="competitors"><span class="t">Competitors</span>'+
   '<span class="d">Ad logs, messaging themes, weekly diffs and a sales brief for '+ORD.length+
   ' competitors.</span><span class="go">Open competitors &rarr;</span></button>'+
   (G?'<button class="ncard" data-go="gauntlet"><span class="t">Drone Dominance Gauntlet</span>'+
   '<span class="d">'+G.teams.length+' pre-qualified drone manufacturers, who is already in each account, and where we can still win.</span>'+
   '<span class="go">Open gauntlet &rarr;</span></button>':"");
  document.querySelectorAll(".ncard").forEach(c=>c.addEventListener("click",()=>go(c.dataset.go)));
}

/* ---- gauntlet ---- */
function gaunt(){
  if(!G) return;
  $("gHead").textContent=G.headline_signal||G.stage;
  $("gWhy").textContent=G.why_it_matters;
  $("gMeta").innerHTML=[["Program",G.program],["Value",G.value],["Stage",G.stage],
    ["Selection funnel",G.funnel],["Requirement",G.requirement],["Sponsor",G.sponsor]]
    .filter(x=>x[1]).map(x=>'<div class="glass gm"><div class="k">'+e(x[0])+'</div><div class="v">'+e(x[1])+"</div></div>").join("");
  $("gSrc").innerHTML=(G.sources||[]).map(s=>'<li><a class="src" href="'+e(s.u)+
    '" target="_blank" rel="noopener">'+e(s.t)+"</a></li>").join("");
  grows("");
  $("gq").addEventListener("input",ev=>grows(ev.target.value));
}
function grows(f){
  const q=(f||"").toLowerCase();
  const r=G.teams.filter(t=>!q||JSON.stringify(t).toLowerCase().includes(q));
  const row=(l,v)=>v?'<div class="gr"><span class="gk">'+l+'</span><span class="gv">'+e(v)+'</span></div>':"";
  $("gRows").innerHTML=r.map(t=>
    '<article class="gcard '+e(t.posture)+'">'+
      '<header><h4>'+e(t.company)+(t.gauntlet1?' <span class="g1">G1</span>':"")+'</h4>'+
      '<div class="chips"><span class="pos '+e(t.posture)+'">'+e(t.posture)+'</span>'+
      '<span class="f">AM stance: '+e(t.am_posture||"Unknown")+'</span>'+
      '<span class="f">'+e(t.confidence)+'</span>'+
      (t.competitor_presence?'<span class="warn">'+e(t.competitor_presence)+'</span>':"")+
      '</div></header>'+
      '<div class="gbody">'+
        row("Based",t.hq)+row("Backing",t.backing)+row("Scale",t.scale)+row("Technology",t.tech)+
      '</div>'+
      (t.sales_hook?'<div class="hook"><b>Sales hook:</b> '+e(t.sales_hook)+'</div>':"")+
      '<p class="gnote">'+e(t.notes)+(t.evidence_url?' <a class="src" href="'+e(t.evidence_url)+
        '" target="_blank" rel="noopener">source</a>':"")+'</p>'+
    '</article>').join("")
    ||'<p class="cap">No companies match.</p>';
  const loc=G.teams.filter(t=>t.posture==="Locked").length,
        con=G.teams.filter(t=>t.posture==="Contested").length;
  $("gCount").textContent=r.length+" of "+G.teams.length+" companies shown. "+
    G.teams.filter(t=>t.gauntlet1).length+" returning from Gauntlet I. "+
    loc+" locked by a competitor, "+con+" contested, "+(G.teams.length-loc-con)+" open.";
}

render(cur); home(); gaunt();
</script>
</body>
</html>
"""

html = TPL.replace("%%DATA%%", json.dumps(PAYLOAD, ensure_ascii=False, separators=(",", ":")))
out = os.path.join(ROOT, "index.html")
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
live = [s for s in order if C[s].get("status") != "pending"]
print("built index.html: %d competitors (%d live, %d pending), %d KB"
      % (len(order), len(live), len(order) - len(live), len(html) // 1024))
