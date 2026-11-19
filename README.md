# Model Data Points

A public log of small experiments with AI models. Each data point records what was tested, on which models, why, and what happened. They are not systematic benchmarks; every entry lists its caveats. Published at https://datapoints.semanticmachines.fyi. For systematic comparisons see [Semantic Machines Benchmarks](https://semanticmachines.fyi/benchmarks).

## Entry format

One Markdown file per experiment in `entries/`, named `YYYY-MM-DD-short-slug.md`. YAML frontmatter holds the structured fields; any Markdown body appears on the page under "More detail". The full field list and an example are in [design/entry-format.md](design/entry-format.md).

Required fields: `id` (must equal the file name without `.md`), `title`, `date`, `task_type`, `models` (name, provider, open_weights, access, version), `purpose`, `context`, `method`, `headline`, `results` (`columns` and `rows`; use `pending` for missing values), `caveats`, `suggests`, `status` (`complete` or `partial`), `sources`.

Raw data referenced by `sources` goes in `data/`. Publication rules: no private content, personal names, machine names, file paths or plan prices.

## Add an entry

1. Copy an existing file in `entries/` and edit it.
2. Put any raw data in `data/` and list it under `sources`.
3. Run the build (below); it fails with a clear message if a field is missing, `id` does not match the file name, or the text contains a private path such as `/Users/` or `~/`.
4. Commit and push.

## Build

Needs [bun](https://bun.sh/). The Astro stack and lockfile follow Research Snacks.

```sh
bun install --frozen-lockfile
bun run build
```

This writes the static site to ignored `site/`: the entry index with task/model/open-or-closed/year filters and a Models tested list, one page per entry at `/<slug>/` (the ID without its date), and `/about/`. `bun run dev` serves local development; `bun run preview` serves a completed build. The old `uv run scripts/build-site.py` command remains a compatibility launcher.

```sh
bun run check
bun run check:release
```

The first command builds and checks types, frontmatter/privacy, citations, local links/anchors, RSS and usage-accounting. The second uses headless Chromium for JavaScript-off pages, keyboard dialogs, filters, reduced motion, 200% text, dark/forced colours, storage failure and copy feedback. It opens no visible browser window. See [migration parity and evidence](docs/parity-model-data-points-astro.md).

## Subscribe and reuse

[Subscribe (RSS)](https://datapoints.semanticmachines.fyi/rss.xml) for new data points. The feed includes each full headline summary, title, experiment date, permanent link and task/status categories. Every page links to the feed, its Markdown counterpart and citation metadata. Agents can start with `/llms.txt` or `/search-index.json`.

Source-listed CSV/SVG files are also served at `/data/<filename>`. GitHub source links stay unchanged. Entries remain single Markdown files with their original frontmatter; no Astro files need editing to add one.

## Usage pipeline

`python3 scripts/value-coding-agent-usage.py` regenerates the frozen coding-agent-token-usage entry, derived CSVs and chart from ranked, undated weekly CSVs, whole-window model/token totals and the pricing CSV. Build afterwards with `bun run build`. The collector's synthetic deduplication/home-boundary test and a byte-for-byte isolated valuation rerun are included in `bun run check`. The collector reads local logs; its JSON is saved under ignored `.local-usage/` and is not publication material. For fresh inputs, the valuation script accepts `--daily` plus explicit local coverage boundaries (see `--help`); no dates are frozen into the published pipeline. The build rejects dated usage data and per-day tables.

## Deploy

`scripts/deploy.sh --preview` checks and publishes a feature branch to the existing Cloudflare Pages project `model-data-points`. Verify parity on that preview, merge to main, then run `scripts/deploy.sh --production` from clean main. The default invocation still selects production. Set `CLOUDFLARE_ACCOUNT_ID=b6ae5bced06492ee6f0c8f92776804da` when several accounts are available. Existing account, custom domain and DNS attachment are retained.

After deployment, `python3 scripts/check-live.py [base-url]` curls every old public path plus canonical page aliases, feed, Markdown and agent routes; it requires HTTP 200 and matching build bytes. The shared kit's citation checker can also perform real Zotero saves when a translation-server is available.

## Licence

Content (entries, data, site text): CC BY 4.0. Code (`scripts/`, `design/source/`): MIT. See [LICENSE](LICENSE).
