# pqc-classifier

Automated classification of post-quantum cryptography (PQC) algorithms for inventory, compliance, and migration support.

## Repo Map
pqc-classifier/
├─ README.md
├─ CHANGELOG.md
├─ LICENSE
├─ .gitignore
├─ config/
│  ├─ project.yaml
│  ├─ paths.yaml
│  ├─ secrets.example.env
├─ docs/
│  ├─ proposal.md
│  ├─ charter.md
│  ├─ timeline.md
│  ├─ risk-register.md
│  ├─ ethics.md
│  ├─ data-governance.md
│  ├─ dataset-limitations.md
│  ├─ model-cards/
│  │  ├─ family_classifier.md
│  │  └─ level_classifier.md
│  └─ api-spec.md
├─ data/
│  ├─ raw/{pqclean, oqs, literature, industry}
│  ├─ interim/staging
│  ├─ processed/{master_catalog.parquet, features_static.parquet, features_dynamic.parquet, features_merged.parquet}
│  └─ schemas/records.schema.json
├─ src/
│  ├─ ingest/
│  ├─ validate/
│  ├─ features/
│  ├─ models/params/
│  ├─ eval/reports/
│  ├─ interpret/
│  ├─ api/
│  └─ utils/
├─ dashboard/{backend, frontend/src}
├─ scripts/
├─ infra/{Dockerfile, docker-compose.yml, k8s/}
└─ ci/github/workflows/

## Quickstart
python -m venv .venv
source .venv/bin/activate
pip install -r dashboard/backend/requirements.txt

## One-liners
bash scripts/make_dataset.sh
bash scripts/run_cv.sh
bash scripts/generate_reports.sh

## Config
See config/paths.yaml for canonical locations used by code and docs.
Create a local config/secrets.env by copying config/secrets.example.env and filling values.

## Governance
See docs/charter.md, docs/data-governance.md, docs/ethics.md, and docs/risk-register.md.
