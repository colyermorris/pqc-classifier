# docs/data-governance.md
# Data Governance — PQC Classifier

## Purpose
Rules for ingest, storage, provenance, and licensing to ensure lawful reuse and reproducibility.

## Intake Checklist
- [ ] Identify **source** and **license_tag** (link to license text if possible).
- [ ] Confirm data is **redistributable**; if not, mark as `Proprietary` and store derived features only.
- [ ] Record **citation_key** and **raw_locator** (URL/path).
- [ ] Capture provenance: `ingested_at` (ISO 8601), `ingested_by`, optional `checksum_sha256`.
- [ ] Validate against `data/schemas/records.schema.json`.
- [ ] Document **platform** for measurements (CPU, OS, compiler flags).
- [ ] Note **transforms** in `transform_notes`; include units.
- [ ] Add minimal **reproduction steps**.

## Retention Policy
- Keep public raw and derived artifacts for 3 years or until superseded.
- For proprietary data: store minimal features; keep link-only `raw_locator`; do not redistribute raw.
- Maintain checksums for bundled CSV/JSON where feasible.

## Anonymization & Minimization
- No personal data. Strip hostnames/secrets from locators.
- Keep only high-level `platform` needed for reproducibility.

## Change Control
- Schema changes require semver bump + CHANGELOG entry.
- Record licensing/source risks in `docs/risk-register.md`.
