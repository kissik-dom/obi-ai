# Long-document and book workflow

## What the current renderer does

`POST /api/v1/documents/render-pdf` formats already-written section text into a PDF. The renderer currently supports a title page, a contents list, chapter headings, selectable built-in serif/sans/monospace fonts, A4/Letter/Legal paper, configurable margins, a glossary, page numbering, and the signature gold rule with centered diamond and a footer quote on every page. The API limits the full payload to 3 million characters and 250 sections. A local controlled stress test rendered 509 pages from 1.9 million characters; this is a layout stress test, not a test of generating or fact-checking a complete book. A rendered PDF is a layout artifact, not proof that the claims are true or that the page count will be exactly the number requested.

Reusable starting points are in `registries/document_templates.json`. `POST /api/v1/documents/template-profile` extracts a bounded style profile from DOCX/PDF/image bytes without saving the source file. DOCX profiles include paragraph style names and section geometry; PDF profiles include page count, page dimensions, and sample extractable text; image profiles include pixel dimensions and mode.

## Required pipeline for a 500-page researched book

1. **Brief and scope:** agree on audience, thesis, date range, language, target page count, citation style, permissions, and excluded claims.
2. **Source ledger:** record each source's title, author/organization, publication date, URL/archive identifier, source type, access date, and claims it supports. Separate user-provided claims from independently corroborated evidence.
3. **Outline:** generate parts, chapters, section goals, estimated word budgets, and required citations. Ask for approval before drafting the full book.
4. **Chapter generation:** draft one chapter at a time with a controlled context window. Carry forward a short continuity ledger, canonical names, date/number facts, open questions, and the bibliography rather than repeatedly sending the entire book.
5. **Verification:** check every citation against retrieved source material; flag missing page numbers, unsupported quotations, contradictory dates, and unresolved assertions. Never fabricate citations.
6. **Consistency pass:** check terminology, names, chronology, repetition, chapter transitions, and glossary definitions across all chunks.
7. **Layout pass:** render chapters using a selected template, insert cover/title page, contents, glossary, bibliography, page numbers, and repeated footer design.
8. **Visual QA:** inspect representative pages and all pages with tables, figures, footnotes, or layout overflow. Compare reference screenshots when matching an example.
9. **Re-render and verify:** count pages, verify page numbers, extract the PDF text, inspect fonts and image embedding, check citations, and archive the exact source + output + template version.

## Important limitation

The current package includes the **rendering and template-profile foundation**, not a durable multi-agent book-production queue. Chapter orchestration, job persistence, resumability, source retrieval/citation verification, approval checkpoints, and a production file store still need implementation before claiming that a one-sentence request will reliably produce a fact-checked 500-page book unattended.

## Template fidelity levels

- **Native template:** exact layout rules authored in the system's template registry; strongest repeatability for new documents.
- **Style-profile recreation:** extract styles, page dimensions, margins, and text from a reference and rebuild in the native renderer.
- **Visual reconstruction:** additionally inspect screenshots, fonts, spacing, page breaks, images, tables, and ornaments. Requires side-by-side QA.
- **Pixel-perfect claim:** never promise this for arbitrary files without a rendering engine that preserves the original format and a human-reviewed visual comparison. An image may omit editable text and font metadata, so some choices require approximation.
