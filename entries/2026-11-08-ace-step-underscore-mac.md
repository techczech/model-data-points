---
id: 2026-11-08-ace-step-underscore-mac
title: "ACE-Step 1.5 turbo: instrumental background music for a short cartoon on a Mac"
date: 2026-11-08
task_type: other
models:
  - name: ACE-Step 1.5 (turbo DiT)
    provider: ACE Studio and StepFun (ACE-Step project)
    open_weights: true
    access: local
    version: "acestep-v15-turbo, MIT licence, MLX backend, 8 inference steps, LM planning off"
purpose: >-
  First try of an open music model: can it make usable background music for a
  108-second voiced cartoon locally, and how fast?
context: >-
  Apple M4 Max laptop, 128 GB unified memory. Model weights about 11 GB in
  total, downloaded once over a slow home connection (about 1 MB/s).
method: >-
  One text brief (gentle, playful indie underscore: plucked guitar,
  glockenspiel, upright bass, brushed drums; sparse, leaves room for
  dialogue), instrumental, 112 s, 92 BPM, D major, seed 7, batch of 3. Each
  take was mixed about 14 dB under the dialogue with sidechain ducking, and
  Whisper large-v3-turbo transcribed each mix to check the dialogue was still
  intelligible. Musical quality was judged by listening, not measured.
headline: >-
  Three 112-second instrumental takes took 72 s of generation in total (about
  4.7 times faster than real time); with the music ducked under the voices,
  Whisper still heard 99-100% of the script's words.
results:
  columns: [Take, Length, Detected tempo, Ending, Mix loudness, Script words heard by Whisper]
  rows:
    - [1, 112 s, "92 BPM (tracker reported double time, 185)", ends by itself, -16.0 LUFS, 99%]
    - [2, 112 s, 92 BPM, ends by itself, -16.0 LUFS, 99%]
    - [3, 112 s, 92 BPM, still playing at 112 s (needs a fade), -16.0 LUFS, 100%]
caveats:
  - One brief, one seed, one machine (n=1).
  - The 72 s excludes model loading and the one-off download, which stalled twice with the built-in downloader and finished with the Hugging Face CLI.
  - Tempo was checked with a beat tracker; style, instrumentation and quality were not scored.
  - The larger XL (4B) variant was not tried.
suggests: >-
  ACE-Step 1.5 turbo makes full-length instrumental takes faster than real
  time on an Apple M4 Max, so generating several takes and choosing by ear is
  cheap. Asking for a sparse arrangement plus ducking kept dialogue clear.
status: complete
sources:
  - https://github.com/ace-step/ACE-Step-1.5
  - https://huggingface.co/ACE-Step/Ace-Step1.5
---

## What was made

Background music for a short animated story with two synthetic voices. The brief asked for a quiet arrangement that leaves room for speech, and the mix lowers the music further whenever someone speaks.

## Notes

The model ran with its language-model planner switched off, so the brief went straight to the diffusion model. Takes 1 and 2 ended on their own a few seconds before 112 s; take 3 kept playing and relies on the fade-out.
