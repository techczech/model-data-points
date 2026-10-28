---
id: 2026-10-25-small-local-models-cataloguing
title: "Eight small local models on transcript-cataloguing tasks"
date: 2026-10-25
task_type: local-models
models:
  - name: Gemma 4 31B
    provider: Google
    open_weights: true
    access: local
    version: "gemma4:31b, 20.39 GB package, Ollama 0.40.4"
  - name: Gemma 4 12B
    provider: Google
    open_weights: true
    access: local
    version: "gemma4:12b, 8.02 GB package"
  - name: Gemma 4 E4B
    provider: Google
    open_weights: true
    access: local
    version: "gemma4:e4b, 6.58 GB package"
  - name: Qwen 3.5 4B
    provider: Alibaba
    open_weights: true
    access: local
    version: "qwen3.5:4b, 3.32 GB package"
  - name: Qwen 3.5 9B
    provider: Alibaba
    open_weights: true
    access: local
    version: "qwen3.5:9b, 6.55 GB package"
  - name: LFM 2.5 8B
    provider: Liquid AI
    open_weights: true
    access: local
    version: "lfm2.5:8b, 5.16 GB package"
  - name: Ministral 3 8B
    provider: Mistral AI
    open_weights: true
    access: local
    version: "ministral-3:8b, 6.02 GB package"
  - name: Granite 4.2 8B
    provider: IBM
    open_weights: true
    access: local
    version: "granite4.2:8b, 5.35 GB package"
purpose: >-
  Find out whether a smaller model on a modest computer could do the
  discovery work (structured extraction from transcript excerpts) that a
  Gemma 4 31B baseline was already doing in a cataloguing workflow.
context: >-
  Six identical excerpts from radio programme transcripts, one bounded request
  per excerpt per model, 48 scored requests in total (60,255 input tokens and
  18,833 generated tokens). Run through Ollama 0.40.4 on an NVIDIA DGX Spark.
  Settings: 8K context, at most 1,200 generated tokens, temperature 0.1,
  seed 42, GPU offload, multi-token prediction (draft tokens) disabled, one
  warm-up request per model, no retries.
method: >-
  Each model answered the same six requests. Each answer was checked
  automatically for format and for whether quoted text appears in the source
  excerpt. Total time for the six requests and median generation speed were
  recorded.
headline: >-
  Gemma 4 31B and 12B passed 5 of 6 checks and LFM 2.5 8B passed 0 of 6;
  median generation speed ranged from 10.3 to 153.7 tokens per second.
results:
  columns: [Model, Package size (GB), Checks passed, Total time for 6 requests (s), Median generation speed (tokens/s)]
  rows:
    - [Gemma 4 31B, "20.39", 5 of 6, "224.4", "10.3"]
    - [Gemma 4 12B, "8.02", 5 of 6, "92.0", "26.1"]
    - [Gemma 4 E4B, "6.58", 4 of 6, "43.2", "56.5"]
    - [Qwen 3.5 4B, "3.32", 2 of 6, "36.4", "63.1"]
    - [Qwen 3.5 9B, "6.55", 1 of 6, "65.0", "37.5"]
    - [LFM 2.5 8B, "5.16", 0 of 6, "16.4", "153.7"]
    - [Ministral 3 8B, "6.02", 2 of 6, "69.4", "39.1"]
    - [Granite 4.2 8B, "5.35", 2 of 6, "81.7", "37.3"]
caveats:
  - One machine, six excerpts, one run per request (n=1); a feasibility screen, not a benchmark on unseen data.
  - The checks test format and whether quoted text is a substring of the source; they do not test whether a quote is attributed to the right speaker.
  - The 31B answers were used as the comparison but are not ground truth.
  - Tokenizers differ between model families, so tokens per second are not strictly comparable across families.
  - Multi-token prediction was off for every model, including the 31B. The same 31B model runs at about 32 tokens per second with it on, so its figure here is lower than in production use.
  - Figures from a DGX Spark say nothing about speed on other hardware.
  - LFM 2.5 8B produced invented song titles in its answers.
suggests: >-
  On this task only the two largest Gemma models passed 5 of 6 checks, and the
  fastest model passed none. Speed and checks passed did not move together
  across the eight models.
status: complete
sources: []
---
