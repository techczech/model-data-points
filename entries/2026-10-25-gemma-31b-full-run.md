---
id: 2026-10-25-gemma-31b-full-run
title: "A 17-hour local run: Gemma 4 31B over 508 documents"
date: 2026-10-25
task_type: local-models
models:
  - name: Gemma 4 31B
    provider: Google
    open_weights: true
    access: local
    version: "gemma4:31b, 30.7B parameters, Q4_K_M quantisation, Ollama 0.40.4"
purpose: >-
  Process a full archive of radio programme transcripts (20,389 minutes of
  audio, already transcribed) with a local model, and record how long it takes
  and how many tokens it uses.
context: >-
  508 transcript documents split into 1,136 chunks, processed on an NVIDIA
  DGX Spark through Ollama. Settings: context 24,576 tokens, at most 4,096
  generated tokens, temperature 0.1, seed 42, multi-token prediction with 3
  draft tokens. The model worked in three stages on each document.
method: >-
  The three stages ran in sequence over the whole set. Request and token
  counts were taken from the saved responses, including corrective attempts.
  An earlier run over 190 of the documents is recorded for comparison.
headline: >-
  508 documents took about 17 h 19 min on a DGX Spark at a median of about
  32 tokens per second, using 8,571,832 input tokens and 1,589,326 generated
  tokens.
results:
  columns: [Stage, Requests (attempts), Input tokens, Generated tokens, Median generation speed (tokens/s)]
  rows:
    - [Stage 1, "1,136 (1,255)", "6,393,910", "1,208,714", "31.75"]
    - [Stage 2, "247 (280)", "1,439,660", "307,560", "33.26"]
    - [Stage 3, "479 (480)", "738,262", "73,052", "32.11"]
    - [Total, "1,862 (2,015)", "8,571,832", "1,589,326", "about 32"]
caveats:
  - One run on one machine (n=1).
  - Counts come from saved responses and include corrective attempts; no meter recorded energy use, peak memory or staff time.
  - The quality of the output was not independently audited.
  - Of the 508 documents, 470 produced drafts and 38 only partial output.
  - The earlier 190-document run took about 8.5 hours, with about 5.19 million prompt tokens and 681,000 generated tokens at about 31 tokens per second.
suggests: >-
  A 30.7B model quantised to Q4_K_M on one DGX Spark sustained about 32 tokens
  per second for 17 hours, so a job of about 10 million tokens took most of a
  day. Speed was steady across the three stages.
status: complete
sources: []
---
