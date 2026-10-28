---
id: 2026-03-08-local-image-generation-m4-max
title: "Local image generation on an M4 Max: FLUX.2 Klein 4B and Qwen-Image"
date: 2026-03-08
task_type: image-generation
models:
  - name: FLUX.2 Klein 4B
    provider: Black Forest Labs
    open_weights: true
    access: local
    version: "4B parameters, 8-bit, run with mflux"
  - name: Qwen-Image 2512
    provider: Alibaba
    open_weights: true
    access: local
    version: "20B parameters, 4-bit MLX build, Apache 2.0, run with mflux 0.16 or later"
purpose: >-
  Find out how long Qwen-Image takes to generate an image on Apple Silicon,
  and how that compares with FLUX Klein.
context: >-
  An Apple M4 Max computer with 128 GB of unified memory and 40 GPU cores. Both
  models were run through the mflux command-line tool, one image per setting,
  in a hands-on session.
method: >-
  Images were generated at the resolutions and step counts in the table and
  total time was noted for each.
headline: >-
  At 1024 x 1024, FLUX Klein took about 18 s; Qwen-Image at 20 steps took about
  8 minutes.
results:
  columns: [Model, Quantisation, Resolution, Steps, Time]
  rows:
    - [FLUX.2 Klein 4B, 8-bit, 512 x 512, 4, about 7 s]
    - [FLUX.2 Klein 4B, 8-bit, 1024 x 1024, 4, about 18 s]
    - [Qwen-Image 2512, 4-bit, 1024 x 1024, 20, about 8 min]
    - [Qwen-Image 2512, 4-bit, 1328 x 1328, 20, about 10 min]
caveats:
  - One machine, one run per setting (n=1), timings approximate.
  - Image quality was not scored; only generation time is compared here.
  - The two models were run at different quantisation levels (8-bit and 4-bit).
  - An earlier estimate of about 3 minutes for Qwen-Image was too low.
suggests: >-
  On this machine Qwen-Image ran at about 23.5 s per step, which made a
  20-step image take about 8 minutes against about 18 s for FLUX Klein at
  1024 x 1024. The notes record that Qwen-Image renders text in images better,
  but that was not measured here.
status: complete
sources: []
---
