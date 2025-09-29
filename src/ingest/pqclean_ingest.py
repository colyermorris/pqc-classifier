# src/ingest/pqclean_ingest.py
#imports
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

try:
    import yaml  # optional; only used if canonical map provided
except Exception:
    yaml = None
#/imports

#block INGEST-PQCLEAN-CLI-001
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Parse PQClean api.h trees into schema-conformant JSONL records."
    )
    p.add_argument(
        "--pqclean_root",
        type=Path,
        default=Path("data/raw/pqclean"),
        help="Root folder where PQClean repository (or subset) is placed.",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=Path("data/interim/staging/pqclean_records.jsonl"),
        help="Output JSONL path to write parsed records.",
    )
    p.add_argument(
        "--canonical",
        type=Path,
        default=Path("src/validate/canonical_names.yaml"),
        help="Optional YAML mapping to canonical algorithm names.",
    )
    return p.parse_args()
#/end of block INGEST-PQCLEAN-CLI-001

#block INGEST-PQCLEAN-UTILS-002
API_MACROS = {
    "CRYPTO_PUBLICKEYBYTES": "public_key_bytes",
    "CRYPTO_SECRETKEYBYTES": "secret_key_bytes",
    "CRYPTO_CIPHERTEXTBYTES": "ciphertext_bytes",   # KEMs
    "CRYPTO_BYTES": "signature_bytes",              # SIGs
}
API_REGEX = re.compile(r"^\s*#\s*define\s+(CRYPTO_[A-Z]+)\s+(\d+)\s*$")

def _compile_replacements(rep: Dict[str, str]):
    return [(re.compile(k), v) for k, v in rep.items()]

def _normalize_token(s: str, rules: Dict) -> str:
    t = s
    if rules.get("strip_whitespace"):
        t = t.strip()
    if rules.get("lowercase"):
        t = t.lower()
    for pat, repl in _compile_replacements(rules.get("replace", {})):
        t = pat.sub(repl, t)
    for pat, repl in rules.get("simplify", {}).items():
        t = re.sub(pat, repl, t)
    t = re.sub(r"-{2,}", "-", t) if rules.get("collapse_duplicates") else t
    if rules.get("trim_dashes"):
        t = t.strip("-")
    return t

def _build_alias_index(cfg: Dict):
    """Build lookup dicts from canonical_names.yaml."""
    norm_rules = (cfg.get("normalization") or {}).get("rules") or []
    # Squash rules into one dict for our simple normalizer
    norm = {
        "strip_whitespace": any(d.get("strip_whitespace") for d in norm_rules if isinstance(d, dict)),
        "lowercase": any(d.get("lowercase") for d in norm_rules if isinstance(d, dict)),
        "replace": {},
        "simplify": {},
        "collapse_duplicates": any(d.get("collapse_duplicates") for d in norm_rules if isinstance(d, dict)),
        "trim_dashes": any(d.get("trim_dashes") for d in norm_rules if isinstance(d, dict)),
    }
    for d in norm_rules:
        if "replace" in d:
            norm["replace"].update(d["replace"])
        if "simplify" in d:
            norm["simplify"].update(d["simplify"])

    alg_alias = {}   # alias -> canonical alg
    alg_meta  = {}   # canonical alg -> {type, family, fips}
    pset_alias = {}  # alias -> {alg, paramset, level}
    # Walk algorithms
    for a in cfg.get("algorithms", []):
        can = a.get("canonical")
        if not can:
            continue
        alg_meta[can] = {"type": a.get("type"), "family": a.get("family"), "fips": a.get("fips")}
        # include canonical name as its own alias
        for alias in set([can] + list(a.get("aliases", []))):
            key = _normalize_token(alias, norm)
            alg_alias[key] = can
        for ps in a.get("param_sets", []) or []:
            pname = ps.get("name")
            level = ps.get("level")
            # canonical paramset name acts as alias too
            for alias in set([pname] + list(ps.get("aliases", []))):
                key = _normalize_token(alias, norm)
                pset_alias[key] = {"alg": can, "paramset": pname, "level": level}
    return {"norm": norm, "alg_alias": alg_alias, "pset_alias": pset_alias, "alg_meta": alg_meta}

def load_canonical_map(path: Path):
    if not path.exists() or yaml is None:
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        return _build_alias_index(cfg)
    except Exception:
        return None

def detect_interface_and_names(api_path: Path, pqclean_root: Path) -> Tuple[str, str, str]:
    rel = api_path.relative_to(pqclean_root).parts
    iface_dir = rel[0] if len(rel) > 0 else ""
    if "crypto_kem" in iface_dir:
        interface = "KEM"
    elif "crypto_sign" in iface_dir:
        interface = "SIGN"
    else:
        interface = "UNKNOWN"
    alg = rel[1] if len(rel) > 1 else "unknown"
    paramset = alg
    return interface, alg, paramset

def parse_api_header(api_path: Path) -> Dict[str, int]:
    sizes: Dict[str, int] = {}
    try:
        with api_path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                m = API_REGEX.match(line)
                if not m:
                    continue
                macro, value = m.group(1), m.group(2)
                field = API_MACROS.get(macro)
                if field:
                    try:
                        sizes[field] = int(value)
                    except ValueError:
                        pass
    except FileNotFoundError:
        pass
    return sizes

def find_api_headers(pqclean_root: Path):
    for pattern in ("crypto_kem/*/*/api.h", "crypto_sign/*/*/api.h"):
        for p in pqclean_root.glob(pattern):
            if p.is_file():
                yield p
#/end of block INGEST-PQCLEAN-UTILS-002

#block INGEST-PQCLEAN-EMIT-003
def build_record(
    api_path: Path,
    interface: str,
    alg: str,
    paramset: str,
    sizes: Dict[str, int],
    canon_idx,
) -> Dict:
    record = {
        "source": "pqclean",
        "interface": interface,
        "algorithm": {
            "raw": alg,
            "canonical": alg,
        },
        "paramset": paramset,
        "sizes": {
            k: sizes.get(k) for k in ("public_key_bytes", "secret_key_bytes", "ciphertext_bytes", "signature_bytes")
        },
        "paths": {"api_h": str(api_path)},
        "meta": {
            "repo_root": str(api_path.parents[3]) if len(api_path.parents) >= 3 else str(api_path.parents[0]),
            "impl_dir": str(api_path.parent),
        },
    }

    # Apply canonicalization if index present
    if canon_idx:
        norm = canon_idx["norm"]
        alg_key = _normalize_token(alg, norm)
        pset_key = _normalize_token(paramset, norm)

        # First try to match param-set alias (also yields alg + level)
        pinfo = canon_idx["pset_alias"].get(pset_key)
        if pinfo:
            record["algorithm"]["canonical"] = pinfo["alg"]
            record["paramset_canonical"] = pinfo["paramset"]
            record["security_level"] = pinfo.get("level")
        # Else fall back to algorithm alias
        a_can = canon_idx["alg_alias"].get(alg_key)
        if a_can:
            record["algorithm"]["canonical"] = a_can

        # Attach meta (family/type/fips) if we know the canonical algorithm
        a_meta = canon_idx["alg_meta"].get(record["algorithm"]["canonical"])
        if a_meta:
            record["family"] = a_meta.get("family")
            record["alg_type"] = a_meta.get("type")
            if a_meta.get("fips"):
                record.setdefault("standards", {})["fips"] = a_meta["fips"]

    return record

def main() -> int:
    args = parse_args()
    pqclean_root: Path = args.pqclean_root
    out_path: Path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    canon_idx = load_canonical_map(args.canonical)

    count = 0
    with out_path.open("w", encoding="utf-8") as w:
        for api_h in find_api_headers(pqclean_root):
            interface, alg, paramset = detect_interface_and_names(api_h, pqclean_root)
            sizes = parse_api_header(api_h)
            rec = build_record(api_h, interface, alg, paramset, sizes, canon_idx)
            w.write(json.dumps(rec, separators=(",", ":")) + "\n")
            count += 1

    print(f"[OK] wrote {out_path}  (records={count})")
    return 0

if __name__ == "__main__":
    sys.exit(main())
#/end of block INGEST-PQCLEAN-EMIT-003
