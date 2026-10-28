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

Needs [uv](https://docs.astral.sh/uv/) (installs PyYAML and Markdown on the fly):

```sh
uv run scripts/build-site.py
```

This writes the static site to `site/` (git-ignored): the index with filters and a "Models tested" list, one page per entry at `/<slug>/` (the id without its date), and `/about/`. Preview with `python3 -m http.server -d site`.

## Deploy

`scripts/deploy.sh` builds and publishes `site/` to the Cloudflare Pages project `model-data-points` with wrangler.

## Licence

Content (entries, data, site text): CC BY 4.0. Code (`scripts/`, `design/source/`): MIT. See [LICENSE](LICENSE).
