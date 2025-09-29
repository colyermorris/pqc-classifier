# Risk Register

| ID | Risk | Likelihood | Impact | Owner | Mitigation | Status |
|----|------|------------|--------|-------|------------|--------|
| R1 | Dataset too small or biased | Medium | High | Data Lead | Expand sources; quarterly refresh | Open |
| R2 | Misclassification in new environments | Medium | Medium | Model Lead | Robustness tests; calibration | Open |
| R3 | Secrets committed by mistake | Low | High | Dev Lead | .gitignore; pre-push checks | Open |
| R4 | Dependency or build breakage | Medium | Medium | Eng | Pin versions; CI checks | Open |



- Risk: Upstream sources may change license terms or disappear.  
  Mitigation: Store license tags, citations, and checksums; keep link-only locators for proprietary data.