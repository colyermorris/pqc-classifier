# Data Governance

## Sources and Provenance
- PQClean, OQS, literature tables, industry contributions (anonymized).

## Access and Controls
- Secrets in config/secrets.env (not committed).
- Industry data stored under data/raw/industry with restricted access.

## Retention and Refresh
- Quarterly dataset refresh; track changes in CHANGELOG.md and docs/dataset-limitations.md.

## Quality
- Schemas in data/schemas; validators in src/validate.
