# web-design-elements kit: citation.py v1
# Citable pages (element 16, references/citation.md), for static Python builders. Twin of citation.ts.
# One page dict gives the <head> tags Zotero, Mendeley and EndNote read, and the visible "Cite this page" block.
# No COinS: it outranks the page's own tags in Zotero.
#   citation_head(page) -> str for <head>;  cite_text(page) -> str;  cite_block(page) -> <section class="cite">
# page keys: title, url (canonical), site, authors [..], organisations [..]?, date "YYYY-MM-DD"|"YYYY"?,
#            description?, type webpage|blogPost|report|bookSection|book (default webpage), language (default en-GB),
#            institution (report), book_title (bookSection), isbn (book)
from html import escape


def surname_first(name):
    n = name.strip()
    if "," in n or " " not in n:
        return n
    given, surname = n.rsplit(" ", 1)
    return f"{surname}, {given}"


def _people(p):
    orgs = set(p.get("organisations") or [])
    return [a if a in orgs else surname_first(a) for a in p.get("authors") or []]


def citation_tags(p):
    lang = p.get("language") or "en-GB"
    typ = p.get("type") or "webpage"
    t = []

    def add(attr, key, value):
        if value:
            t.append((attr, key, str(value)))

    add("name", "citation_title", p["title"])
    for a in _people(p):
        add("name", "citation_author", a)
    if p.get("date"):
        add("name", "citation_publication_date", str(p["date"]).replace("-", "/"))
    add("name", "citation_public_url", p["url"])
    add("name", "citation_language", lang.split("-")[0])
    if typ == "report":
        add("name", "citation_technical_report_institution", p.get("institution"))
    if typ == "bookSection":
        add("name", "citation_inbook_title", p.get("book_title"))
    if typ == "book":
        add("name", "citation_isbn", p.get("isbn"))
    add("name", "DC.type", typ)
    add("name", "DC.title", p["title"])
    for a in _people(p):
        add("name", "DC.creator", a)
    add("name", "DC.date", p.get("date"))
    add("name", "DC.publisher", p["site"])
    add("name", "DC.language", lang)
    add("property", "og:site_name", p["site"])
    add("property", "og:title", p["title"])
    add("property", "og:url", p["url"])
    return t


def citation_head(p):
    return "\n".join(f'<meta {a}="{k}" content="{escape(v)}">' for a, k, v in citation_tags(p))


def cite_text(p):
    names = _people(p)
    who = names[0] if len(names) == 1 else (", ".join(names[:-1]) + " and " + names[-1] if names else p["site"])
    year = str(p["date"])[:4] if p.get("date") else "n.d."
    title = p["title"] if p["title"][-1:] in ".?!" else p["title"] + "."
    return f'{who} ({year}). {title} {p["site"]}. {p["url"]}'


def cite_block(p):
    return ('<section class="cite" aria-labelledby="cite-h"><h2 id="cite-h">Cite this page</h2>'
            f'<p id="cite-text">{escape(cite_text(p))}</p>'
            '<button type="button" data-copy="#cite-text">Copy citation</button></section>')
