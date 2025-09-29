# Dataset Limitations

This document captures the current limitations of datasets used in the pqc-classifier project and defines a plan to expand post-training. These constraints must be revisited and updated as the project matures.

## Current Limitations

### 1. Sample Size
- Our current dataset is limited to a small collection of PQC algorithm families and parameter sets.  
- Coverage is narrow: primarily test vectors and metadata from PQClean and OQS.  
- Insufficient to fully represent the diversity of production deployments.

### 2. Benchmark Bias
- Most data comes from published benchmarks, which may not reflect real-world workloads.  
- Vendor-tuned or research-oriented benchmarks can overestimate or underestimate performance.  
- Risk: models may learn biases in benchmark conventions instead of true algorithm characteristics.

### 3. Missing Dynamic Features
- Current features focus on **static sizes** (key, ciphertext, signature).  
- Lacking **runtime/operational signals** such as CPU usage, memory footprint, latency, or network overhead.  
- These dynamic features are critical for classification accuracy in practical environments.

### 4. Environment Diversity
- Present data sources are primarily Linux-based and academic libraries.  
- Missing variations across compilers, hardware architectures, and deployment contexts (e.g., cloud, mobile, embedded).  
- Without environment diversity, generalization may fail when models encounter new settings.

### 5. Refresh & Update Plan
- Datasets will be refreshed quarterly to include:  
  - Newly standardized NIST PQC algorithms.  
  - Expanded runtime metrics from multiple platforms (CPU/GPU/ARM).  
  - Industry-provided anonymized datasets (subject to governance).  
- A standing task will validate dataset health against these goals.

---

## Next Actions
- Capture initial benchmarks and document provenance.  
- Begin work to integrate dynamic performance logs.  
- Track new NIST releases and update quarterly.  


## Notes
- Current dataset consists of a toy example only; not representative of real-world measurements.  
- Sizes/timings are illustrative placeholders and should not be used for benchmarking or modeling.

## Aliasing & Canonical Naming (WP-02)

**Why this matters.** Our sources (NIST docs, liboqs/PQClean repos, vendor SDKs, scraped tables) use inconsistent labels for the *same* algorithms, parameter sets, families, and security levels. Without a canonical map, joins are lossy and features fragment (e.g., `Kyber768` vs `ML-KEM-768`).

**What we standardized.**
- **Canonical algorithm names:** Follow current NIST/FIPS nomenclature where available (e.g., **ML-KEM**, **ML-DSA**, **SLH-DSA**). Falcon, Classic McEliece, BIKE, and HQC retain common names.
- **Families:** `{lattice, code, hash}` with liberal alias coverage (e.g., `ring-lwe`, `module-lwe` → **lattice**).
- **Security levels:** Canonical levels `{1, 3, 5}` with aliases (`L1`, `cat5`, `nist-3`, etc.).
- **Parameter sets:** Mapped to levels (e.g., `ML-KEM-768` → level 3; `Falcon-1024` → level 5).

**Normalization rules.** We apply case-folding, space/underscore → hyphen, `+` → `plus`, and simplifications like removing `crystals-` and collapsing duplicate separators. See `src/validate/canonical_names.yaml#normalization`.

### Alias Coverage (snapshot)
The table below summarizes current alias breadth (counts approximate; wildcard families, e.g., `oqs_*`, may resolve to multiple tokens at runtime).

| Canonical           | Type       | Family  | Param Sets (→ Level)                                 | Alias Count* |
|--------------------|------------|---------|------------------------------------------------------|--------------|
| ML-KEM             | KEM        | lattice | 512→1, 768→3, 1024→5                                 | 20+          |
| FrodoKEM           | KEM        | lattice | 640→1, 976→3, 1344→5                                 | 10+          |
| SABER              | KEM        | lattice | Light→1, Saber→3, Fire→5                             | 6+           |
| NTRU               | KEM        | lattice | HPS/HRSS variants                                    | 6+           |
| NTRU Prime         | KEM        | lattice | sntrup761 (typical)                                  | 5+           |
| NewHope            | KEM        | lattice | 512/1024-CCA                                         | 4+           |
| ML-DSA             | Signature  | lattice | 44→1, 65→3, 87→5                                     | 12+          |
| Falcon             | Signature  | lattice | 512→1, 1024→5                                        | 8+           |
| SLH-DSA            | Signature  | hash    | SHA2-{128,192,256}{f,s} etc.                         | 12+          |
| Classic McEliece   | KEM        | code    | 348864/460896/6688128/6960119/8192128 (+f variants)  | 16+          |
| BIKE               | KEM        | code    | L1→1, L3→3, L5→5                                     | 6+           |
| HQC                | KEM        | code    | 128→1, 192→3, 256→5                                  | 6+           |
| **Families (alias buckets)** | — | — | lattice/code/hash alias groups                        | 10+          |
| **Security levels (alias buckets)** | — | — | {1,3,5} alias lists                                  | 24+          |

\*Alias Count includes parameter-set and library tokens; exact total will depend on runtime wildcard expansion (e.g., `oqs_*`, `pqclean-*`).

**Limitations & assumptions.**
- Some ecosystems (OpenSSL forks, vendor SDKs) invent transient labels; we normalize common cases but expect stragglers.
- SPHINCS\+ variants (SHAKE, Haraka) are folded under **SLH-DSA**; we treat the SHA2 family as representative examples for now.
- Deprecated/broken submissions (e.g., **SIKE**, **Rainbow**) are retained in a `deprecated` sink to avoid misclassification during ingestion of legacy tables.

**Next steps.**
- Add automated alias discovery: harvest tokens from headers/README of liboqs/PQClean at pin commits; unit-test that all tokens map to a canonical label.
- Surface an “alias resolution report” in the ETL logs: unmapped tokens flagged with source file and first-seen line number.

# Dataset Limitations (WP-03 scope)

- **Source coverage**: Only algorithms present in the dropped PQClean subtree are ingested. If a family/param-set is absent upstream, it will be absent here.
- **Heuristic param-set naming**: We infer `paramset` from the `<alg>` directory (e.g., `kyber1024`). Ambiguous layouts may require alias additions.
- **Macro dependence**: Size fields come from `api.h` macros (`CRYPTO_PUBLICKEYBYTES`, etc.). Non-standard headers or computed macros will be skipped.
- **Canonical mapping incompleteness**: If an alias isn’t listed, canonical fields (`paramset_canonical`, `security_level`) can be missing until the map is updated.
