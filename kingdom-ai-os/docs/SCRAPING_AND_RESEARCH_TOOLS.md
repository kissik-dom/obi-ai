# Web research, scraping, and extraction toolkit

## Recommended layered approach

1. **Playwright** for JavaScript-rendered pages and browser workflows; it supports Chromium, Firefox, and WebKit. Use it for pages that need browser rendering, not as a promise to defeat access controls.
2. **Scrapy** for structured, scheduled, large-scale crawls with pipelines, retries, and deduplication. Configure rate limits, allowed domains, and robots policy per project.
3. **Trafilatura** for article/main-text extraction and metadata from accessible HTML, with fallback extraction strategies.
4. **Crawl4AI** for crawler workflows that convert accessible pages to Markdown and optionally use structured extraction. Validate the library version and dependencies before enabling it in production.
5. **Beautiful Soup** for HTML/XML parsing after content has been lawfully fetched.
6. **Apache Tika / OCRmyPDF / Tesseract** for extracting text and metadata from documents and scanned PDFs. OCR output must be reviewed, especially names, dates, and numbers.
7. **pypdf / python-docx / ReportLab / docxtpl / LibreOffice / Pandoc** for PDF/DOCX inspection, generation, templating, and conversion.

## Safe scraping boundaries

No tool can access every site. Some content requires an account, subscription, client-side proof, or owner permission; some sites disallow automated access. The crawler service must:

- use an explicit domain allowlist for each job;
- check robots.txt and the site's terms and applicable law;
- respect rate limits, retry-after responses, and backoff;
- avoid credential theft, CAPTCHA bypass, paywall bypass, and access-control evasion;
- avoid collecting sensitive personal data unless specifically authorized and lawful;
- prevent SSRF by blocking loopback, private, link-local, metadata-service, and non-HTTP(S) destinations, including redirects and DNS rebinding;
- cap response size, content types, crawl depth, pages per domain, runtime, and concurrency;
- quarantine downloads, scan files, and isolate browser workers;
- log the job's URL scope, policy decision, errors, and source provenance.

## Status

The candidate names are added to `registries/open_source_projects.json`, but they remain `UNVERIFIED`. This is a discovery shortlist, not a completed install test, security audit, or license review. Do not enable arbitrary URL fetching in the public API before implementing SSRF protection, tenant isolation, and an isolated worker queue.

## License-source spot checks (2026-10-27)

The following entries have a license claim checked against the upstream repository or package metadata. These are **license-source checks only**; install, dependency, vulnerability, security, and production compatibility reviews remain outstanding.

| Project | License claim recorded | Upstream source |
|---|---|---|
| Scrapy | BSD-3-Clause | https://github.com/scrapy/scrapy |
| Playwright | Apache-2.0 | https://github.com/microsoft/playwright |
| Trafilatura | Apache-2.0 for current project; older versions before 1.8.0 were GPLv3+ | https://github.com/adbar/trafilatura |
| Crawl4AI | Apache-2.0 with an attribution notice | https://github.com/unclecode/crawl4ai |
| python-docx | MIT | https://pypi.org/project/python-docx/ |
| ReportLab | BSD license (see upstream license text) | https://pypi.org/project/reportlab/ |
| pypdf | BSD-3-Clause | https://github.com/py-pdf/pypdf |
| OCRmyPDF | MPL-2.0 for core software; some components have separate licenses | https://github.com/ocrmypdf/ocrmypdf |

License claims are stored with source URL and review note in `registries/open_source_projects.json`. A verified license is not a recommendation to install the software without further review.
