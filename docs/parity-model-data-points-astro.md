---
title: Model Data Points Astro migration parity inventory
date: 2026-11-18
source: scripts/build-site.py and check scripts at 27f21f9
purpose: Verify the approved framework migration without changing experiment records
reader: Maintainers assessing the release or resuming its checks
prior_knowledge: Existing single-file entry and anonymous usage-data workflow
required_knowledge: Preserved behaviour, additions, verification and deployment evidence
exclusions: No new model measurements or research interpretation
---

# Existing behaviour and verification

The baseline is commit `27f21f9`, built before implementation into ignored `.check/old-site/`. All 14 `entries/*.md`, all data, the usage collector and the valuation script remain unchanged. The migration follows the Research Snacks Astro implementation, including its exact dependency versions and copy-in kit. Authoring remains one Markdown file with its current YAML frontmatter; the canonical command changes to `bun run build`.

| Existing contract | Verification | Result |
|---|---|---|
| YAML frontmatter mapping; all 15 required fields; optional Markdown body | Actual entries and negative fixtures for missing fields/malformed YAML | PASS |
| ID equals filename, date-prefixed ID, valid date, date-free stable slug | Loader fixtures, old/new URL manifest, every entry link | PASS |
| Task types, complete/partial status, nonempty model list, required model keys, boolean open_weights, API/local/CLI access | Negative fixtures; existing records render | PASS |
| Results columns/rows lists, equal row widths; caveats and sources lists, including empty lists | Negative fixtures and full rendered-table comparisons | PASS |
| Raw-entry rejection of private paths and script URLs, source-file existence | Private-path/script/source fixtures; build scans all entries and published CSVs | PASS |
| Duplicate/reserved slugs rejected before output is touched; optional trial entries directory | Loader fixtures; `MDP_ENTRIES_DIR` and Python compatibility launcher | PASS |
| Descending date then ID ordering; short/long British dates | Whole card/model-list and entry-facts comparison | PASS |
| Unique model chips with open/closed labels, task/partial tags, complete headline | Entire index list DOM text equality | PASS |
| Four filters: task, model, open/closed and year; model index with linked truncated titles | Whole model-index comparison; headless control/results checks | PASS; query search, URL state and Back restoration added |
| Entry title/date/task/status; model names/version/provider/open/access; purpose/context/method/results/caveats/suggestion/source | Every entry's full main text and every table compared with baseline | PASS |
| Paragraph splitting, escaped field text, pending cell styling, Markdown body/tables/code/images; raw HTML escaped | Renderer fixtures, DOM equality and local image loading | PASS |
| Legacy YAML scalar rendering, including `1.0` and one mapping-valued caveat | Explicit fixture and every rendered page compared | PASS; source records unchanged |
| Source entry and source-file GitHub URLs; source-backed SVG copied locally | Full old-link comparison; SVG byte equality and loaded usage chart | PASS |
| Home/About text, navigation, Models tested anchor, Research Snacks/GitHub/Benchmarks/parent links and licence | DOM/link checks on all original routes | PASS |
| Element 16 citation/DC/OG metadata, canonical URL, surname-first author, undated home/About, dated entries, webpage type, no COinS/journal title | Existing Python checker on all 17 pages; shared checker and real Zotero save at release | Local PASS; deployed results recorded below |
| Visible page citation and copy feedback | Existing citation text plus headless Clipboard API, fallback and failure checks | PASS; home gains a visible citation too |
| Cream/navy/amber visual style, serif headings, responsive shell, constrained article column, scrollable tables | Old/new captures of all 16 original routes at 1280/390 pixels; direct sheet inspection | PASS; balanced headings and new contents/house controls are intentional additions |
| Usage collector deduplication and personal-home boundary | Original synthetic `test-usage-accounting.py` unchanged | PASS |
| Valuation output, disjoint token types, analysis windows, unpriced categories, generated Markdown/CSVs/SVG | Isolated standard-library valuation rerun; frozen entry, four CSVs and chart compare byte-for-byte | PASS |
| Old build invocation used by the frozen usage method | `scripts/build-site.py` delegates to Astro, including optional entries-dir argument | PASS; no content/generator edit needed |
| Pages project, account and attached domain | Existing project retained; deploy script uses preview branch or clean main; attach-domain.py unchanged | Preview/live evidence below |

The loader also rejects path traversal/non-file sources, unsafe route characters and collisions with new reserved routes. These checks constrain authoring errors without requiring any change to an existing record. Publication still requires the author's privacy review; pattern checks cannot determine whether narrative text reveals private context.

# File and URL parity

The old build has **20 files**, all retained, with **zero removals**. New output has **54 files**. The existing 16 HTML files and stylesheet change; `/copy.js`, `/filters.js` and the usage SVG remain byte-identical. All 14 source entries and every data file are unchanged.

There are **34 added files**: 17 Markdown counterparts (including the new search page), `/search/index.html`, `/search-index.json`, `/llms.txt`, `/rss.xml`, ten source-listed CSV downloads, `_headers`, and two hashed Astro bundles. Bundle names vary with source changes. `_headers` is new hosting configuration, not an old URL. Unlike Research Snacks, this baseline contains no `_headers`; all 20 old paths are public assets.

`docs/urls-model-data-points-baseline.txt` contains the complete baseline manifest. `bun scripts/check-parity.ts` compares all output paths, every original page's content/tables/links/citation metadata, the home cards/model list and unchanged assets. It requires the ignored old build. To reconstruct it later, run the original builder from commit `27f21f9` in a separate checkout, then place its output in `.check/old-site/`.

# Feed and agent layer

RSS 2.0 is `/rss.xml`: one item per entry, complete headline summary, title, original experiment date, canonical date-free link and GUID, task label and status categories. Every page has feed autodiscovery and a visible **Subscribe (RSS)** link. The validator checks well-formed XML, required channel/item fields, absolute links, unique GUIDs, UTC RFC 822 dates, ordering and exact summaries/categories/dates.

Every page has JSON-LD and a Markdown alternate. Entry Markdown copies are byte-identical to their canonical single files, retaining frontmatter and full body. Home/About/search copies, `/llms.txt` and `/search-index.json` provide agent discovery. Source-listed CSVs are also served locally at their existing repository-relative `/data/` paths; existing GitHub source links remain intact. Unsanitised collector output is never copied or published.

# Release checklist

| Required check | Result |
|---|---|
| `bun run check` | PASS: Astro build, TypeScript, six Bun tests/39 assertions, existing 17-page citation checker, built metadata/links/anchors/feed validator, original usage-accounting test |
| JavaScript off | PASS: home, About and every entry render; usage image loads; no new page overflow at desktop/phone widths; search has a static complete page list |
| Keyboard | PASS: native search/keys dialogs, Tab avoids background controls, Esc, focus return; off switch disables all single keys and Ctrl+K still works |
| Search/filter/list | PASS: grouped accent-folding search/combobox; five filters including original four; live count, no-results/clear and Back restoration |
| Reduced motion | PASS: automatic/instant scrolling and no dialog animation |
| 200% text | PASS: body doubles at desktop/phone widths on all 16 original routes, no horizontal page overflow; tables scroll locally |
| Dark/forced colours | PASS: captured and inspected; explicit light overrides dark system; open/closed badges retain text labels |
| Storage blocked | PASS: throwing localStorage leaves theme, page, off switch and Ctrl+K working |
| Kit drift | PASS: all ten TypeScript/CSS copies under src report same; existing Python citation kit unchanged |
| Citation copy | PASS: Clipboard API success, execCommand fallback, visible failure |
| Citation/Zotero | Local metadata PASS; deployed real-save results below |
| RSS | PASS: all 14 full headline summaries, dates, canonical URLs and task/status categories |

Elements 1–13 and 16 are adopted. The entry/About server-rendered contents disclosure has heading anchors, current-section enhancement and sticky positioning at wide widths. Elements 14 (archive) and 15 (book reader) are not applicable. Unchanged kit modules are copied locally; no shared package is introduced.

# Security and verification tools

The stack exactly follows Research Snacks: Astro 7.4.8, micromark 4.0.3, GFM 3.0.0, YAML 2.8.3, TypeScript 6.0.3, Playwright core 1.62.1 and the same overrides/lock resolution. The security harvest records zero critical/medium/low findings and two unpatched high picomatch build-time ReDoS advisories (2.3.2/4.0.7, GHSA-fc5q-39xc-vjpf), matching the reference site. Only static output is deployed; the package tree and a Node server are not published. These advisories remain recorded, not suppressed.

The headless release suite uses Playwright's headless shell, never the desktop Chrome application. It closes contexts and local servers. `scripts/make-comparisons.ts` produces four ignored old/new sheets covering all 16 original routes at both widths (page tops), plus a dark/forced-colours sheet. Raw full-page screenshots are removed at completion. Sheets are retained in `.check/comparisons/` for later inspection.

# Deployment evidence

Preview, live URL checks and real Zotero saves are recorded here after the approved release gates pass. Production deployment is allowed only from clean main; `scripts/attach-domain.py` remains unchanged because no DNS/domain change is needed.

## First deployed preview (18 November 2026)

Preview `https://e271f874.model-data-points.pages.dev`, implementation `5f59944`: complete headless suite PASS, all 16 original routes captured at desktop/phone widths, **70/70 curl checks** with exact built bytes, including **20/20 baseline public paths** and every new download/bundle. Four real Zotero saves PASS: home, About, usage entry and search each produce exactly one webpage, author `Lukeš, Dominik`, Website Title `Model Data Points`; the usage entry has `2026/11/17`, other pages are undated. The final preview adds the same contents disclosure to About and corrects the lockfile's project name; no experiment source or data changes.
