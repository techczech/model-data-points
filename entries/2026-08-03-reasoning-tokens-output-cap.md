---
id: 2026-08-03-reasoning-tokens-output-cap
title: "Reasoning tokens used up an output cap on GPT-5.5 Pro"
date: 2026-08-03
task_type: api-behaviour
models:
  - name: GPT-5.5 Pro
    provider: OpenAI
    open_weights: false
    access: api
    version: "gpt-5.5-pro-2026-04-23, Responses API"
purpose: >-
  Record what happens when a request to a reasoning model sets a maximum
  output length that the model's reasoning alone can use up.
context: >-
  Two requests to the Responses API in a cost-controlled consultation. Costs
  are at the provider's list rates of $30 per million input tokens and $180
  per million output tokens.
method: >-
  The first request used medium reasoning and max_output_tokens of 6,000. A
  second request on a revised problem used high reasoning and no output cap.
  Status, token usage, time and visible text were recorded from the response.
headline: >-
  With max_output_tokens at 6,000, all 6,000 tokens went to reasoning and no
  text came back; an uncapped run took 542 s and 22,828 output tokens.
results:
  columns: [Request, Reasoning setting, Output cap, Status, Time, Input tokens, Output tokens, Reasoning tokens, Visible answer tokens, Approximate cost]
  rows:
    - [Capped (streaming retry), medium, "6,000", incomplete, 101.25 s, "1,718", "6,000", "6,000", "0", "$1.13"]
    - [Uncapped, high, none, completed, 541.92 s, "1,940", "22,828", "19,793", "3,035", "$4.17"]
caveats:
  - Two requests only (n=1 each), and they used different reasoning settings and different problems.
  - The first non-streaming attempt ended after about 40 seconds with a disconnection; its usage and cost could not be established, so the capped cost excludes it.
suggests: >-
  The output cap covered reasoning and visible text together, so a cap that
  looks generous for the answer can be spent before any answer is produced.
  The uncapped run used more than three times the capped limit on reasoning
  alone.
status: complete
sources: []
---
