---
id: 2026-11-08-androgynous-tts-voices
title: "Making two androgynous teenage TTS voices: VoiceDesign casting, a gender classifier and a Praat shift"
date: 2026-11-08
task_type: speech
models:
  - name: Qwen3-TTS VoiceDesign
    provider: Alibaba Qwen
    open_weights: true
    access: local
    version: "1.7B bf16 via mlx-audio (casting takes)"
  - name: Qwen3-TTS Base
    provider: Alibaba Qwen
    open_weights: true
    access: local
    version: "0.6B bf16 via mlx-audio (cloning each line from the casting take)"
  - name: wav2vec2 voice-gender classifier
    provider: alefiury (Hugging Face)
    open_weights: true
    access: local
    version: "wav2vec2-large-xlsr-53-gender-recognition-librispeech"
  - name: Praat "Change gender"
    provider: Praat (via parselmouth)
    open_weights: true
    access: local
    version: "parselmouth"
purpose: >-
  Two cartoon characters with no gender needed voices that are neither male-
  nor female-coded but still distinct from each other.
context: >-
  Apple M4 Max laptop. 32 lines of dialogue (17 for one character, 15 for the
  other). The classifier was checked first on two earlier, clearly gendered
  casting takes: it scored them 0.01 and 1.00 P(female).
method: >-
  Text personas asked for androgynous, mid-pitch 17-year-old voices. 40
  VoiceDesign takes of a casting line per character were scored by the
  classifier; the most ambiguous pair with speaker-embedding similarity below
  0.80 was kept. Every line was then cloned from its casting take. A per-line
  classifier gate was tried and abandoned. Finally one fixed Praat "Change
  gender" shift per voice (formant ratio and pitch median, grid search) was
  chosen so the classifier's verdicts split about evenly across that voice's
  lines.
headline: >-
  The classifier lands near 0 or 1 on whole lines even when the casting take
  scored 0.44-0.49, so ambiguity had to be set per voice, not per line: one
  small fixed shift moved the share of lines heard as female from 28% and 97%
  to 47% for both voices.
results:
  columns: [Step, Voice A, Voice B]
  rows:
    - [Casting takes in the 0.2-0.8 P(female) band, "6 of 40", "7 of 40"]
    - [Chosen casting take P(female), 0.44 (139 Hz), 0.49 (149 Hz)]
    - [Mean P(female) of cloned lines, 0.28, 0.97]
    - [Shift chosen, "pitch median 155 Hz, formants unchanged", "pitch median 160 Hz, formants x0.94"]
    - [Share of lines heard as female after the shift, 47%, 47%]
    - [Speaker similarity within voice after the shift, 0.77, 0.82]
    - [Speaker similarity between the two voices, 0.67, 0.67]
caveats:
  - One classifier, trained on read audiobook speech; it decides male or female and was used here only as a proxy for "gender-ambiguous". Listening is the real test.
  - The classifier is very sensitive; a 5% formant shift flipped one line from 0.01 to 0.99.
  - One script, one run (n=1). Pair similarity threshold 0.80 chosen by hand.
suggests: >-
  To get gender-ambiguous synthetic voices, cast from many designed takes and
  then apply one calibrated formant and pitch shift per voice; gating each line
  on a binary classifier wastes retries because its scores are rarely in the
  middle.
status: complete
sources:
  - https://huggingface.co/alefiury/wav2vec2-large-xlsr-53-gender-recognition-librispeech
  - https://huggingface.co/mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16
  - https://parselmouth.readthedocs.io/
---

## Why per voice and not per line

On whole lines the classifier's scores clustered at the ends: 26 of 32 lines scored below 0.05 or above 0.95 before the shift. Rejecting takes that were not in the middle burned all eight retries on the first line. A single shift per voice keeps each character's voice consistent from line to line, and choosing it so verdicts split about evenly means neither voice reads as one gender overall.
