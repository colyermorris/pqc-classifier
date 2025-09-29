# src/validate/validate_pqclean_records.py
#imports
import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple
#/imports

#block VALIDATE-PQCLEAN-CLI-001
def parse_args():
    p = argparse.ArgumentParser(description="Validate pqclean_records.jsonl schema and basic consistency.")
    p.add_argument(
        "--infile",
        type=Path,
        default=Path("data/interim/staging/pqclean_records.jsonl"),
        help="Path to JSONL from the PQClean ingester.",
    )
    return p.parse_args()
#/end of block VALIDATE-PQCLEAN-CLI-001

#block VALIDATE-PQCLEAN-CHECKS-002
REQUIRED_TOP = ["source", "interface", "algorithm", "paramset", "sizes", "paths"]
REQUIRED_ALG = ["raw", "canonical"]
REQUIRED_SIZES_ANY = ["public_key_bytes", "secret_key_bytes"]  # always present
KEM_ONLY = "ciphertext_bytes"
SIGN_ONLY = "signature_bytes"

def _is_intlike(v):
    return isinstance(v, int) and v >= 0

def validate_record(rec: Dict) -> List[str]:
    errs: List[str] = []

    # required top-level fields
    for k in REQUIRED_TOP:
        if k not in rec:
            errs.append(f"missing field: {k}")

    # algorithm subfields
    alg = rec.get("algorithm", {})
    for k in REQUIRED_ALG:
        if k not in alg or not isinstance(alg.get(k), str) or not alg.get(k):
            errs.append(f"algorithm.{k} missing/empty")

    # sizes present and int-like
    sizes = rec.get("sizes", {})
    for k in REQUIRED_SIZES_ANY:
        if not _is_intlike(sizes.get(k)):
            errs.append(f"sizes.{k} missing/not-int")

    iface = rec.get("interface")
    # KEM vs SIGN consistency
    if iface == "KEM":
        if not _is_intlike(sizes.get(KEM_ONLY)):
            errs.append(f"sizes.{KEM_ONLY} missing/not-int for KEM")
        if sizes.get(SIGN_ONLY) is not None:
            errs.append(f"sizes.{SIGN_ONLY} should be absent for KEM")
    elif iface == "SIGN":
        if not _is_intlike(sizes.get(SIGN_ONLY)):
            errs.append(f"sizes.{SIGN_ONLY} missing/not-int for SIGN")
        if sizes.get(KEM_ONLY) is not None:
            errs.append(f"sizes.{KEM_ONLY} should be absent for SIGN")
    else:
        errs.append("interface must be KEM or SIGN")

    # optional canonical enrichments, if present, should be sane
    sl = rec.get("security_level")
    if sl is not None and sl not in (1, 3, 5):
        errs.append("security_level must be 1, 3, or 5 if present")

    fam = rec.get("family")
    if fam is not None and fam not in ("lattice", "code", "hash"):
        errs.append("family (if present) must be lattice|code|hash")

    return errs
#/end of block VALIDATE-PQCLEAN-CHECKS-002

#block VALIDATE-PQCLEAN-MAIN-003
def main() -> int:
    args = parse_args()
    infile: Path = args.infile

    if not infile.exists():
        print(f"[ERROR] Input not found: {infile}")
        return 2

    errors: List[Tuple[int, List[str]]] = []
    count = 0
    with infile.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception as e:
                errors.append((i, [f"invalid JSON: {e}"]))
                continue
            count += 1
            errs = validate_record(rec)
            if errs:
                errors.append((i, errs))

    if errors:
        print(f"[FAIL] {len(errors)} invalid record(s) out of {count}. Showing first 20:")
        for i, (lineno, errs) in enumerate(errors[:20], start=1):
            print(f"  #{i} @line {lineno}:")
            for e in errs:
                print(f"    - {e}")
        return 1

    print(f"[OK] Validation passed: {count} records")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
#/end of block VALIDATE-PQCLEAN-MAIN-003
