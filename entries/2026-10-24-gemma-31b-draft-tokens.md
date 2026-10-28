---
id: 2026-10-24-gemma-31b-draft-tokens
title: "Draft-token setting and speed on Gemma 4 31B"
date: 2026-10-24
task_type: local-models
models:
  - name: Gemma 4 31B
    provider: Google
    open_weights: true
    access: local
    version: "gemma4:31b, quantised weights, through Ollama, with a draft component for multi-token prediction"
purpose: >-
  Measure how the number of draft tokens (multi-token prediction) changes
  generation speed for a local model used for batch text processing.
context: >-
  Gemma 4 31B served through Ollama on an NVIDIA DGX Spark. Three real inputs
  from a cataloguing task, each sent twice per setting. The run date is not
  recorded; the figures come from a report dated 24 October 2026.
method: >-
  The draft setting was set to 0, 3 and 5 in turn. Each of the three inputs
  was sent twice at each setting, with warm-up requests excluded. Median
  generation speed and median request time (excluding reported model load)
  were recorded, and the outputs were scored on 6 automated checks.
headline: >-
  With the draft-token setting at 0, 3 and 5, median speed was 10.6, 32.6 and
  41.3 tokens per second; each setting passed 4 of 6 checks.
results:
  columns: [Draft setting, Median generation speed (tokens/s), Median request time (s), Automated checks passed]
  rows:
    - ["0", "10.6", "28.73", 4 of 6]
    - ["3", "32.6", "10.23", 4 of 6]
    - ["5", "41.3", "8.46", 4 of 6]
caveats:
  - Three inputs, two requests each, one machine; a small workload.
  - No quality difference between the settings was established; all three passed the same 4 of 6 checks.
  - The exact run date is not recorded.
suggests: >-
  Turning draft tokens on roughly tripled generation speed on this model and
  workload, and 5 was faster than 3. The checks did not show a quality
  difference between the settings.
status: complete
sources: []
---
