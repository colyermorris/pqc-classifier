# Risk Register

| ID | Risk | Likelihood | Impact | Owner | Mitigation | Status |
|----|------|------------|--------|-------|------------|--------|
| R1 | Dataset too small or biased | Medium | High | Data Lead | Expand sources; quarterly refresh | Open |
| R2 | Misclassification in new environments | Medium | Medium | Model Lead | Robustness tests; calibration | Open |
| R3 | Secrets committed by mistake | Low | High | Dev Lead | .gitignore; pre-push checks | Open |
| R4 | Dependency or build breakage | Medium | Medium | Eng | Pin versions; CI checks | Open |



- Risk: Upstream sources may change license terms or disappear.  
  Mitigation: Store license tags, citations, and checksums; keep link-only locators for proprietary data.

  # Risk Register

## R-002: Alias Drift Across Sources
- **Context:** Upstream repos (liboqs, PQClean, vendor SDKs) evolve labels. New tokens may bypass joins.
- **Impact:** Fragmented features, mis-joins, noisy model labels.
- **Likelihood:** Medium | **Severity:** Medium
- **Mitigations:**
  - Establish canonical map (`src/validate/canonical_names.yaml`) and apply normalization before joins.
  - Add CI test to fail builds on unmapped tokens (planned WP-03).
  - Log alias-resolution reports during ETL with first-seen file/line.
- **Owner:** Data Eng
- **Status:** Mitigation in progress (map shipped; CI test pending).

## R-003: Conflicting Tokens (Same Alias → Multiple Canonicals)
- **Context:** Ambiguous labels like `spx`, versioned `oqs_*` tokens.
- **Impact:** Wrong canonical assignment.
- **Mitigations:**
  - Priority rules inside normalization (e.g., map `spx` → `sphincsplus` under SLH-DSA).
  - Unit tests for known ambiguous cases (planned WP-03).
- **Owner:** Data Eng
- **Status:** Open
