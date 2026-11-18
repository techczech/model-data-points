#!/usr/bin/env bash
# Build, check and deploy the static Astro output to Cloudflare Pages.
# Set CLOUDFLARE_ACCOUNT_ID when several accounts are available.
set -euo pipefail
cd "$(dirname "$0")/.."
mode="${1:---production}"
branch="$(git branch --show-current)"
case "$mode" in
  --preview)
    if [[ "$branch" == main || -z "$branch" ]]; then
      echo 'Preview deployment needs a named feature branch.' >&2; exit 1
    fi ;;
  --production)
    if [[ "$branch" != main ]]; then
      echo 'Production deployment must be built from main.' >&2; exit 1
    fi
    if [[ -n "$(git status --porcelain --untracked-files=normal)" ]]; then
      echo 'Commit the reviewed changes before production deployment.' >&2; exit 1
    fi ;;
  *) echo 'Usage: scripts/deploy.sh [--preview|--production]' >&2; exit 1 ;;
esac
bun run check
wrangler pages deploy site --project-name model-data-points --branch "$branch" \
  --commit-hash "$(git rev-parse HEAD)" --commit-message "$(git log -1 --format=%s)"
