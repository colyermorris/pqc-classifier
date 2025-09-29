#block WP01-VALIDATE-003
# src/validate/validators.py
# Purpose: Public API stubs to load the record JSON Schema and validate a record dict.

from typing import Dict, Any, Tuple

def load_schema() -> Dict[str, Any]:
    """Return the loaded JSON Schema for a PQC record."""
    raise NotImplementedError

def validate_record(record: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate a single record dict against the schema; return (ok, message)."""
    raise NotImplementedError
#/end of block WP01-VALIDATE-003
