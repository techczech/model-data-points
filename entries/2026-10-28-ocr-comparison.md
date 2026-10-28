---
id: 2026-10-28-ocr-comparison
title: "OCR comparison: Unlimited-OCR 2, Docling and MinerU on academic PDFs"
date: 2026-10-28
task_type: ocr
models:
  - name: Unlimited-OCR 2
    provider: Baidu
    open_weights: true
    access: local
    version: "about 3B parameters, MIT licence, served with SGLang"
  - name: Unlimited-OCR 2
    provider: Baidu
    open_weights: true
    access: local
    version: "same weights, Hugging Face Transformers"
  - name: Docling
    provider: Docling project
    open_weights: true
    access: cli
    version: "2.93"
  - name: MinerU
    provider: OpenDataLab
    open_weights: true
    access: cli
    version: "3.1.9 (MinerU2.5-Pro model)"
purpose: >-
  Decide whether a new OCR model is worth adding to a PDF-to-Markdown
  workflow for academic papers, which already uses Docling by default and
  MinerU for maths-heavy papers.
context: >-
  10 academic papers, 174 pages: three two-column journal papers, two
  table-heavy papers, two maths-heavy papers, one scanned 1967 book chapter,
  one 66-page report and one Spanish-language paper. All runs on an NVIDIA
  DGX Spark (GB10, 128 GB unified memory), one tool at a time.
method: >-
  Each paper was converted to Markdown by each tool and wall-clock time was
  recorded per paper. The Transformers route was stopped after 4 papers as
  too slow. Text was compared with the PDF's own text layer (word error rate
  after normalising whitespace and hyphenation), and every number in each
  output was checked against the numbers in the text layer. The scan was
  compared with OCRmyPDF output instead. Tables emitted were counted.
headline: >-
  Docling took 3.5 minutes for all 10 papers, Unlimited-OCR 2 on SGLang
  31 minutes and MinerU 62 minutes, with no accuracy advantage for either
  slower tool on born-digital papers.
results:
  columns: [Setup, Total time (10 papers), Time per page, Word error rate vs text layer, Numbers not in text layer, Tables emitted]
  rows:
    - [Docling 2.93, 3.5 min, about 1.2 s, 21.9%, 215, 81]
    - [Unlimited-OCR 2 (SGLang), 30.9 min, about 10.7 s, 22.7%, 249, 84]
    - [MinerU 3.1.9, 61.7 min, about 21 s, 27.4%, 302, 153]
    - [Unlimited-OCR 2 (Transformers), "4 papers only: 446-4,562 s each", not computed, not comparable, not comparable, not comparable]
caveats:
  - One machine, one set of 10 papers, one run each (n=1).
  - The word error rate is dominated by reading order (headers, footnotes, figure text placed differently), so it shows the tools as roughly equal rather than measuring misread words.
  - Most "numbers not in text layer" are page numbers, table cells or formatting differences, not misreadings; one real misreading was found in Unlimited-OCR 2 output (a caption's 75% written as 55%).
  - One 66-page report accounts for most absent numbers in every tool (200 to 261).
  - On the scanned chapter, against OCRmyPDF as baseline, Unlimited-OCR 2 (19.3%) and MinerU (17.6%) differed far less than Docling (37.5%).
  - SGLang times exclude about 1 min 45 s of server start-up; the server held about 61 GB of GPU memory.
  - Table layout quality was not judged by eye.
suggests: >-
  For born-digital academic PDFs, Docling was about nine times faster than
  Unlimited-OCR 2 and as accurate on these measures, so the new model was not
  adopted. Unlimited-OCR 2 may be worth a look for scanned pages, and only
  through a serving engine such as SGLang: through Transformers it was 5 to
  10 times slower again.
status: complete
sources:
  - data/2026-10-28-ocr-comparison-timings.csv
---
