# AGENTS.md (model-data-points)

- Register: FOR AGENTS. Public repo: nothing private, ever.
- What: one MD file per experiment in `entries/` -> static site in `site/` via `uv run scripts/build-site.py`. Live: datapoints.semanticmachines.fyi.

## When to add an entry (standing, Dominik 2026-10-28)

- Every small experiment with AI models, in any session: speed, quality, cost, behaviour, a model or tool comparison, a computer-use or subagent trial, open or closed models. Not only small models.
- Add it once the result is in (n=1 is fine; say so in caveats). Partial results: `status: partial`, `pending` cells, update later.
- Standing approval: Dominik asked for all such experiments to be published. Write, check, commit, push, deploy without asking; name the new entry and its URL in the reply.

## How

1. Format: `design/entry-format.md`; copy the shape of an existing entry. File `entries/YYYY-MM-DD-short-slug.md`, `id` = file name.
2. Facts only from the run's own records; every number traceable. Raw data worth keeping: `data/<id>-*.csv` (no private content), listed in `sources`.
3. Privacy check before commit: no personal names, machine nicknames/hostnames, file paths, account or plan details, private document titles or content, unreleased private app names. Hardware type and public list prices are fine. Private corpora: generic description plus numbers.
4. Wording: "small experiments with AI models", never "small models".
5. `uv run scripts/build-site.py` (validates fields, id, private paths, script URLs, row widths). Commit, push, `scripts/deploy.sh` (needs `CLOUDFLARE_ACCOUNT_ID=b6ae5bced06492ee6f0c8f92776804da` if several accounts). Check the entry URL returns 200.
6. Prose: short and literal; `dominik-writer` for longer write-ups.

## Notes

- Slug = id minus date; keep stable (URLs).
- `site/` git-ignored. Licence: content CC BY 4.0, code MIT.
