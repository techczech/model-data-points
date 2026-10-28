# Entry file format

One Markdown file per data point in `entries/`, named `YYYY-MM-DD-short-slug.md`. YAML frontmatter holds the structured fields; the body holds the prose sections shown on the entry page.

## Frontmatter fields

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Same as the file name without `.md`. |
| `title` | string | Plain description of what was tested. |
| `date` | date | When the test was run (end date if it spanned days). |
| `task_type` | string | One of: ocr, computer-use, local-models, coding, api-behaviour, image-generation, speech, other. |
| `models` | list | One item per model or tool tested (below). |
| `models[].name` | string | Name as the provider writes it. |
| `models[].provider` | string | Company or project. |
| `models[].open_weights` | true or false | Whether the weights can be downloaded. |
| `models[].access` | api, local or cli | How it was run. |
| `models[].version` | string | Version, revision or size, where known. |
| `purpose` | string | Why it was tested. |
| `context` | string | Hardware, data and anything else a reader needs to judge the result. |
| `method` | string | Short account of what was done. |
| `headline` | string | One sentence with the main result. |
| `results` | table | `columns` (list) and `rows` (list of lists); the page renders it as a table. Use `pending` for missing values. |
| `caveats` | list of strings | Limits of the test (n=1, shared machine, and so on). |
| `suggests` | string | One or two factual sentences on what this means for choosing a model. |
| `status` | complete or partial | Partial means some planned results are missing. |
| `sources` | list | Public links or file names of the raw data kept in the repository. No private paths. |

Publication rules: no private content, personal names, machine names, file paths or plan prices. Numbers only where text would expose private material.

## Example

```markdown
---
id: 2026-10-28-ocr-comparison
title: "OCR comparison: Unlimited-OCR 2, Docling and MinerU on academic PDFs"
date: 2026-10-28
task_type: ocr
models:
  - name: Unlimited-OCR 2
    provider: Baidu
    open_weights: true
    access: local
    version: "about 3B parameters, MIT licence, served with SGLang"
  - name: Unlimited-OCR 2
    provider: Baidu
    open_weights: true
    access: local
    version: "same weights, Hugging Face Transformers"
  - name: Docling
    provider: Docling project
    open_weights: true
    access: cli
    version: "2.93"
  - name: MinerU
    provider: OpenDataLab
    open_weights: true
    access: cli
    version: "3.1.9"
purpose: >-
  Decide whether a new OCR model is worth using for converting academic PDFs
  to Markdown, and how fast it is compared with tools already in use.
context: >-
  10 academic papers, 174 pages, one of them a scan. All runs on an NVIDIA
  DGX Spark (GB10, 128 GB unified memory), one after another.
method: >-
  Each paper was converted to Markdown by each tool and wall-clock time was
  recorded per paper. The Transformers route was stopped after 4 papers.
  Accuracy was spot-checked by reading output against the PDF.
headline: >-
  Docling took about 1.2 s per page; Unlimited-OCR 2 on SGLang about 10.7 s
  per page; the same model on Transformers took 446 to 4,562 s per paper.
results:
  columns: [Setup, Papers run, Time per paper, Time per page, Completed]
  rows:
    - [Unlimited-OCR 2 (SGLang), 10, 61-453 s, "4.7-21.4 s (about 10.7 overall)", 10 of 10]
    - [Unlimited-OCR 2 (Transformers), "4 (stopped)", 446-4,562 s, not computed, stopped as too slow]
    - [Docling 2.93, 10, 10-57 s, about 1.2 s overall, 10 of 10]
    - [MinerU 3.1.9, 10, pending, pending, re-run pending]
caveats:
  - One machine, one set of 10 papers, one run each (n=1).
  - The first MinerU run ran out of GPU memory because another model server held it; re-run pending.
  - An early Transformers versus SGLang timing shared the machine with other tools and is not used.
  - Transformers timings include first-use setup.
  - Accuracy spot check found one caption number misread by the SGLang run (75% as 55%); full scoring pending.
suggests: >-
  On this hardware Docling was about nine times faster per page than
  Unlimited-OCR 2 on SGLang, and serving through SGLang was far faster than
  Transformers. Accuracy scoring is needed before choosing between them.
status: partial
sources:
  - data/2026-10-28-ocr-comparison-timings.csv
---

## Purpose
(Optional prose; the page renders the frontmatter fields, and any body text
appears under "More detail".)
```
