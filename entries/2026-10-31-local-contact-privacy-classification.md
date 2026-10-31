---
id: 2026-10-31-local-contact-privacy-classification
title: "Gemma 4 12B and Llama 4 Scout on 48 synthetic contact-privacy cases"
date: 2026-10-31
task_type: local-models
models:
  - name: Gemma 4 12B
    provider: Google
    open_weights: true
    access: local
    version: "Instruction model, QAT Q4_0 GGUF, llama.cpp runtime directory 2.59.0"
  - name: Llama 4 Scout
    provider: Meta
    open_weights: true
    access: local
    version: "17B-16E text, MLX 8-bit"
purpose: >-
  Test whether a local model can distinguish contacts requiring redaction from
  public generic contacts, placeholders and numbers that are not contact data.
context: >-
  Apple M3 Ultra desktop, 512 GiB unified memory, 32 CPU cores, shared workload.
  Forty-eight entirely synthetic labelled excerpts; twenty describe third-party contacts.
method: >-
  One request per case, temperature zero, seed 731, thinking disabled, maximum
  160 generated tokens. JSON schema and enum validation; malformed responses
  and confidence below 0.90 default to redact. One server slot, 2048-token
  context, four CPU threads, GPU offload. Each request was followed by a pause
  at least as long as its inference time. No prompt tuning or retries.
headline: >-
  Gemma 4 12B made 29 of 48 correct decisions and kept 0 of 20 third-party
  contacts. Llama 4 Scout made 45 of 48 but kept 3 of 20, each at confidence 1.00.
results:
  columns: [Model, Class accuracy, Decision accuracy, Third-party class misses, Unsafe third-party keeps, Request time (s), Whole run (s)]
  rows:
    - [Gemma 4 12B, "47/48", "29/48", "0/20", "0/20", "62.9", "132.5"]
    - [Llama 4 Scout, "45/48", "45/48", "3/20", "3/20", "126.7", "260.6"]
caveats:
  - Two models, one machine and one authored test set; each case was run once.
  - Cases include UK and Czech numbers, ISBNs, versions, dates, placeholders and invented personal emails.
  - The test cases are repetitive and explicit; they are not representative of unseen private documents.
  - There were no whole-file exclusion cases or adversarial prompt-injection cases.
  - Nineteen cases expected redaction but received whole-file exclusion. One private owner contact was misclassified, but its file was still excluded.
  - Confidence is self-reported and uncalibrated. All three unsafe Scout keeps were labelled placeholders at confidence 1.00.
  - Scout ran on an MLX server, Gemma on llama.cpp, so the two times are not a fair speed comparison.
  - Whole-run time includes loading, deliberate pauses and cleanup; request time is the sum of inference calls.
  - No private material or real-document results are included in this entry.
suggests: >-
  Decision accuracy and safety diverged: the model with fewer correct decisions was
  the safe one. Neither result establishes a safe automatic release gate.
status: complete
sources:
  - data/2026-10-31-local-contact-privacy-classification-scores.csv
---
