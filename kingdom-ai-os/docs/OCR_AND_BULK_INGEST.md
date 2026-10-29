# OCR and bulk-ingest plan

## Why files disappear in large uploads

A folder or transfer link can contain nested folders, archives, duplicate files, unsupported formats, damaged files, image-only PDFs, and files that require authentication. A chat system that only receives a subset of attachments cannot infer the missing 450 files. The first stage must enumerate every file and produce a manifest before OCR begins.

## Implemented now: inventory before extraction

Run from the project root:

```bash
python scripts/bulk_ingest_inventory.py /path/to/collection --recursive --output ./ingest-manifest.json
```

The script lists all files under the selected directory, records relative paths, file sizes and SHA-256 hashes, marks supported/unsupported types, and does not silently claim OCR success. It reports counts and supports an explicit `--max-files` cap. It does not upload files or extract archives. ZIP/7z/TAR containers are inventoried as containers and must be safely extracted into a staging directory before recursive inventory of their contents.

## Recommended OCR cascade (not installed or live-benchmarked in this package)

1. **Existing text layer first**: inspect PDFs for usable text; avoid re-OCR when the text is already present.
2. **OCRmyPDF + Tesseract**: searchable PDF baseline for printed text; retain source files and create derived outputs.
3. **PaddleOCR**: general OCR and multilingual text; evaluate its structure/table pipeline for forms.
4. **Docling**: structured document conversion and layout-aware extraction for PDFs and Office documents.
5. **Surya**: layout, reading order and tables; review model-weight license separately from code license before commercial use.
6. **Handwriting / difficult scans**: benchmark specialist models such as TrOCR or other document VLMs on a labeled sample; do not assume general VLM vision equals reliable OCR.

Sources reviewed: PaddleOCR, Docling, Tesseract, OCRmyPDF, Surya, Scrapy official documentation and recent independent OCR comparisons. See project URLs in `registries/open_source_projects.json`; all candidate statuses remain unverified until exact versions, licenses, install tests, security checks and quality benchmarks are recorded.

## Required production architecture for hundreds or millions of files

- Connectors: local folder, user-authorized Google Drive API, object storage, and explicitly authorized transfer-provider downloads. Do not rely on a chat attachment list as the authoritative inventory.
- Durable job queue and worker pool; each file gets a stable ID and state: discovered → downloaded → hashed → classified → extracted/OCR → quality-checked → indexed.
- Idempotency by SHA-256; deduplicate by hash while retaining every original path/reference.
- Checkpoint after each stage; retries with exponential backoff and dead-letter queue; preserve failed-file reasons.
- PDF page count and image dimensions recorded; split huge PDFs into page ranges; maintain page-to-source mapping and OCR confidence.
- Extract embedded images and diagrams separately, preserve page order and captions, use OCR fallback for image-only pages.
- Store originals in private object storage; extracted text and page images in a controlled index; apply tenant-level access control and audit logging.
- Quality gates: count reconciliation (discovered = succeeded + failed + pending), sample page rendering, text-coverage checks, OCR confidence, and human review for low-confidence pages.
- Security: archive path traversal limits, decompression-bomb limits, MIME sniffing, file-size/page limits, malware scanning, sandboxed parsers, SSRF defenses, and strict access controls.

## Can it process 500 images or a million pages?

The inventory tool can enumerate large local collections subject to disk I/O, memory, and runtime; it is not an OCR service. The current app does not yet provide the distributed queue, authorized Drive/WeTransfer connectors, storage, OCR workers, or index needed to promise a 500-file end-to-end run or a million-page crawl. A million-page workload is possible in principle with partitioning, enough workers/storage, careful rate limits, and budget monitoring, but no honest maximum can be stated before benchmarking the actual files, models, hardware, target domains and throughput.

## Acceptance criteria before calling OCR complete

- Reconcile the inventory against the source provider's own item count.
- No missing or duplicate source IDs; every item ends in success, skipped-with-reason, failed-with-reason, or pending.
- Benchmark clean print, rotated phone photos, low-resolution scans, tables, columns, handwriting, multilingual text, and image-only PDFs.
- Publish character error rate / word error rate where ground truth exists, table-structure accuracy, page throughput, GPU/CPU/RAM use, and per-page failure rate.
- Run 500 mixed files as an integration test, then a staged 10,000-page soak test before scaling further.
