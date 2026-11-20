---
id: 2026-11-20-copy-writer-comparison
title: "Which model writes the clearest public copy for a specialist reader? Four writers, six pages"
date: 2026-11-20
task_type: other
models:
  - name: Gemini 4 Hydrogen
    provider: Google
    open_weights: false
    access: api
  - name: Gemini 4 Neon
    provider: Google
    open_weights: false
    access: api
  - name: GPT-6.2 Sol
    provider: OpenAI
    open_weights: false
    access: api
  - name: Claude Opus 5.5
    provider: Anthropic
    open_weights: false
    access: api
purpose: >-
  Find which model writes the clearest public copy for a specialist reader with
  no knowledge of AI, and whether the four writers differ in ways that matter.
context: >-
  Six pages of a public website, 7,822 words in the original. Each writer
  rewrote the same pages from the same inputs and rules. Each set was read by
  two readers who were not told who wrote it: Claude Sonnet 5.5 and GPT-6 Luna,
  each playing a university Assyriologist with no knowledge of AI.
method: >-
  Each writer produced a complete rewrite of the six pages. Each set was read
  cold. For each page the reader said back what the model was given, what it
  was asked, what it returned, how that was checked and the main finding, and
  quoted every sentence it did not understand. Scores were recorded per set and
  reader, along with word counts.
headline: >-
  No writer clearly won: the four sets differed less from one another than the
  two readers differed in strictness, and no set produced pages a cold reader
  would read to the end.
results:
  columns: ["Writer", "Words", "Reader", "Understanding (0-10)", "Willing to keep reading (0-10)", "Said back in full (of 30)", "Not understood (sentences)", "Read to the end (of 6)"]
  rows:
    - ["Gemini 4 Hydrogen", "8,228", "Sonnet", "4", "4", "11", "49", "3"]
    - ["Gemini 4 Hydrogen", "8,228", "Luna", "7", "6", "22", "0", "3"]
    - ["Gemini 4 Neon", "9,408", "Sonnet", "5", "4", "17", "47", "1"]
    - ["Gemini 4 Neon", "9,408", "Luna", "6", "5", "22", "6", "1"]
    - ["Claude Opus 5.5", "8,719", "Sonnet", "5", "5", "10", "41", "3"]
    - ["Claude Opus 5.5", "8,719", "Luna", "6", "6", "23", "20", "1"]
    - ["GPT-6.2 Sol", "6,940", "Sonnet", "4", "3", "8", "60", "1"]
    - ["GPT-6.2 Sol", "6,940", "Luna", "6", "5", "21", "7", "1"]
caveats:
  - One task, six pages, one run per writer, two readers per set.
  - The two readers disagree by two points on the same text, so a one-point difference between writers means nothing.
  - Claude Opus 5.5 and the Sonnet reader are from the same model family, which may favour or disfavour it.
  - Sonnet was the stricter reader on every set (understanding 4 to 5, against 6 to 7 from Luna).
  - Not measured: a second round with a reader's report in hand, or a page limit.
suggests: >-
  The reader loop mattered more than the choice of writer. The writers failed in
  different ways: one leaked internal detail, one was vague, and one explained
  at length, so each needs a different check.
status: complete
sources:
  - https://github.com/techczech/preprint-archives-ai-methods-demo/blob/main/research/copy-writer-comparison/results.md
---

## More detail

Blind labels in the source were K = Gemini 4 Neon, M = Claude Opus 5.5, P = GPT-6.2 Sol and T = Gemini 4 Hydrogen.

"Said back in full" counts the fields (five per page, thirty per set) the reader marked "yes". "Not understood" is the number of sentences the reader quoted. "Read to the end" is the number of the six pages the reader said it would finish.

- **Gemini 4 Hydrogen** had the most regular structure and the fewest sentences before a first result. It broke the rule against internal detail about forty times.
- **Gemini 4 Neon** was the longest set. The stricter reader said back more of it than of any other set. One number is wrong: it says the judging model noted that the transliteration supports the draft in 3 of the 117 "different" lines; the data has 2.
- **Claude Opus 5.5** was the only writer to add an interpretation a specialist can use. It had the fewest sentences quoted as not understood by the stricter reader, and it put the most text before a result.
- **GPT-6.2 Sol** was the shortest set and the only one with no internal detail and no factual slip found. It was also the vaguest, and the stricter reader said back least of it (8 of 30).
