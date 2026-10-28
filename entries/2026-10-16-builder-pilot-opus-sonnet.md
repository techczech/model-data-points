---
id: 2026-10-16-builder-pilot-opus-sonnet
title: "Builder pilot: Opus 5.5 rebuilds five app tasks first built by Sonnet 5.5"
date: 2026-10-16
task_type: coding
models:
  - name: Claude Opus 5.5
    provider: Anthropic
    open_weights: false
    access: cli
    version: "builder; rebuilt five tasks"
  - name: Claude Sonnet 5.5
    provider: Anthropic
    open_weights: false
    access: cli
    version: "builder; original accepted builds"
  - name: GPT-6.1 Sol
    provider: OpenAI
    open_weights: false
    access: cli
    version: "blind reviewer"
  - name: Muse Wonder Full 1.0
    provider: Meta
    open_weights: false
    access: cli
    version: "blind reviewer"
  - name: Claude Fable 5.1
    provider: Anthropic
    open_weights: false
    access: cli
    version: "checked every reviewer claim"
purpose: >-
  Find out whether Opus 5.5 using fewer tokens would make it cheaper than
  Sonnet 5.5 on tasks Sonnet could already do.
context: >-
  Five real tasks from app development. The Sonnet side was the build that had
  originally been accepted. Opus rebuilt each task from the same starting
  state and brief. Costs are at published list prices.
method: >-
  Two reviewers (GPT-6.1 Sol and Muse Wonder Full) scored each build solo
  against a rubric (1 to 5) without knowing which model built it, then
  compared the pair side by side. Fable 5.1 checked each of the 86 claims the
  reviewers made.
headline: >-
  At list prices Opus cost $9.02 against $3.78 for Sonnet (2.4 times); blind
  review scores were close (3.30 and 3.40 against 3.27 and 3.23). One build
  per cell.
results:
  columns: [Measure, Sonnet 5.5, Opus 5.5]
  rows:
    - [Total build cost at list price, "$3.78", "$9.02"]
    - ["Task 1 (calls, cost)", "17, $0.72", "23, $1.91"]
    - ["Task 2 (calls, cost)", "28, $0.685", "16, $1.60"]
    - ["Task 3 (calls, cost)", "12, $0.36", "26, $1.32"]
    - ["Task 4 (calls, cost)", "46, $1.07", "27, $1.60"]
    - ["Task 5 (calls, cost)", "32, $0.94", "49, $2.59"]
    - ["Mean rubric score, Sol reviewer (1-5)", "3.40", "3.30"]
    - ["Mean rubric score, Muse reviewer (1-5)", "3.23", "3.27"]
    - [Side-by-side preference (10 judgements), "1", "9"]
    - [Verified unique defects, "2 major, 22 minor", "2 major, 18 minor"]
caveats:
  - One build per task per model (n=1 per cell); the source report calls the result tentative.
  - The Opus builds were not taken through review to acceptance; the Sonnet builds were accepted builds.
  - The side-by-side judgements favoured the build shown first in 7 of 10 cases, so the 9 of 10 preference for Opus is weak evidence.
  - Reviewer precision differed: 18 of 24 Sol claims (75%) and 36 of 62 Muse claims (58%) were verified as real.
  - Checking the reviewers' claims with Fable 5.1 cost $16.38 at list price, more than both builds together. That figure is not in the build costs above.
  - Review packets that contained only diffs produced false defect claims.
  - What counts as a call in the per-task rows is not defined in the source notes.
suggests: >-
  On these five tasks Opus cost about 2.4 times as much as Sonnet at list
  prices and did not score clearly higher on the rubric. The pilot is too
  small to settle the question of token efficiency.
status: complete
sources: []
---
