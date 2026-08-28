"""Project configuration.

Centralizes paths and settings so notebooks and scripts read from one place.
Paths resolve against the project root (derived from this file's location) and can
be overridden with environment variables set in a local `.env`.
"""

import os
from pathlib import Path

# Project root = one level up from src/.
ROOT = Path(__file__).resolve().parent.parent


def _path(env_name, default):
    """Return a project-root-relative path, overridable via an environment variable."""
    value = os.getenv(env_name, default)
    p = Path(value)
    if not p.is_absolute():
        p = ROOT / p
    return p


DATA_DIR_RAW = _path("DATA_DIR_RAW", "data/raw")
DATA_DIR_PROCESSED = _path("DATA_DIR_PROCESSED", "data/processed")
MODEL_DIR = _path("MODEL_DIR", "model")
REPORTS_DIR = _path("REPORTS_DIR", "reports")
DOCS_DIR = _path("DOCS_DIR", "docs")

# Reproducibility seed used for data generation and resampling.
RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))


def ensure_dirs():
    """Create the standard data / model / reports / docs directories if missing."""
    for d in (DATA_DIR_RAW, DATA_DIR_PROCESSED, MODEL_DIR, REPORTS_DIR, DOCS_DIR):
        d.mkdir(parents=True, exist_ok=True)
    return True
