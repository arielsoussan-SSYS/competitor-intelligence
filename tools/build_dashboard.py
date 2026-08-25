#!/usr/bin/env python3
"""Build index.html from the latest run file in data/.

The data file is the asset. This script is only a view of it.
Usage: python3 tools/build_dashboard.py [data/YYYY-MM-DD-slug.json]
"""
import json, sys, glob, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def latest():
    files = sorted(glob.glob(os.path.join(ROOT, "data", "20*-*.json")))
    if not files:
        sys.exit("No run files in data/")
    return files[-1]

src = sys.argv[1] if len(sys.argv) > 1 else latest()
D = json.load(open(src, encoding="utf-8"))
D["built"] = datetime.date.today().isoformat()

TPL = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Competitive Ad Intelligence &middot; Stratasys</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --ink:#0b0f1a; --ink2:#3c4457; --ink3:#6b7488;
  --glass:rgba(255,255,255,.62); --glass2:rgba(255,255,255,.45);
  --stroke:rgba(255,255,255,.75); --hair:rgba(11,15,26,.09);
  --shadow:0 1px 2px rgba(11,15,26,.05),0 8px 30px rgba(11,15,26,.09);
  --navy:#1f3864; --red:#c8102e; --amber:#b06a00; --green:#1f6b45;
  --bg1:#eef2fb; --bg2:#e7ecf7;
  --r:24px;
}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){
  --ink:#f2f5fb; --ink2:#b9c2d4; --ink3:#8b94a8;
  --glass:rgba(28,33,46,.62); --glass2:rgba(28,33,46,.45);
  --stroke:rgba(255,255,255,.12); --hair:rgba(255,255,255,.10);
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 34px rgba(0,0,0,.44);
  --navy:#93b4f0; --red:#ff7a8f; --amber:#e3a838; --green:#5ec894;
  --bg1:#0b0f1a; --bg2:#121826;
}}
html{-webkit-text-size-adjust:100%}
body{
  font:15px/1.5 -apple-system,BlinkMacSystemFont,"SF Pro Text","SF Pro Display",
       "Segoe UI",Inter,system-ui,sans-serif;
  color:var(--ink); background:var(--bg1);
  letter-spacing:-.011em; -webkit-font-smoothing:antialiased;
  min-height:100vh; padding-bottom:64px;
}
body::before{
  content:""; position:fixed; inset:0; z-index:-1; background:
    radial-gradient(58vw 52vw at 8% -6%, rgba(200,16,46,.20), transparent 62%),
    radial-gradient(52vw 48vw at 96% 4%, rgba(31,56,100,.26), transparent 60%),
    radial-gradient(60vw 55vw at 46% 104%, rgba(60,140,200,.20), transparent 62%),
    linear-gradient(170deg,var(--bg1),var(--bg2));
}
.wrap{max-width:1180px;margin:0 auto;padding:0 18px}
.glass{
  background:var(--glass);
  -webkit-backdrop-filter:blur(32px) saturate(185%);
  backdrop-filter:blur(32px) saturate(185%);
  border:1px solid var(--stroke); border-radius:var(--r); box-shadow:var(--shadow);
}
/* header */
header{padding:34px 0 16px}
.eyebrow{font-size:11px;font-weight:660;letter-spacing:.1em;text-transform:uppercase;color:var(--ink3)}
h1{font-size:clamp(26px,4.4vw,38px);font-weight:700;letter-spacing:-.028em;margin:6px 0 8px}
.sub{color:var(--ink2);font-size:14px;max-width:70ch}
.pills{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.pill{font-size:12px;font-weight:600;padding:6px 12px;border-radius:999px;
  background:var(--glass2);border:1px solid var(--stroke);color:var(--ink2);
  -webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.pill b{color:var(--ink)}
/* hero */
.hero{padding:26px 26px 22px;margin:18px 0;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;inset:0 0 auto 0;height:3px;
  background:linear-gradient(90deg,var(--red),var(--navy))}
.hero .lab{font-size:11px;font-weight:660;letter-spacing:.1em;text-transform:uppercase;color:var(--red)}
.hero h2{font-size:clamp(19px,2.7vw,25px);font-weight:660;letter-spacing:-.022em;margin:10px 0 14px;line-height:1.32}
.sowhat{padding:14px 16px;border-radius:16px;background:var(--glass2);
  border:1px solid var(--stroke);border-left:3px solid var(--amber);font-size:14px;color:var(--ink2)}
.sowhat b{color:var(--ink)}
/* tabs */
nav.tabs{position:sticky;top:10px;z-index:30;margin:18px 0;padding:5px;
  display:flex;gap:3px;overflow-x:auto;scrollbar-width:none}
nav.tabs::-webkit-scrollbar{display:none}
.tab{flex:0 0 auto;border:0;cursor:pointer;font:inherit;font-size:13.5px;font-weight:600;
  color:var(--ink2);background:transparent;padding:9px 15px;border-radius:16px;
  transition:background .18s,color .18s,transform .18s}
.tab:hover{color:var(--ink)}
.tab[aria-selected=true]{background:var(--glass);color:var(--ink);box-shadow:var(--shadow)}
.panel{display:none;animation:in .32s cubic-bezier(.22,.9,.3,1)}
.panel.on{display:block}
@keyframes in{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.panel{animation:none}}
/* blocks */
.card{padding:20px 22px;margin-bottom:16px}
.card h3{font-size:16px;font-weight:660;letter-spacing:-.018em;margin-bottom:4px}
.card .cap{font-size:13px;color:var(--ink3);margin-bottom:16px}
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}
/* kpi */
.kpi{padding:16px 18px}
.kpi .k{font-size:11px;font-weight:660;letter-spacing:.06em;text-transform:uppercase;color:var(--ink3)}
.kpi .v{font-size:30px;font-weight:700;letter-spacing:-.03em;margin:6px 0 4px;
  font-variant-numeric:tabular-nums}
.kpi .d{font-size:12.5px;color:var(--ink2);line-height:1.42}
.dir{display:inline-block;font-weight:700;margin-right:5px}
.dir.down{color:var(--red)}.dir.up{color:var(--green)}.dir.flat{color:var(--ink3)}
/* talk track */
.tt{padding:18px 20px}
.tt .tag{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.07em;
  text-transform:uppercase;color:var(--red);margin-bottom:9px}
.tt .claim{font-size:14.5px;font-weight:600;line-height:1.45;margin-bottom:11px;color:var(--ink)}
.tt .arrow{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--green);display:block;margin-bottom:5px}
.tt .ctr{font-size:14px;color:var(--ink2);line-height:1.55}
/* change list */
.chg{margin-bottom:14px;padding:16px 18px}
.chg .cat{font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;
  color:var(--navy);margin-bottom:12px;display:flex;align-items:center;gap:8px}
.chg .cat span{font-size:10.5px;background:var(--glass2);border:1px solid var(--stroke);
  border-radius:999px;padding:2px 8px;color:var(--ink3)}
.chg li{list-style:none;padding:12px 0;border-top:1px solid var(--hair)}
.chg li:first-of-type{border-top:0;padding-top:0}
.chg .t{font-weight:600;font-size:14px;margin-bottom:5px;line-height:1.45}
.chg .d{font-size:13.5px;color:var(--ink2);line-height:1.55}
a.src{font-size:12px;color:var(--navy);text-decoration:none;font-weight:600;
  border-bottom:1px solid transparent;transition:border-color .15s}
a.src:hover{border-bottom-color:currentColor}
ul.plain li{list-style:none;padding:11px 0;border-top:1px solid var(--hair);
  font-size:14px;color:var(--ink2);line-height:1.55}
ul.plain li:first-child{border-top:0;padding-top:0}
ul.plain b{color:var(--ink)}
/* table */
.tools{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
input.search{flex:1;min-width:220px;font:inherit;font-size:14px;padding:11px 15px;
  border-radius:14px;border:1px solid var(--stroke);background:var(--glass2);color:var(--ink);
  -webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);outline:none}
input.search:focus{border-color:var(--navy);box-shadow:0 0 0 3.5px rgba(31,56,100,.16)}
input.search::placeholder{color:var(--ink3)}
.scroll{overflow-x:auto;border-radius:16px;border:1px solid var(--hair)}
table{border-collapse:collapse;width:100%;font-size:13px;min-width:760px}
th{background:var(--glass2);text-align:left;padding:11px 13px;font-size:11px;font-weight:660;
  letter-spacing:.06em;text-transform:uppercase;color:var(--ink3);
  position:sticky;top:0;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
td{padding:12px 13px;border-top:1px solid var(--hair);vertical-align:top;color:var(--ink2)}
td.hl{color:var(--ink);font-weight:550;max-width:340px}
tr.new td{background:rgba(31,107,69,.09)}
.badge{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.05em;
  padding:3px 8px;border-radius:999px;white-space:nowrap}
.b-new{background:rgba(31,107,69,.16);color:var(--green)}
.b-carry{background:var(--glass2);color:var(--ink3);border:1px solid var(--stroke)}
.b-drop{background:rgba(200,16,46,.14);color:var(--red)}
.f{font-size:11px;font-weight:660;color:var(--ink3)}
canvas{max-height:270px}
footer{margin-top:26px;padding:20px 22px;font-size:12.5px;color:var(--ink3);line-height:1.7}
footer b{color:var(--ink2)}
@media(max-width:640px){
  .wrap{padding:0 14px} .hero{padding:20px 18px} .card{padding:17px 18px}
  nav.tabs{top:6px}
}
</style>
</head>
<body>
<div class="wrap">

<header>
  <div class="eyebrow">Stratasys competitive intelligence</div>
  <h1>Competitive Ad Intelligence</h1>
  <p class="sub">What competitors are advertising, what changed this week, and what to say about it on a call. Sources: LinkedIn Ad Library, Meta Ad Library, Google Ads Transparency Center, trade press.</p>
  <div class="pills">
    <span class="pill">Tracking <b id="pComp"></b></span>
    <span class="pill">Run <b id="pRun"></b></span>
    <span class="pill">vs baseline <b id="pBase"></b></span>
    <span class="pill" id="pWeek"></span>
  </div>
</header>

<section class="glass hero">
  <div class="lab">Key headline this week</div>
  <h2 id="hHead"></h2>
  <div class="sowhat"><b>So what:</b> <span id="hSo"></span></div>
</section>

<nav class="tabs glass" role="tablist">
  <button class="tab" role="tab" aria-selected="true"  data-p="brief">Sales Brief</button>
  <button class="tab" role="tab" aria-selected="false" data-p="changed">What Changed</button>
  <button class="tab" role="tab" aria-selected="false" data-p="ads">Ad Log</button>
  <button class="tab" role="tab" aria-selected="false" data-p="themes">Messaging</button>
  <button class="tab" role="tab" aria-selected="false" data-p="charts">Charts</button>
  <button class="tab" role="tab" aria-selected="false" data-p="watch">Watch</button>
  <button class="tab" role="tab" aria-selected="false" data-p="notes">Notes</button>
</nav>

<section class="panel on" id="p-brief">
  <div class="glass card">
    <h3>If they bring up the competitor, say this</h3>
    <p class="cap">Claims currently live in market, and the counter for each. Do not read these verbatim, they are angles, not scripts.</p>
    <div class="grid g2" id="tt"></div>
  </div>
  <div class="glass card">
    <h3>Where we are exposed</h3>
    <p class="cap">Messaging ground they are taking that we consider ours.</p>
    <ul class="plain" id="expo"></ul>
  </div>
  <div class="glass card">
    <h3>Where they are vulnerable</h3>
    <p class="cap">Operational gaps visible in their own live advertising.</p>
    <ul class="plain" id="vuln"></ul>
  </div>
</section>

<section class="panel" id="p-changed">
  <div class="grid g3" id="kpis" style="margin-bottom:16px"></div>
  <div id="chg"></div>
  <div class="glass card">
    <h3>Creatives dropped since baseline</h3>
    <p class="cap">Present in the prior run, absent today. Paused, expired, or rotated out.</p>
    <div class="scroll"><table><thead><tr><th>Headline</th><th>CTA</th><th>Funnel</th><th>Note</th></tr></thead><tbody id="drop"></tbody></table></div>
  </div>
</section>

<section class="panel" id="p-ads">
  <div class="glass card">
    <h3>Ad Log</h3>
    <p class="cap">One row per unique creative. The same creative is served as multiple library entries; instance counts are in Notes.</p>
    <div class="tools"><input class="search" id="q" placeholder="Search headline, theme, audience, landing page..." autocomplete="off"></div>
    <div class="scroll"><table>
      <thead><tr><th>Status</th><th>Theme</th><th>Headline / hook</th><th>Format</th><th>CTA</th><th>Funnel</th><th>Impr</th><th>Est $/mo</th><th>Audience</th><th>Notes</th></tr></thead>
      <tbody id="rows"></tbody></table></div>
    <p class="cap" style="margin:12px 0 0" id="count"></p>
  </div>
</section>

<section class="panel" id="p-themes">
  <div class="glass card">
    <h3>Messaging themes</h3>
    <p class="cap">What they are actually claiming, and which buying committee role each theme speaks to.</p>
    <div class="scroll"><table><thead><tr><th>Theme</th><th>Unique</th><th>Live</th><th>Sample headline</th><th>Funnel</th><th>Buying committee role</th></tr></thead><tbody id="th"></tbody></table></div>
  </div>
</section>

<section class="panel" id="p-charts">
  <div class="grid g2">
    <div class="glass card"><h3>Theme mix</h3><p class="cap">Live instances by campaign theme</p><canvas id="c1"></canvas></div>
    <div class="glass card"><h3>Format mix</h3><p class="cap">Live instances by creative format</p><canvas id="c2"></canvas></div>
    <div class="glass card"><h3>Funnel distribution</h3><p class="cap">Where they are spending in the buying cycle</p><canvas id="c3"></canvas></div>
    <div class="glass card"><h3>Estimated spend by theme</h3><p class="cap">Low and high monthly bands. Directional only.</p><canvas id="c4"></canvas></div>
  </div>
</section>

<section class="panel" id="p-watch">
  <div class="glass card">
    <h3>Watch</h3>
    <p class="cap">Company and market intelligence behind the ads. Every claim carries a source.</p>
    <div id="watch"></div>
  </div>
  <div class="glass card">
    <h3>Unverified and refuted</h3>
    <p class="cap">Tracked deliberately. Do not repeat these as fact.</p>
    <ul class="plain" id="unv"></ul>
  </div>
</section>

<section class="panel" id="p-notes">
  <div class="glass card">
    <h3>Collection notes</h3>
    <p class="cap">Methodology and limitations. Read before quoting any number externally.</p>
    <div id="srcs"></div>
    <ul class="plain" style="margin-top:14px">
      <li><b>One row equals one unique creative.</b> LinkedIn serves the same creative as many separate library entries. Unique creatives and live instances are reported separately and are not interchangeable.</li>
      <li><b>Spend is a directional estimate</b>, never an actual budget. LinkedIn impression midpoint times a $30-80 B2B CPM. Impression figures are bands, not counts, so midpoint arithmetic compounds error.</li>
      <li><b>Google spend cannot be split by business unit.</b> The parent domain mixes all of the company's advertising together.</li>
      <li><b>Absence of evidence is not evidence of absence.</b> A keyword search returning nothing does not prove a competitor runs no ads there.</li>
      <li><b>Labels.</b> <code>[Inference]</code> is reasoning, <code>[Unverified]</code> is an uncorroborated claim, <code>[Estimate]</code> is modelled spend.</li>
    </ul>
  </div>
</section>

<footer class="glass">
  <b>Last successful scan: <span id="fRun"></span></b> &middot; built <span id="fBuilt"></span> &middot; next refresh Monday.<br>
  Internal use, Stratasys marketing and sales. Competitor ad copy is summarised, not reproduced, for customer-facing use.
</footer>

</div>
<script>
const D=%%DATA%%;
const e=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const $=i=>document.getElementById(i);
const money=a=>"$"+(a.lo/1000)+"-"+(a.hi/1000)+"K";

$("pComp").textContent=D.competitor; $("pRun").textContent=D.run_date;
$("pBase").textContent=D.baseline_date; $("pWeek").textContent=D.week_label||"";
$("hHead").textContent=D.headline; $("hSo").textContent=D.so_what;
$("fRun").textContent=D.run_date; $("fBuilt").textContent=D.built;

$("tt").innerHTML=(D.talk_track||[]).map(t=>
  '<div class="glass tt"><span class="tag">'+e(t.tag)+'</span><div class="claim">'+e(t.claim)+
  '</div><span class="arrow">Counter</span><div class="ctr">'+e(t.counter)+'</div></div>').join("");
$("expo").innerHTML=(D.exposure||[]).map(x=>"<li>"+e(x)+"</li>").join("");

const stale=D.ads.filter(a=>/stale|past|expired|passed|months? stale/i.test(a.notes||""));
$("vuln").innerHTML=(stale.length?stale.map(a=>"<li><b>"+e(a.theme)+".</b> "+e(a.notes)+"</li>").join("")
  :"<li>No operational gaps flagged this run.</li>")
  +'<li><b>Platform concentration.</b> '+e(D.sources&&D.sources.meta?D.sources.meta.note:"")+"</li>";

$("kpis").innerHTML=(D.kpis||[]).map(k=>{
  const s=k.dir==="down"?"&darr;":k.dir==="up"?"&uarr;":"&ndash;";
  return '<div class="glass kpi"><div class="k">'+e(k.label)+'</div><div class="v">'+e(k.value)+
  '</div><div class="d"><span class="dir '+e(k.dir)+'">'+s+"</span>"+e(k.delta)+"</div></div>";}).join("");

$("chg").innerHTML=(D.changes||[]).map(c=>
  '<div class="glass chg"><div class="cat">'+e(c.cat)+"<span>"+c.items.length+"</span></div><ul>"+
  c.items.map(i=>'<li><div class="t">'+e(i.t)+'</div><div class="d">'+e(i.d)+
  (i.u?' <a class="src" href="'+e(i.u)+'" target="_blank" rel="noopener">source</a>':"")+
  "</div></li>").join("")+"</ul></div>").join("");

$("drop").innerHTML=(D.dropped||[]).map(d=>"<tr><td class='hl'>"+e(d.headline)+"</td><td>"+e(d.cta)+
  '</td><td><span class="f">'+e(d.funnel)+"</span></td><td>"+e(d.note)+"</td></tr>").join("")
  ||'<tr><td colspan="4">Nothing dropped since the baseline.</td></tr>';

function draw(f){
  const q=(f||"").toLowerCase();
  const r=D.ads.filter(a=>!q||JSON.stringify(a).toLowerCase().includes(q));
  $("rows").innerHTML=r.map(a=>{
    const isNew=/NEW/i.test(a.status);
    return "<tr"+(isNew?' class="new"':"")+'><td><span class="badge '+(isNew?"b-new":"b-carry")+'">'+
    e(isNew?"NEW":"Carried")+'</span></td><td><span class="f">'+e(a.theme)+"</span></td>"+
    '<td class="hl"><a class="src" href="'+e(a.url)+'" target="_blank" rel="noopener">'+e(a.headline)+"</a></td>"+
    "<td>"+e(a.format)+"</td><td>"+e(a.cta)+'</td><td><span class="f">'+e(a.funnel)+"</span></td><td>"+
    e(a.impr)+"</td><td>"+money(a)+"</td><td>"+e(a.audience)+"</td><td>"+e(a.notes)+"</td></tr>";}).join("");
  $("count").textContent=r.length+" of "+D.ads.length+" unique creatives shown. "+
    (D.sources&&D.sources.linkedin?D.sources.linkedin.live_instances+" live instances total.":"");
}
draw(""); $("q").addEventListener("input",ev=>draw(ev.target.value));

$("th").innerHTML=(D.theme_detail||[]).map(t=>"<tr><td class='hl'>"+e(t[0])+"</td><td>"+t[1]+
  "</td><td>"+t[2]+"</td><td>"+e(t[3])+'</td><td><span class="f">'+e(t[4])+"</span></td><td>"+e(t[5])+"</td></tr>").join("");

$("watch").innerHTML=(D.watch||[]).map(w=>'<div class="chg" style="border:0;box-shadow:none;padding:12px 0;border-top:1px solid var(--hair)">'+
  '<div class="t">'+e(w.h)+'</div><div class="d">'+e(w.b)+
  (w.u?' <a class="src" href="'+e(w.u)+'" target="_blank" rel="noopener">source</a>':"")+"</div></div>").join("");
$("unv").innerHTML=(D.unverified||[]).map(u=>"<li>"+e(u)+"</li>").join("");
$("srcs").innerHTML=Object.entries(D.sources||{}).map(([k,v])=>
  '<div class="chg" style="border:0;box-shadow:none;padding:11px 0;border-top:1px solid var(--hair)">'+
  '<div class="t" style="text-transform:capitalize">'+e(k)+"</div><div class='d'>"+
  e(v.note||((v.unique_creatives!=null?v.unique_creatives+" unique creatives, ":"")+
  (v.live_instances!=null?v.live_instances+" live instances.":"")))+"</div></div>").join("");

let drawn=false;
document.querySelectorAll(".tab").forEach(t=>t.addEventListener("click",()=>{
  document.querySelectorAll(".tab").forEach(x=>x.setAttribute("aria-selected",x===t));
  document.querySelectorAll(".panel").forEach(p=>p.classList.toggle("on",p.id==="p-"+t.dataset.p));
  if(t.dataset.p==="charts"&&!drawn){drawn=true;charts();}
}));

function charts(){
  const dark=matchMedia("(prefers-color-scheme:dark)").matches;
  const ink=dark?"#b9c2d4":"#3c4457", grid=dark?"rgba(255,255,255,.09)":"rgba(11,15,26,.08)";
  const P=["#c8102e","#1f3864","#2e7d4f","#d9a600","#1f6fb8","#d9701f","#7b5ea7","#4a5464"];
  Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'SF Pro Text',system-ui,sans-serif";
  Chart.defaults.color=ink; Chart.defaults.borderColor=grid;
  const noL={plugins:{legend:{display:false}}},
        base={responsive:true,maintainAspectRatio:false,
              scales:{x:{grid:{color:grid}},y:{grid:{color:grid}}}};
  const th=Object.entries(D.themes).sort((a,b)=>b[1]-a[1]);
  new Chart($("c1"),{type:"bar",data:{labels:th.map(x=>x[0]),
    datasets:[{data:th.map(x=>x[1]),backgroundColor:th.map((_,i)=>i?P[1]:P[0]),borderRadius:7}]},
    options:{...base,...noL,indexAxis:"y"}});
  const fm=Object.entries(D.formats).sort((a,b)=>b[1]-a[1]);
  new Chart($("c2"),{type:"doughnut",data:{labels:fm.map(x=>x[0]),
    datasets:[{data:fm.map(x=>x[1]),backgroundColor:P,borderWidth:0}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:"62%",
    plugins:{legend:{position:"right",labels:{boxWidth:11,usePointStyle:true,pointStyle:"circle"}}}}});
  const ORD=["Top","Mid","Bottom"],fu=Object.entries(D.funnels)
    .sort((a,b)=>ORD.indexOf(a[0])-ORD.indexOf(b[0]));
  new Chart($("c3"),{type:"bar",data:{labels:fu.map(x=>x[0]),
    datasets:[{data:fu.map(x=>x[1]),backgroundColor:P[1],borderRadius:7}]},options:{...base,...noL}});
  const sp={}; D.ads.forEach(a=>{const k=a.theme;sp[k]=sp[k]||[0,0];sp[k][0]+=a.lo;sp[k][1]+=a.hi;});
  const se=Object.entries(sp).sort((a,b)=>b[1][1]-a[1][1]);
  new Chart($("c4"),{type:"bar",data:{labels:se.map(x=>x[0]),datasets:[
    {label:"Low",data:se.map(x=>x[1][0]),backgroundColor:P[1],borderRadius:6},
    {label:"High",data:se.map(x=>x[1][1]),backgroundColor:P[0],borderRadius:6}]},
    options:{...base,plugins:{legend:{position:"top",labels:{boxWidth:11,usePointStyle:true,pointStyle:"circle"}}}}});
}
</script>
</body>
</html>
"""

html = TPL.replace("%%DATA%%", json.dumps(D, ensure_ascii=False, separators=(",", ":")))
out = os.path.join(ROOT, "index.html")
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print("built %s from %s (%d KB, %d ads)" % (
    os.path.basename(out), os.path.basename(src), len(html) // 1024, len(D["ads"])))
