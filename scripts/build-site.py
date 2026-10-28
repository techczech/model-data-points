#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml", "markdown"]
# ///
"""Build site/ from entries/*.md. Run: uv run scripts/build-site.py"""
import re
import shutil
import sys
from datetime import date
from html import escape
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
GITHUB = "https://github.com/techczech/model-data-points"
BENCHMARKS = "https://semanticmachines.fyi/benchmarks"
SM_HOME = "https://semanticmachines.fyi"

TASK_TYPES = {
    "ocr": "OCR", "computer-use": "Computer use", "local-models": "Local models",
    "coding": "Coding", "api-behaviour": "API behaviour",
    "image-generation": "Image generation", "speech": "Speech", "other": "Other",
}
ACCESS = {"api": "API", "local": "Local", "cli": "Command line"}
REQUIRED = ["id", "title", "date", "task_type", "models", "purpose", "context", "method",
            "headline", "results", "caveats", "suggests", "status", "sources"]
# Private paths must never ship: checked on the raw text of every entry.
PRIVATE_PATH = re.compile(r"/Users/|~/|/home/|[A-Za-z]:\\\\")
# optional entries-directory override for trial builds
ENTRIES = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "entries"
ID_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")


def parse(path):
    text = path.read_text(encoding="utf-8")
    errors = []
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, [f"{path.name}: no YAML frontmatter"]
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return None, [f"{path.name}: invalid YAML ({e})"]
    if not isinstance(fm, dict):
        return None, [f"{path.name}: frontmatter is not a mapping"]
    for k in REQUIRED:
        if k not in fm or fm[k] in (None, ""):
            if not (k in ("caveats", "sources") and fm.get(k) == []):
                errors.append(f"{path.name}: missing required field '{k}'")
    if errors:
        return None, errors
    if fm["id"] != path.stem:
        errors.append(f"{path.name}: id '{fm['id']}' does not match file name '{path.stem}'")
    if not ID_RE.match(str(fm["id"])):
        errors.append(f"{path.name}: id must look like YYYY-MM-DD-slug")
    if not isinstance(fm["date"], date):
        errors.append(f"{path.name}: date must be YYYY-MM-DD")
    if fm["task_type"] not in TASK_TYPES:
        errors.append(f"{path.name}: task_type '{fm['task_type']}' not one of {', '.join(TASK_TYPES)}")
    if fm["status"] not in ("complete", "partial"):
        errors.append(f"{path.name}: status must be complete or partial")
    if not isinstance(fm["models"], list) or not fm["models"]:
        errors.append(f"{path.name}: models must be a non-empty list")
    else:
        for i, mo in enumerate(fm["models"]):
            for k in ("name", "provider", "open_weights", "access"):
                if not isinstance(mo, dict) or k not in mo:
                    errors.append(f"{path.name}: models[{i}] missing '{k}'")
            if isinstance(mo, dict):
                if not isinstance(mo.get("open_weights"), bool):
                    errors.append(f"{path.name}: models[{i}].open_weights must be true or false")
                if mo.get("access") not in ACCESS:
                    errors.append(f"{path.name}: models[{i}].access must be api, local or cli")
    r = fm["results"]
    if not (isinstance(r, dict) and isinstance(r.get("columns"), list) and isinstance(r.get("rows"), list)):
        errors.append(f"{path.name}: results needs 'columns' and 'rows' lists")
    else:
        for i, row in enumerate(r["rows"]):
            if len(row) != len(r["columns"]):
                errors.append(f"{path.name}: results row {i + 1} has {len(row)} cells, expected {len(r['columns'])}")
    for k in ("caveats", "sources"):
        if not isinstance(fm[k], list):
            errors.append(f"{path.name}: {k} must be a list")
    for n, line in enumerate(text.splitlines(), 1):
        if re.search(r"(?i)javascript:|data:text/html", line):
            errors.append(f"{path.name}:{n}: script URL not allowed")
        if PRIVATE_PATH.search(line):
            errors.append(f"{path.name}:{n}: contains an absolute or home path (private paths cannot ship): {line.strip()[:80]}")
    for s in fm["sources"] if isinstance(fm["sources"], list) else []:
        s = str(s)
        if not s.startswith("http") and not (ROOT / s).exists():
            errors.append(f"{path.name}: source file '{s}' does not exist in the repository")
    fm["_body"] = m.group(2).strip()
    fm["slug"] = ID_RE.match(str(fm["id"])).group(2) if ID_RE.match(str(fm["id"])) else str(fm["id"])
    return fm, errors


def e(x):
    return escape(str(x), quote=True)


def cell(v):
    s = str(v)
    return '<span class="pending">pending</span>' if s.strip().lower() == "pending" else e(s)


def nice_date(d):
    return f"{d.day} {d.strftime('%b %Y')}"


def long_date(d):
    return f"{d.day} {d.strftime('%B %Y')}"


def paragraphs(s):
    return "".join(f"<p>{e(p.strip())}</p>" for p in re.split(r"\n\s*\n", str(s).strip()) if p.strip())


def page(title, body, desc, nav_on=""):
    def a(key, href, label):
        return f'<a{" class=on" if nav_on == key else ""} href="{href}">{label}</a>'
    nav = (a("entries", "/", "Entries") + a("models", "/#models", "Models tested") + a("about", "/about/", "About")
           + f'<a href="{GITHUB}">GitHub</a><a href="{BENCHMARKS}">Semantic Machines Benchmarks</a>')
    return f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="stylesheet" href="/style.css"></head><body><header class="site"><div class="wrap"><a class="logo" href="/"><b>MD</b><span>Model Data Points</span></a>
<nav class="main">{nav}</nav></div></header>
{body}
<footer><div class="wrap">Model Data Points · datapoints.semanticmachines.fyi · <a href="{GITHUB}">Source repository</a> · <a href="{SM_HOME}">Semantic Machines</a> · Text CC BY 4.0</div></footer></body></html>
"""


def chips(models):
    seen, out = set(), []
    for m in models:
        if m["name"] in seen:
            continue
        seen.add(m["name"])
        cls, lab = ("open", "open") if m["open_weights"] else ("closed", "closed")
        out.append(f'<span class="chip {cls}" title="{"Open weights" if m["open_weights"] else "Closed"}">{e(m["name"])} · {lab}</span>')
    return "".join(out)


def index_page(entries):
    types = sorted({TASK_TYPES[x["task_type"]] for x in entries})
    names = sorted({m["name"] for x in entries for m in x["models"]}, key=str.lower)
    years = sorted({str(x["date"].year) for x in entries}, reverse=True)
    opt = lambda vals: "".join(f"<option>{e(v)}</option>" for v in vals)
    cards = []
    for x in entries:
        opens = {"open" if m["open_weights"] else "closed" for m in x["models"]}
        cards.append(
            f'<a class="card" href="/{e(x["slug"])}/" data-type="{e(TASK_TYPES[x["task_type"]])}" '
            f'data-open="{" ".join(sorted(opens))}" data-models="{e("|".join(dict.fromkeys(m["name"] for m in x["models"])))}" '
            f'data-date="{x["date"].isoformat()}"><div class="meta"><span>{nice_date(x["date"])}</span>'
            f'<span class="tag">{e(TASK_TYPES[x["task_type"]])}</span>'
            f'{"<span class=tag>Partial</span>" if x["status"] == "partial" else ""}</div>'
            f'<h3>{e(x["title"])}</h3><div>{chips(x["models"])}</div><p>{e(x["headline"])}</p></a>')
    index = {}
    for x in entries:
        for m in x["models"]:
            d = index.setdefault(m["name"], {"open": m["open_weights"], "entries": {}})
            d["entries"][x["slug"]] = x["title"]
    mcards = []
    for name in names:
        d = index[name]
        cls, lab = ("open", "open") if d["open"] else ("closed", "closed")
        links = "".join(f'<a href="/{e(s)}/">{e(t if len(t) < 48 else t[:47] + "…")}</a><br>' for s, t in d["entries"].items())
        mcards.append(f'<div><b>{e(name)} <span class="chip {cls}">{lab}</span></b>{links}</div>')
    body = f"""<section class="hero"><div class="wrap"><h1>Model Data Points</h1>
<p>A data point is one small experiment with AI models: what was tested, on which models, why, and what happened. They are not systematic benchmarks; read each one with its caveats.</p>
<div class="tools"><a href="{GITHUB}">All entries as Markdown files on GitHub</a><a href="{BENCHMARKS}">Semantic Machines Benchmarks (systematic comparisons) →</a></div></div></section>
<main class="wrap"><div class="filters" id="filters">
<label>Task type<select id="f-type"><option value="">All</option>{opt(types)}</select></label>
<label>Model<select id="f-model"><option value="">All</option>{opt(names)}</select></label>
<label>Open or closed<select id="f-open"><option value="">All</option><option value="open">Open weights</option><option value="closed">Closed</option></select></label>
<label>Year<select id="f-year"><option value="">Any year</option>{opt(years)}</select></label>
</div><div class="legend" id="count"></div>
<div class="list">{"".join(cards)}</div>
<h2 class="sec" id="models">Models tested</h2><p class="legend">Green is open weights, amber is closed. Each model lists its entries.</p>
<div class="models">{"".join(mcards)}</div></main><script src="/filters.js"></script>"""
    return page("Model Data Points", body, "Small experiments with AI models: what was tested, on which models, why, and what happened.", "entries")


def source_link(s):
    s = str(s)
    href = s if s.startswith("http") else f"{GITHUB}/blob/main/{s}"
    return f'<li><a href="{e(href)}">{e(s)}</a></li>'


def entry_page(x):
    rows = "".join(
        f'<tr><td>{e(m["name"])}{" <span class=dim>(" + e(m["version"]) + ")</span>" if m.get("version") else ""}</td>'
        f'<td>{e(m["provider"])}</td><td>{"Open weights" if m["open_weights"] else "Closed"}</td><td>{ACCESS[m["access"]]}</td></tr>'
        for m in x["models"])
    r = x["results"]
    head = "".join(f"<th>{e(c)}</th>" for c in r["columns"])
    trs = "".join("<tr>" + "".join(f"<td>{cell(v)}</td>" for v in row) + "</tr>" for row in r["rows"])
    caveats = "".join(f"<li>{e(c)}</li>" for c in x["caveats"])
    more = ""
    if x["_body"]:
        more = '<h2>More detail</h2><div class="body-md">' + markdown.markdown(x["_body"].replace("&", "&amp;").replace("<", "&lt;"), extensions=["tables"]) + "</div>"
    body = f"""<main class="wrap entry" style="padding-top:40px">
<h1>{e(x["title"])}</h1>
<dl class="facts"><dt>Date</dt><dd>{long_date(x["date"])}</dd><dt>Task type</dt><dd>{e(TASK_TYPES[x["task_type"]])}</dd><dt>Status</dt><dd>{x["status"].capitalize()}</dd></dl>
<h2>Models tested</h2><div class="tw"><table><tr><th>Model or tool</th><th>Provider</th><th>Open?</th><th>How run</th></tr>{rows}</table></div>
<h2>Purpose</h2>{paragraphs(x["purpose"])}
<h2>Context</h2>{paragraphs(x["context"])}
<h2>Method</h2>{paragraphs(x["method"])}
<h2>Results</h2>
<div class="headline">{e(x["headline"])}</div>
<div class="tw"><table><tr>{head}</tr>{trs}</table></div>
<h2>Caveats</h2><ul>{caveats}</ul>
<h2>What this suggests</h2>{paragraphs(x["suggests"])}
{more}
<h2>Source</h2><p><a href="{GITHUB}/blob/main/entries/{e(x["id"])}.md">entries/{e(x["id"])}.md</a> in the GitHub repository (Markdown with YAML frontmatter).</p>
{"<ul>" + "".join(source_link(s) for s in x["sources"]) + "</ul>" if x["sources"] else ""}
</main>"""
    return page(f'{x["title"]} · Model Data Points', body, x["headline"])


ABOUT = f"""<main class="wrap entry" style="padding-top:40px"><h1>About Model Data Points</h1>
<p>A data point is one small experiment with AI models: what was tested, on which models, why, and what happened. Each one is a single Markdown file with structured fields, so the entries can be read, filtered and reused.</p>
<h2>What these are not</h2><p>They are not systematic benchmarks. Most are one run on one machine with a handful of tasks. Every entry lists its caveats; read them before drawing a conclusion. For systematic comparisons see <a href="{BENCHMARKS}">Semantic Machines Benchmarks</a>.</p>
<h2>Use and licence</h2><p>The text and data are published under CC BY 4.0; the build scripts are MIT. The entries, raw data files and build script are in the <a href="{GITHUB}">GitHub repository</a>.</p>
<h2>Author</h2><p>Dominik Lukeš, part of <a href="{SM_HOME}">Semantic Machines</a>.</p></main>"""


def main():
    entries, errors = [], []
    for p in sorted(ENTRIES.glob("*.md")):
        fm, errs = parse(p)
        errors += errs
        if fm:
            entries.append(fm)
    slugs = {}
    for x in entries:
        if x["slug"] in slugs:
            errors.append(f"duplicate slug '{x['slug']}' ({slugs[x['slug']]} and {x['id']})")
        slugs[x["slug"]] = x["id"]
        if x["slug"] in ("about", "style.css", "filters.js"):
            errors.append(f"{x['id']}: slug '{x['slug']}' is reserved")
    if errors:
        print("BUILD FAILED:\n  " + "\n  ".join(errors), file=sys.stderr)
        sys.exit(1)
    entries.sort(key=lambda x: (x["date"], x["id"]), reverse=True)
    out = ROOT / "site"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()
    for f in ("style.css", "filters.js"):
        shutil.copy(ROOT / "scripts/assets" / f, out / f)
    (out / "index.html").write_text(index_page(entries), encoding="utf-8")
    (out / "about").mkdir()
    (out / "about/index.html").write_text(page("About · Model Data Points", ABOUT, "About Model Data Points", "about"), encoding="utf-8")
    for x in entries:
        (out / x["slug"]).mkdir()
        (out / x["slug"] / "index.html").write_text(entry_page(x), encoding="utf-8")
    print(f"Built {len(entries)} entries into {out}")


if __name__ == "__main__":
    main()
