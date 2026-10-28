# AGENTS.md (model-data-points)

- Register: FOR AGENTS. Public repo: nothing private, ever.
- What: one MD file per experiment in `entries/` -> static site in `site/` via `uv run scripts/build-site.py`.
- Format: `design/entry-format.md`. Build validates fields, id = filename, no `/Users/` or `~/`.
- Entries: no personal names, machine names, paths, plan prices. Use `pending` for missing cells.
- Wording: "small experiments with AI models", never "small models".
- Slug = id minus date; keep stable (URLs).
- `site/` git-ignored. Deploy: `scripts/deploy.sh` (needs explicit go; see README).
- Licence: content CC BY 4.0, code MIT.
