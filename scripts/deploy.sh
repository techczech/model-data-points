#!/usr/bin/env bash
# Build and deploy site/ to the Cloudflare Pages project model-data-points.
# One-off setup (project, custom domain, DNS) is documented in README/handoff; this only deploys.
set -euo pipefail
cd "$(dirname "$0")/.."
uv run scripts/build-site.py
npx wrangler pages deploy site --project-name model-data-points --branch main \
  --commit-hash "$(git rev-parse HEAD)" --commit-message "$(git log -1 --format=%s)"
