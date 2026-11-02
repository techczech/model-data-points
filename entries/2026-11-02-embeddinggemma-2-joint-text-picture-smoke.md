---
id: 2026-11-02-embeddinggemma-2-joint-text-picture-smoke
title: "EmbeddingGemma 2 finding text and pictures in one space: a seven-query smoke test"
date: 2026-11-02
task_type: local-models
models:
  - name: EmbeddingGemma 2
    provider: Google
    open_weights: true
    access: local
    version: "Revision 914f7f89, 768 dimensions, sentence-transformers on MPS, float32"
purpose: >-
  Check that one local model places words and pictures in a shared space well
  enough for a single search over mixed items, before relying on it in a desktop app.
context: >-
  Apple M4 Max laptop, 128 GiB unified memory. Six made-up items in one index:
  three drawn pictures of a coloured shape on white, and three one-sentence
  texts with a title.
method: >-
  Pinned revision downloaded, then all items embedded through the app's own
  local call, batch size 8. Seven written queries used the SearchQuery prompt.
  Ranking by cosine similarity over all six items. No tuning; each query run once.
headline: >-
  All seven queries put the right item first, four of them searching words for
  a picture, with top scores of 0.74 to 0.80 against 0.55 to 0.64 for the runner-up.
results:
  columns: [Query, Right item, Top score, Runner-up score]
  rows:
    - ["a red circle", "picture", "0.764", "0.621"]
    - ["a blue square", "picture", "0.782", "0.629"]
    - ["a green triangle", "picture", "0.791", "0.609"]
    - ["something round and red", "picture", "0.735", "0.592"]
    - ["boats coming back to port", "text", "0.760", "0.598"]
    - ["money approved by a committee", "text", "0.756", "0.554"]
    - ["someone who looks after a lighthouse", "text", "0.796", "0.641"]
caveats:
  - Six items and seven queries, each once; a smoke test, not a retrieval benchmark.
  - The pictures are plain drawn shapes, far simpler than photographs or scans.
  - Query wording was written by the tester knowing the items.
  - Embedding the six items took 50.4 s including model load; the seven queries took 0.2 s. Neither is a speed measure.
  - Download took 271 s and is not a model property.
suggests: >-
  Enough to build on for a shared text and picture index on one Mac. It says
  nothing yet about quality on real archives, which needs its own test.
status: complete
sources: []
---

The model loaded through a pinned local snapshot with no remote code. Scores for text and pictures were close enough to compare in one list on this small set. That may not hold on a real collection, so a real search also ranks text and picture matches separately and combines the ranks.
