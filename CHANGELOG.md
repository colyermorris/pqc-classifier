# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Initial repository scaffolding (WP-00)
- .gitignore with Python, macOS, and project rules
- GIT_HELP.md (ignored)
- Added data governance guardrails, JSON Schema for records, validator stubs, and toy example (WP-01).
- (planned) Add alias-resolution CI test and unmapped-token reporting (WP-03).


### Changed
- None yet

### Fixed
- None yet

## [WP-02] — Canonical Naming & Alias Map (2025-09-28)
### Added
- `src/validate/canonical_names.yaml` with normalization rules, family/level alias buckets, and ≥50 algorithm/param aliases.
- `docs/dataset-limitations.md` aliasing section and coverage table.

### Changed
- Documentation: clarified canonical algorithm names (ML-KEM/ML-DSA/SLH-DSA), family buckets, and level mapping {1,3,5}.

### Risks/Mitigations
- Alias drift across upstream repos — logged in `docs/risk-register.md` with CI tests planned.

## WP-03 — Ingest PQClean (api.h → records)
- Added `src/ingest/pqclean_ingest.py` CLI to scan PQClean trees and emit JSONL records.
- Added `src/validate/canonical_names.yaml` and canonicalization logic (family, param-set, NIST level, FIPS tags).
- Added validator `src/validate/validate_pqclean_records.py` for schema and consistency checks.
- Added `scripts/make_dataset.sh` with `pqclean` target wrapper.
- Output artifact: `data/interim/staging/pqclean_records.jsonl`.