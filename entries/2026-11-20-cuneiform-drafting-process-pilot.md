---
id: 2026-11-20-cuneiform-drafting-process-pilot
title: "Does batching or a staged process improve model translations of cuneiform tablets?"
date: 2026-11-20
task_type: other
models:
  - name: Claude Sonnet 5.5
    provider: Anthropic
    open_weights: false
    access: cli
    version: "draft translations and revisions"
  - name: GPT-6.2 Sol
    provider: OpenAI
    open_weights: false
    access: cli
    version: "critic in the staged process"
  - name: GPT-6.1 Sol
    provider: OpenAI
    open_weights: false
    access: cli
    version: "judge"
  - name: Claude Opus 5.5
    provider: Anthropic
    open_weights: false
    access: cli
    version: "wrote the period and genre reference sheets"
purpose: >-
  An earlier set of 600 draft English translations of cuneiform tablets was made
  50 tablets per session with nine outputs requested per tablet. Test whether
  one tablet per call, translation alone, or a staged process would give better
  translations.
context: >-
  26 tablets from public CDLI data that have published translations, 496
  aligned lines, shown on the public site https://wedgewise.pages.dev. The same
  judge model and the same judge instruction were used as for the earlier
  drafts. Published translations entered no generation input. No generation or
  critic call had web access.
method: >-
  Five candidates were judged line by line against the published translation as
  same, minor difference, different or declined. batch-a and batch-b are the
  existing batch drafts judged twice, to measure judge noise. single-old gave
  the same instruction one tablet per fresh call (26 calls). single-translate
  asked for translation only, one tablet per fresh call (26 calls). staged
  added a reference sheet for the tablet's period and genre, had a second model
  flag lines against the transliteration, and had the drafting model revise the
  flagged lines (26 drafts, 26 critic calls, 24 revision calls, 150 flags).
  Each candidate was judged in its own fresh session under a letter code, and
  the key to the codes was kept away from the judge until all verdicts were
  written.
headline: >-
  The staged process gave a net gain of 12 of 496 lines, while a second
  judgement of identical drafts disagreed on 47 lines; batching, and asking for
  nine outputs at once, did not hurt.
results:
  columns: [Candidate, Same, Minor difference, Different, Declined, "Different, Old Babylonian", "Different, Ur III"]
  rows:
    - [batch-a (existing drafts), 42%, 27%, 27%, 4%, 41-43%, 7-10%]
    - [batch-b (same drafts rejudged), 40%, 27%, 29%, 4%, 41-43%, 7-10%]
    - [single-old, 40%, 33%, 27%, 0%, 39%, 7-10%]
    - [single-translate, 36%, 33%, 29%, 1%, 40%, 7-10%]
    - [staged, 37%, 37%, 24%, 2%, 34%, 7-10%]
caveats:
  - Only 26 tablets and 496 lines, one run per candidate.
  - The judge is a model (GPT-6.1 Sol), not a specialist in cuneiform.
  - Judge noise is large. Two judgements of identical drafts disagree on 47 of 496 lines (9.5%), and their "same" share differs by 2 points.
  - The reference sheets used in the staged process were written by a model.
  - The calling programs add their own fixed instructions to each call, so the text sent was not only the instruction described here.
  - Percentages are shares of the 496 lines; the Ur III figure is given as a range across candidates (7-10%), not per candidate.
suggests: >-
  Batching did not make translations worse; one tablet per call with the same
  instruction gave the same profile and stopped the model declining lines,
  which became minor differences. The staged process reduced outright wrong
  lines in Old Babylonian legal and literary texts, but the gain is within the
  range of judge and run-to-run variation, so it is a direction, not a settled
  result. The text mattered more than the process: Ur III administrative lines
  were mostly right and Old Babylonian literary lines mostly wrong whatever the
  method.
status: complete
sources:
  - data/2026-11-20-cuneiform-drafting-process-pilot-overall.csv
  - data/2026-11-20-cuneiform-drafting-process-pilot-different-by-group.csv
  - https://wedgewise.pages.dev
---

## More detail

- **Batching.** One tablet per call with the same instruction gave the same profile as the batch drafts. It stopped the model declining lines ("[broken]"), which became minor differences instead. Asking for nine outputs at once did not hurt the translation either: translation alone came out slightly worse, within noise.
- **Staged process.** Fewer outright wrong lines in Old Babylonian legal and literary texts, more lines with minor differences, and a slightly lower share judged the same. By genre, "different" fell in legal texts (23% to 15%) and literary texts (46% to 37%), and stayed at 9% in administrative texts.
- **Paired by line**, against lines both batch judgements agree on: staged turned 48 "different" lines into something better and made 36 previously acceptable lines "different", a net 12 lines. single-old: 41 against 37. single-translate: 34 against 38.
- **Run-to-run variation.** Every rerun changes many lines in both directions (about 75 to 85 per candidate). The model's own run-to-run variation is larger than the differences between processes.
- **Period.** Lines judged "different" were 7 to 10% for Ur III for every candidate. For Old Babylonian they were 41 to 43% for the batch drafts, 39% for single-old, 40% for single-translate and 34% for staged.
