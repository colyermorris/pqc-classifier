# Risk Register

| ID | Risk | Likelihood | Impact | Mitigation | Status |
|----|------|------------|--------|------------|--------|
| R-03-01 | PQClean folder naming doesn't match aliases → missed canonicalization | M | M | Expand `aliases` in `src/validate/canonical_names.yaml`; re-run ingest | Open |
| R-03-02 | `api.h` macro variance (non-integer defines) | L | M | Parser ignores non-int; add scheme-specific patches if needed | Monitoring |
| R-03-03 | Partial source drop → missing algorithms | M | M | Acceptance check compares record count vs expected sets; verify source completeness | Open |
| R-03-04 | Downstream schema drift | L | M | Keep validator in CI; fail on schema violations | Open |



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



