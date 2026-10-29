# Registry status

- `tabs.json`: 24 named tabs preserved from the Voltaire two-key mapping, plus four explicit unresolved placeholders because the source mapping names 24, while the current target is 28. These placeholders must not be treated as completed features.
- `models.json`: 101 candidate model records seeded from names in the source document. Every entry is UNVERIFIED; the source contains names/claims but does not establish exact provider model IDs, current availability, licenses, or actual tests.
- `open_source_projects.json`: 532 unique project/tool candidate names extracted from the source mapping and older category lists. These are intake records, not a claim that the full 600+ list has been normalized or that any project is open source or installed. The source document contains category-level summaries and mixed commercial APIs; these are preserved as unverified candidates, not asserted to be open source. The source claims 600+ entries, but only 532 unique names have been normalized in this intake pass; additional source mentions and the remaining claimed inventory require extraction and review.

Before activation, each model must have an exact provider model ID or repository/checkpoint and verified access/license details. Each project needs an official repository, real license file, project type, pinned release/commit, dependency/security review, install/health/integration tests, hardware/network needs, and a dated evidence record.


A small subset has `open_source_status: VERIFIED_LICENSE` with `license_source_url` and a review note based on the upstream project or package metadata. This verifies only the license claim for the named version/project; it does not mean the project was installed, security-audited, tested, or approved for production. All project `status` fields remain `UNVERIFIED`.
