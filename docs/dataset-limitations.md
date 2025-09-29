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
