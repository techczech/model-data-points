---
id: 2026-10-27-computer-use-haiku-terra-luna
title: "Computer use: Claude Haiku 5.5, GPT-6.1 Terra and GPT-6 Luna"
date: 2026-10-27
task_type: computer-use
models:
  - name: Claude Haiku 5.5
    provider: Anthropic
    open_weights: false
    access: cli
    version: "run with claude -p, model set to haiku"
  - name: GPT-6.1 Terra
    provider: OpenAI
    open_weights: false
    access: cli
    version: "gpt-6.1-terra, run with codex exec"
  - name: GPT-6 Luna
    provider: OpenAI
    open_weights: false
    access: cli
    version: "gpt-6-luna, run with codex exec"
purpose: >-
  Decide which model should be the default for computer-use checks (opening a
  page or an app, looking at it, and reporting what is wrong).
context: >-
  Two scripted jobs. The first was a local web page with 5 planted defects and
  2 traps. The second was a desktop app built with Electron, controlled over
  the Chrome DevTools Protocol in a second, hidden instance. Each model ran
  each job 3 times; the table shows medians. A fixed scorer gave quality as 0.5
  for correct facts, 0.3 for defect recall, 0.1 for screenshots taken and 0.1
  for valid JSON output, minus 0.05 per false defect reported.
method: >-
  Same prompt and same job for each model, 3 runs per model per job, scored by
  the deterministic scorer. Wall-clock time and tokens were recorded per run.
  The desktop-app job was run twice because the first prompt was faulty (see
  caveats); the table shows the second run.
headline: >-
  On the web-page check Haiku scored 0.95 in 23.4 s, Luna 0.9 in 43.6 s and
  Terra 0.9 in 46.7 s; on the desktop-app check all three scored 1.0 in 35.1 s,
  47.9 s and 40.0 s.
results:
  columns: [Job, Model, Failed runs of 3, Median quality, Defect recall, False defects, Median time, Median tokens]
  rows:
    - [Web page, Claude Haiku 5.5, 0, 0.95, 1.0, 3, 23.4 s, "95,667"]
    - [Web page, GPT-6 Luna, 0, 0.9, 0.93, 4, 43.6 s, "181,396"]
    - [Web page, GPT-6.1 Terra, 1, 0.9, 0.67, 2, 46.7 s, "301,496"]
    - [Desktop app (second run), Claude Haiku 5.5, 0, 1.0, not scored, 0, 35.1 s, "225,124"]
    - [Desktop app (second run), GPT-6 Luna, 0, 1.0, not scored, 0, 47.9 s, "224,173"]
    - [Desktop app (second run), GPT-6.1 Terra, 0, 1.0, not scored, 0, 40.0 s, "202,970"]
caveats:
  - Three runs per model per job; the figures are indicative, not statistical.
  - The first desktop-app run used a prompt that said "take the first page", which was a prompt fault and not a model difference. Medians in that run were Haiku 1.0 in 44.2 s, Luna 0.5 in 61.7 s and Terra 0.45 in 36.4 s; it is not used in the table.
  - One Terra web-page run could not launch the browser (a sandbox failure) and counts as the 1 failed run.
  - The web-page test was changed after its first run, so false-defect counts are not comparable with earlier runs.
  - The models could in principle read the file holding the answer key.
  - Token counts are as reported by each tool and may not be comparable across the two tools.
  - No cost figures are given.
suggests: >-
  On these two jobs Haiku 5.5 matched or beat the other two on quality and was
  the fastest on both. The two OpenAI models took roughly twice as long on the
  web-page job, and Terra used about three times the tokens.
status: complete
sources: []
---
