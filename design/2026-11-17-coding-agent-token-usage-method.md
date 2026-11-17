---
title: Coding-agent usage reconstruction and publication method
date: 2026-11-17
register: FOR AGENTS
provenance: Retained local-log aggregates, frozen public provider prices and the approved publication privacy cut.
purpose: Explain the published usage accounting and its limits
reader: Readers checking the entry and maintainers rebuilding it
prior_knowledge: Coding agents and token billing
required_knowledge: Coverage windows, ranked weeks, cache accounting and private input boundaries
exclusions: Machine identities, session content and dates of activity
---

The entry describes one heavy user's recorded coding-agent usage across several machines. Its sequence is the three-week combined result, a longer Claude-only comparison, whole-window model and token-type totals, then pricing and reconstruction. Token volume supports no conclusion about quality or productivity.

## Inputs and collection

The local snapshot contains earlier fragmentary retention and a partial week at collection. Unavailable sources are excluded. Local daily counts are collapsed by tool and exact logged model after discarding folder, origin and entrypoint labels. Reasoning is an informational subset of Codex output, never an extra billing category. No session content or account identifiers are publication inputs.

The generic collector reads personal tool homes, including archive-only homes, and excludes the enterprise home. Claude deduplication keeps the first record for each message/request pair in each home. Later streaming updates are not merged. Codex uses changed cumulative totals and deduplicates timestamp/cumulative/last-usage tuples across files within each home. Copies across homes or machines cannot be deduplicated from aggregate counts. Missing sources and these limits are not repaired by inference.

The collector writes only to ignored `.local-usage/` storage. Original collections, daily inputs, machine coverage and date-to-rank mappings must never be committed or served. The public repository contains the generic collection and valuation scripts so readers can inspect the method.

## Coverage and publication

The headline window contains **three consecutive full weeks** with retained records for both tools. The secondary window contains **eight full weeks** of Claude Code records. These windows were selected from retention evidence, not by token volume. Claude's earlier default log cleanup left fragmentary records before retention increased; Codex retention begins later despite earlier use. The first partial Codex week and the partial week at collection are excluded. Earlier fragmentary weeks do not count as zero activity.

Weekly aggregation uses Monday boundaries on recorded timestamp dates without local-time conversion. Publication removes those dates and independently sorts each window by priced value, descending. Labels **Week 1, Week 2, ...** are ranks within a window; they carry no chronological order or shared cross-window identity. The chart has separate panels and no date axis. The Claude-only panel and CSV rows contain only Claude counts and values.

Whole-window CSVs retain the headline and all-retained tool/model/token-type totals. The all-retained grand total is secondary and includes fragmentary periods and the partial week at collection. A separate window-totals CSV preserves the exact Decimal sums: summing the older model CSV's six-decimal display values would otherwise introduce rounding drift. The weekly CSV publishes only the selected full windows. Daily, machine-coverage and weekly-by-model tables are not public outputs.

## Valuation

Rates are frozen standard short-context list prices in USD per million tokens, checked on **17 November 2026**, with provider URLs in the price CSV. Claude categories are uncached input, output, cache reads, five-minute writes and one-hour writes. Codex categories are uncached input, output, cached input and writes; no Codex writes were recorded. Five-minute Claude writes cost 1.25 times input and one-hour writes cost twice input; missing retention splits are assigned to five-minute writes.

The verified Fable 5.1 cache-read rate is $0.25/M, with the original $1 alternative retained as a labelled sensitivity calculation. No price is inferred for `codex-auto-review`; unknown rates and values are blank, with separate unpriced-token counts. Cache share is the priced value of cached categories divided by total priced value, not money saved.

Per-request context length and processing tier are absent from the aggregates. Long-context surcharges, fast/ultrafast premiums, regional adjustments and tool charges are excluded. Haiku 5.5 uses the base rate up to 100,000 input tokens. List-price equivalents are not historical bills or subscription savings.

## Rebuild and validation

Run `python3 scripts/value-coding-agent-usage.py` to rebuild the entry and SVG from public ranked weeks and whole-window totals. Run `bun run check` for the full build and accounting suite. The isolated public rerun requires no private daily data and reproduces the published files byte-for-byte.

For a fresh local collection, use the collector's ignored output and prepare the daily CSV locally with fields `tool`, `date`, `model`, `uncached_input`, `output`, `cache_read`, `cache_write_5m_or_codex_write`, `cache_write_1h` and `reasoning_included_in_output`. Run the valuation script with `--daily` and all five local coverage boundaries shown by `--help`. Daily inputs cannot be read from public `data/`; the command writes only ranked weeks and whole-window public totals. Local dates are arguments, never frozen source constants.

Before publication, reconcile token counts, exact Decimal priced sums, unpriced counts, weekly means/medians, model totals and cached share. The original figures remain: $11,684.414954230 headline value; $4,340.046136090 weekly median; $3,894.804984743... weekly mean; $3,053.0261492725 Claude-only median; $8,774.887849730 cached value (75.099077567...%); 44,195,194,919 headline tokens, including 4,432,888,344 unpriced tokens. Price and all-retained model/token CSVs remain byte-identical. Headline model/token rows retain every original number with date columns removed.

The build scans every usage file under public `data/`, including files not listed as sources. It rejects daily/coverage/weekly-model files, per-day tables and ISO dates outside the price-check column. Synthetic tests retain collector deduplication, reasoning-subset and excluded-home checks; public and local valuation paths are checked independently. A successful reconstruction does not prove completeness of the original logs.
