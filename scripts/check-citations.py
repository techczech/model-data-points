"""Check built citation metadata. Usage: python3 check-citations.py OUTPUT_DIRECTORY."""
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
import sys

class Head(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = defaultdict(list)
        self.canonical = []
        self.coins = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            self.meta[(a.get("name") or a.get("property") or "").lower()].append(a.get("content", ""))
        if tag == "link" and "canonical" in a.get("rel", "").split():
            self.canonical.append(a.get("href", ""))
        if "Z3988" in a.get("class", "").split():
            self.coins = True

errors = []
files = sorted(Path(sys.argv[1]).rglob("*.html"))
assert files, "No built HTML pages"
for path in files:
    h = Head()
    h.feed(path.read_text(encoding="utf-8"))
    m = h.meta
    for key in ("citation_title", "citation_public_url", "citation_language", "dc.type", "dc.title", "dc.publisher", "dc.language", "og:site_name", "og:title", "og:url", "description"):
        if len(m[key]) != 1 or not m[key][0]:
            errors.append(f"{path}: expected one nonempty {key}, got {m[key]}")
    if not m["citation_author"] or any("," not in a for a in m["citation_author"]):
        errors.append(f"{path}: missing surname-first authors")
    if m["dc.creator"] != m["citation_author"]:
        errors.append(f"{path}: author mismatch")
    if m["dc.type"] != ["webpage"]:
        errors.append(f"{path}: expected webpage")
    if h.canonical != m["citation_public_url"] or h.canonical != m["og:url"] or not all(u.startswith("https://") for u in h.canonical):
        errors.append(f"{path}: canonical/citation/OG URL mismatch")
    if m["citation_title"] != m["dc.title"] or m["citation_title"] != m["og:title"]:
        errors.append(f"{path}: title mismatch")
    if m["dc.publisher"] != m["og:site_name"]:
        errors.append(f"{path}: site name mismatch")
    if h.coins or m["citation_journal_title"]:
        errors.append(f"{path}: COinS or journal metadata")
    dates = m["citation_publication_date"]
    if len(dates) > 1 or [d.replace("/", "-") for d in dates] != m["dc.date"]:
        errors.append(f"{path}: publication date mismatch")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"Citation checks passed: {len(files)} HTML pages")
