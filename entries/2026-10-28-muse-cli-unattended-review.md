---
id: 2026-10-28-muse-cli-unattended-review
title: "Muse CLI: one unattended source-review run"
date: 2026-10-28
task_type: api-behaviour
models:
  - name: Muse Wonder Full
    provider: Meta
    open_weights: false
    access: cli
    version: "muse-wonder-full-1.0; reasoning effort medium"
purpose: >-
  Check whether the Muse CLI could complete a bounded code review without
  stopping for tool approval.
context: >-
  One source-only review of an application code change. The reviewer could
  read the project but had shell, write, web, reminder and user-input tools
  disabled. No institutional or personal knowledge documents were supplied.
method: >-
  Run muse exec with explicit approval-mode never, approval-judge off and
  per-run Contributor mode on. Keep the sandbox enabled. Collect the CLI exit
  status, review output and recorded approval-request count.
headline: >-
  The source-only review completed with exit code 0 and no approval requests.
results:
  columns: [Run, Exit code, Approval requests, Review returned]
  rows:
    - ["One unattended source review", 0, 0, "Yes"]
caveats:
  - One bounded run; this is not an approval-prompt reliability estimate.
  - The reviewer did not execute tests, run a build or verify the application at runtime.
  - The review verdict was returned by the model; this entry does not independently score its quality.
  - Contributor mode was explicitly permitted for the code in this run; this does not establish permission for other material.
  - The sandbox remained enabled; unattended approval settings do not remove sandbox restrictions.
  - Elapsed time, tokens and cost were not measured for this entry.
suggests: >-
  These per-run CLI settings were sufficient for this read-only review to
  finish without tool-approval interruptions. Broader coding and runtime
  tasks need separate evidence.
status: complete
sources:
  - data/2026-10-28-muse-cli-unattended-review-results.csv
---

The observations were extracted from the completed run's local records. The
public data file contains only the result and settings; project content,
local paths and the review transcript are not published.
