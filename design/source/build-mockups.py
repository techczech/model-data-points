import html, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") + os.sep
CSS = """
:root{--bg:#fbfaf7;--fg:#1d2433;--card:#f6f5f1;--primary:#202f61;--sec:#eee6db;--mut:#626e83;--acc:#f0a830;--bd:#e8e2d9;--open:#2f7a55;--closed:#8a5a1c;--tan:#f7ecda}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Inter,system-ui,-apple-system,"Segoe UI",sans-serif}
h1,h2,h3,.serif{font-family:"Source Serif 4",Georgia,"Times New Roman",serif;letter-spacing:-.01em}
a{color:var(--primary)}
.badge{position:fixed;top:8px;left:8px;z-index:100;background:#1f8a4c;color:#fff;font:600 12px/1 Inter,system-ui,sans-serif;padding:7px 10px;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.25)}
.wrap{max-width:1072px;margin:0 auto;padding:0 16px}
header.site{position:sticky;top:0;z-index:50;background:rgba(251,250,247,.96);border-bottom:1px solid var(--bd)}
header.site .wrap{display:flex;align-items:center;justify-content:space-between;height:64px;gap:12px}
.logo{display:flex;align-items:center;gap:8px;text-decoration:none;color:var(--fg)}
.logo b{display:inline-flex;width:36px;height:36px;border-radius:8px;background:var(--primary);color:#fbfaf7;align-items:center;justify-content:center;font:700 18px Georgia,serif}
.logo span{font:600 20px Georgia,serif}
nav.main{display:flex;gap:4px;flex-wrap:wrap}
nav.main a{padding:8px 14px;border-radius:6px;font-size:14px;font-weight:500;color:var(--mut);text-decoration:none}
nav.main a.on{background:var(--sec);color:var(--fg)}
.hero{background:var(--tan);border-bottom:1px solid var(--bd);padding:40px 0}
.hero h1{margin:0;font-size:40px;line-height:1.1}
.hero p{margin:12px 0 0;max-width:640px;font-size:18px;color:#3d4659}
.tools{display:flex;gap:16px;flex-wrap:wrap;margin-top:14px;font-size:14px}
.filters{display:flex;gap:10px;flex-wrap:wrap;margin:24px 0 8px;align-items:end}
.filters label{display:flex;flex-direction:column;font-size:12px;color:var(--mut);font-weight:600;gap:3px}
.filters select{font:14px Inter,system-ui,sans-serif;padding:7px 10px;border:1px solid var(--bd);border-radius:6px;background:#fff;color:var(--fg)}
h2.sec{font-size:24px;margin:32px 0 12px}
.list{display:grid;gap:12px}
.card{border:1px solid var(--bd);background:var(--card);border-radius:10px;padding:16px 18px;display:block;text-decoration:none;color:inherit}
.card:hover{border-color:var(--primary)}
.card .meta{font-size:13px;color:var(--mut);display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.card h3{margin:4px 0 6px;font-size:19px;color:var(--primary)}
.card p{margin:8px 0 0;font-size:14.5px}
.chip{display:inline-block;font-size:12px;padding:2px 8px;border-radius:999px;border:1px solid var(--bd);background:#fff;margin:2px 4px 2px 0;white-space:nowrap}
.chip.open{border-color:#a9d3bc;background:#edf7f1;color:#205a3d}
.chip.closed{border-color:#e4cfa8;background:#fbf3e3;color:#6e4510}
.tag{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;padding:2px 7px;border-radius:4px;background:var(--sec);color:#3d4659}
.tag.bm{background:#dfe6f7;color:#202f61}
.legend{font-size:13px;color:var(--mut);margin:6px 0 0}
.models{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}
.models div{border:1px solid var(--bd);border-radius:8px;padding:10px 14px;background:#fff;font-size:14px}
.models b{display:block;margin-bottom:3px}
.models a{display:inline-block;margin-right:8px;font-size:13px}
footer{border-top:1px solid var(--bd);margin-top:48px;padding:24px 0;font-size:14px;color:var(--mut)}
.note{border-left:4px solid var(--acc);background:#fff;padding:10px 14px;margin:20px 0;font-size:14px}
table{border-collapse:collapse;width:100%;font-size:14px;background:#fff}
th,td{border:1px solid var(--bd);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--card)}
.tw{overflow-x:auto}
.entry{max-width:760px}
.entry h1{font-size:34px;line-height:1.15;margin:8px 0}
.entry h2{font-size:22px;margin:30px 0 8px}
.facts{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;font-size:14px;margin:12px 0}
.facts dt{color:var(--mut);font-weight:600}.facts dd{margin:0}
.headline{background:var(--tan);border-radius:8px;padding:12px 16px;font-size:17px;margin:12px 0}
.pending{color:#8a5a1c;font-weight:600}
@media(max-width:640px){.hero h1{font-size:30px}.logo span{display:none}header.site .wrap{height:auto;padding:10px 16px;flex-wrap:wrap}.badge{font-size:11px}.facts{grid-template-columns:1fr}}
body{padding-top:0}.hero,.entrytop{padding-top:48px}
"""
def chip(m):
    n,o=m
    return f'<span class="chip {"open" if o else "closed"}" title="{"Open weights" if o else "Closed"}">{html.escape(n)} · {"open" if o else "closed"}</span>'
E=[ # id,date,iso,title,type,models,headline,link
("ocr","28 Oct 2026","2026-10-28","OCR comparison: Unlimited-OCR 2, Docling and MinerU on academic PDFs","OCR",[("Unlimited-OCR 2",1),("Docling 2.93",1),("MinerU 3.1.9",1)],"On a DGX Spark, Docling converted 10 papers in 3.5 min, Unlimited-OCR 2 in 31 min and MinerU in 62 min, with no accuracy gain for the slower tools.",1),
("cu","27 Oct 2026","2026-10-27","Computer use: Claude Haiku 5.5, GPT-6.1 Terra and GPT-6 Luna","Computer use",[("Claude Haiku 5.5",0),("GPT-6.1 Terra",0),("GPT-6 Luna",0)],"On a web-page check Haiku scored 0.95 in 23 s; Luna and Terra scored 0.9 in 44 s and 47 s. On a desktop-app check all three scored 1.0 (3 runs each).",0),
("small","25 Oct 2026","2026-10-25","Eight small local models on transcript-cataloguing tasks","Local models",[("Gemma 4 31B",1),("Gemma 4 12B",1),("Gemma 4 E4B",1),("Qwen 3.5 4B / 9B",1),("LFM 2.5 8B",1),("Ministral 3 8B",1),("Granite 4.2 8B",1)],"Gemma 4 31B and 12B passed 5 of 6 checks; LFM 2.5 passed 0 of 6. Median speed ranged from 10 to 154 tokens per second.",0),
("full","25 Oct 2026","2026-10-25","A 17-hour local run: Gemma 4 31B over 508 documents","Local models",[("Gemma 4 31B",1)],"508 documents took about 17 h 19 min on a DGX Spark at a median of about 32 tokens per second, using 8.6 million input and 1.6 million generated tokens.",0),
("mtp","24 Oct 2026","2026-10-24","Draft-token setting and speed on Gemma 4 31B","Local models",[("Gemma 4 31B",1)],"With the draft-token setting at 0, 3 and 5, median speed was 10.6, 32.6 and 41.3 tokens per second; each setting passed 4 of 6 checks.",0),
("builder","16 Oct 2026","2026-10-16","Builder pilot: Opus 5.5 rebuilds five app tasks first built by Sonnet 5.5","Coding",[("Claude Opus 5.5",0),("Claude Sonnet 5.5",0),("GPT-6.1 Sol",0),("Muse Wonder Full 1.0",0)],"At list prices Opus cost $9.02 against $3.78 for Sonnet (2.4 times); blind review scores were close (3.30 and 3.40 against 3.27 and 3.23). One build per cell.",0),
("reason","3 Aug 2026","2026-08-03","Reasoning tokens used up an output cap","API behaviour",[("GPT-5.5 Pro",0)],"With max_output_tokens at 6,000, all 6,000 tokens went to reasoning and no text came back; an uncapped run took 542 s and 22,828 output tokens.",0),
("image","8 Mar 2026","2026-03-08","Local image generation on an M4 Max: FLUX Klein 4B and Qwen-Image","Image generation",[("FLUX.2 Klein 4B",1),("Qwen-Image 2512",1)],"At 1024 x 1024, FLUX Klein took about 18 s; Qwen-Image at 20 steps took about 8 minutes.",0),
]
BM=[ # benchmark items, link external
("2026-10-20","20 Oct 2026","Writing comparisons","Creative writing",[("Several models",0)],"Six writing experiments, 191 records; published without ranking."),
("2026-10-13","13 Oct 2026","Bicycle Test, October 2026","SVG drawing",[("Claude Haiku 5.5",0),("Claude Opus 5.5",0),("Claude Sonnet 5.5",0),("Muse Spark 1.3",0)],"Each model was asked to make an SVG of a bicycle; outputs shown side by side."),
("2026-09-04","4 Sep 2026","Bicycle Test, September 2026","SVG drawing",[("Claude Fable 5.1",0),("Gemini 3.8 Flash",0),("GPT-6 Astra",0),("GLM 5.3 Flash",0)],"Same prompt, five models; token counts and costs shown."),
("2026-07-12","12 Jul 2026","Bicycle Test, Google models","SVG drawing",[("Gemini 2.5 / 3.1 / 3.5",0)],"3 of 12 model and setting combinations never returned an SVG."),
("2026-06-04","4 Jun 2026","Gemma 4 video understanding","Local multimodal",[("Gemma 4 12B",1)],"A 26-second screencast, 26 frames; weak on absolute timestamps."),
]
def entry_card(e,badge=False):
    i,d,iso,t,ty,ms,h,_=e
    return f'''<a class="card" href="mockup-entry-page.html" data-type="{ty}" data-open="{ "open" if any(o for _,o in ms) else ""} {"closed" if any(not o for _,o in ms) else ""}" data-models="{html.escape("|".join(n for n,_ in ms))}" data-date="{iso}">
<div class="meta"><span>{d}</span><span class="tag">{ty}</span>{'<span class="tag" style="background:#e3efe8">Data point</span>' if badge else ''}</div>
<h3>{html.escape(t)}</h3><div>{"".join(chip(m) for m in ms)}</div><p>{html.escape(h)}</p></a>'''
def bm_card(b):
    iso,d,t,ty,ms,h=b
    return f'''<a class="card" href="#benchmarks-stays-on-existing-page" data-type="{ty}" data-open="{ "open" if any(o for _,o in ms) else ""} {"closed" if any(not o for _,o in ms) else ""}" data-models="{html.escape("|".join(n for n,_ in ms))}" data-date="{iso}">
<div class="meta"><span>{d}</span><span class="tag bm">Benchmark</span><span class="tag">{ty}</span></div>
<h3>{html.escape(t)}</h3><div>{"".join(chip(m) for m in ms)}</div><p>{html.escape(h)}</p><p style="font-size:13px;color:var(--mut)">Opens the existing reader on /benchmarks.</p></a>'''
def models_index(items):
    d={}
    for e in items:
        for n,o in e["models"]:
            d.setdefault(n,[o,[]])[1].append(e["title"])
    out=""
    for n in sorted(d):
        o,ts=d[n]
        out+=f'<div><b>{html.escape(n)} <span class="chip {"open" if o else "closed"}">{"open" if o else "closed"}</span></b>'+"".join(f'<a href="mockup-entry-page.html">{html.escape(t[:48])}{"…" if len(t)>48 else ""}</a><br>' for t in ts[:3])+'</div>'
    return out
items=[dict(title=e[3],models=e[5]) for e in E]
bitems=[dict(title=b[2],models=b[4]) for b in BM]
types=sorted({e[4] for e in E}|{b[3] for b in BM})
allm=sorted({n for e in E for n,_ in e[5]}|{n for b in BM for n,_ in b[4]})
FILTERS=lambda inc: f'''<div class="filters" id="filters">
<label>Task type<select id="f-type"><option value="">All</option>{"".join(f"<option>{t}</option>" for t in types)}</select></label>
<label>Model<select id="f-model"><option value="">All</option>{"".join(f"<option>{html.escape(m)}</option>" for m in allm)}</select></label>
<label>Open or closed<select id="f-open"><option value="">All</option><option value="open">Open weights</option><option value="closed">Closed</option></select></label>
<label>Date<select id="f-date"><option value="">Any time</option><option value="2026-10">October 2026</option><option value="2026-09">September 2026</option><option value="2026-0">Earlier in 2026</option></select></label>
</div><div class="legend" id="count"></div>'''
JS='''<script>
const cs=[...document.querySelectorAll('.list .card')];
function ap(){const t=f('f-type'),m=f('f-model'),o=f('f-open'),d=f('f-date');let n=0;
cs.forEach(c=>{let ok=(!t||c.dataset.type===t)&&(!m||c.dataset.models.split('|').includes(m))&&(!o||c.dataset.open.split(' ').includes(o))&&(!d||(d==='2026-0'?c.dataset.date<'2026-09':c.dataset.date.startsWith(d)));c.style.display=ok?'':'none';if(ok)n++});
document.getElementById('count').textContent=n+' of '+cs.length+' entries shown (newest first)'}
function f(i){return document.getElementById(i).value}
document.querySelectorAll('#filters select').forEach(s=>s.onchange=ap);ap();
</script>'''
def page(title,badge,body):
    return f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{CSS}</style></head><body><div class="badge">{badge}</div>{body}</body></html>'
GH="https://github.com/techczech/model-data-points"
# A
a=f'''<header class="site"><div class="wrap"><a class="logo" href="#"><b>MD</b><span>Model Data Points</span></a>
<nav class="main"><a class="on" href="#">Entries</a><a href="#models">Models tested</a><a href="#">About</a><a href="{GH}">GitHub</a><a href="#">Semantic Machines Benchmarks</a></nav></div></header>
<section class="hero"><div class="wrap"><h1>Model Data Points</h1>
<p>A data point is one small experiment on an AI model: what was tested, on which models, why, and what happened. They are not systematic benchmarks; read each one with its caveats.</p>
<div class="tools"><a href="{GH}">All entries as Markdown files on GitHub</a><a href="#">Semantic Machines Benchmarks (systematic comparisons) →</a></div></div></section>
<main class="wrap">{FILTERS(0)}
<div class="list">{"".join(entry_card(e) for e in E)}</div>
<h2 class="sec" id="models">Models tested</h2><p class="legend">Green is open weights, amber is closed. Each model lists its entries.</p>
<div class="models">{models_index(items)}</div>
<div class="note">Existing Benchmarks (drawing, writing, speech and video comparisons) stay on <a href="#">semanticmachines.fyi/benchmarks</a>.</div></main>
<footer><div class="wrap">Model Data Points · datapoints.semanticmachines.fyi · <a href="{GH}">Source repository</a> · <a href="#">Semantic Machines</a></div></footer>{JS}'''
open(D+"mockup-a-own-subsite-index.html","w").write(page("Model Data Points (Direction A)","A — own subsite",a))
# B
merged=sorted([(e[2],entry_card(e,True)) for e in E]+[(b[0],bm_card(b)) for b in BM],reverse=True)
nav="".join(f'<a href="#" class="{"on" if n=="Data points" else ""}">{n}</a>' for n in ["Explainers","Workshops","Activities","Evals","Benchmarks","Data points"])
b=f'''<header class="site"><div class="wrap"><a class="logo" href="#"><b>SM</b><span>SemanticMachines</span></a><nav class="main">{nav}</nav></div></header>
<section class="hero"><div class="wrap"><h1>Data points</h1>
<p>A data point is one small experiment on an AI model: what was tested, on which models, why, and what happened. Entries tagged Benchmark are the longer comparisons from the Benchmarks section, listed here so there is one place to browse.</p>
<div class="tools"><a href="{GH}">Entries as Markdown files on GitHub</a><a href="#">Benchmarks section →</a></div></div></section>
<main class="wrap">{FILTERS(1)}
<div class="list">{"".join(c for _,c in merged)}</div>
<h2 class="sec" id="models">Models tested</h2><p class="legend">Green is open weights, amber is closed.</p>
<div class="models">{models_index(items+bitems)}</div></main>
<footer><div class="wrap">semanticmachines.fyi/data-points · <a href="{GH}">Source repository</a></div></footer>{JS}'''
open(D+"mockup-b-section-in-semantic-machines-index.html","w").write(page("Data points (Direction B)","B — section in Semantic Machines",b))
# entry
en=f'''<header class="site"><div class="wrap"><a class="logo" href="mockup-a-own-subsite-index.html"><b>MD</b><span>Model Data Points</span></a>
<nav class="main"><a href="mockup-a-own-subsite-index.html">All entries (direction A)</a><a href="mockup-b-section-in-semantic-machines-index.html">All entries (direction B)</a></nav></div></header>
<main class="wrap entry" style="padding-top:40px">
<h1>OCR comparison: Unlimited-OCR 2, Docling and MinerU on academic PDFs</h1>
<dl class="facts"><dt>Date</dt><dd>28 October 2026</dd><dt>Task type</dt><dd>OCR, PDF to Markdown</dd><dt>Status</dt><dd>Complete</dd></dl>
<h2>Models tested</h2><div class="tw"><table><tr><th>Model or tool</th><th>Provider</th><th>Open?</th><th>How run</th></tr>
<tr><td>Unlimited-OCR 2 (about 3B parameters)</td><td>Baidu</td><td>Open weights, MIT licence</td><td>Local GPU, SGLang server</td></tr>
<tr><td>Unlimited-OCR 2, same weights</td><td>Baidu</td><td>Open weights, MIT licence</td><td>Local GPU, Hugging Face Transformers</td></tr>
<tr><td>Docling 2.93</td><td>Docling project</td><td>Open source</td><td>Local GPU, command line</td></tr>
<tr><td>MinerU 3.1.9</td><td>OpenDataLab</td><td>Open source</td><td>Local GPU, command line</td></tr></table></div>
<h2>Purpose</h2><p>To decide whether a new OCR model is worth adding to a PDF-to-Markdown workflow for academic papers, which already uses Docling by default and MinerU for maths-heavy papers.</p>
<h2>Context</h2><p>Ten academic papers, 174 pages: three two-column journal papers, two table-heavy papers, two maths-heavy papers, one scanned 1967 book chapter, one 66-page report and one Spanish-language paper. All runs were on an NVIDIA DGX Spark (GB10, 128 GB unified memory), one tool at a time. Unlimited-OCR 2 is a recent model from Baidu that reads page images directly.</p>
<h2>Method</h2><p>Each paper was converted to Markdown by each tool. Wall-clock time was recorded per paper. The Transformers route was started on the first papers and stopped when it proved too slow. Text was compared with the PDF's own text layer (word error rate), every number in each output was checked against the numbers in the text layer, and tables were counted. The scan was compared with OCRmyPDF output instead.</p>
<h2>Results</h2>
<div class="headline">Docling took 3.5 minutes for all 10 papers, Unlimited-OCR 2 on SGLang 31 minutes and MinerU 62 minutes, with no accuracy advantage for either slower tool on born-digital papers.</div>
<div class="tw"><table><tr><th>Setup</th><th>Total time (10 papers)</th><th>Time per page</th><th>Word error rate vs text layer</th><th>Numbers not in text layer</th><th>Tables emitted</th></tr>
<tr><td>Docling 2.93</td><td>3.5 min</td><td>about 1.2 s</td><td>21.9%</td><td>215</td><td>81</td></tr>
<tr><td>Unlimited-OCR 2, SGLang</td><td>30.9 min</td><td>about 10.7 s</td><td>22.7%</td><td>249</td><td>84</td></tr>
<tr><td>MinerU 3.1.9</td><td>61.7 min</td><td>about 21 s</td><td>27.4%</td><td>302</td><td>153</td></tr>
<tr><td>Unlimited-OCR 2, Transformers</td><td>4 papers only: 446–4,562 s each</td><td>not computed</td><td>not comparable</td><td>not comparable</td><td>not comparable</td></tr></table></div>
<p><b>Scanned chapter.</b> Against OCRmyPDF as baseline, Unlimited-OCR 2 (19.3%) and MinerU (17.6%) differed far less than Docling (37.5%).</p>
<h2>Caveats</h2><ul><li>One machine, one set of 10 papers, one run each (n=1).</li>
<li>The word error rate is dominated by reading order (headers, footnotes, figure text placed differently), so it shows the tools as roughly equal rather than measuring misread words.</li>
<li>Most numbers not found in the text layer are page numbers, table cells or formatting differences, not misreadings. One real misreading was found in Unlimited-OCR 2 output: a caption's 75% written as 55%.</li>
<li>One 66-page report accounts for most absent numbers in every tool (200 to 261).</li>
<li>SGLang times exclude about 1 min 45 s of server start-up; the server held about 61 GB of GPU memory.</li>
<li>Table layout quality was not judged by eye.</li></ul>
<h2>What this suggests</h2><p>For born-digital academic PDFs, Docling was about nine times faster than Unlimited-OCR 2 and as accurate on these measures, so the new model was not adopted. Unlimited-OCR 2 may be worth a look for scanned pages, and only through a serving engine such as SGLang: through Transformers it was 5 to 10 times slower again.</p>
<h2>Source</h2><p><a href="{GH}/blob/main/entries/2026-10-28-ocr-comparison.md">entries/2026-10-28-ocr-comparison.md</a> in the GitHub repository (Markdown with YAML frontmatter).</p>
</main><footer><div class="wrap">Used by both directions: datapoints.semanticmachines.fyi/ocr-comparison and semanticmachines.fyi/data-points/ocr-comparison.</div></footer>'''
open(D+"mockup-entry-page.html","w").write(page("OCR comparison (entry page)","A and B — entry page",en))
