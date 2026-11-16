from __future__ import annotations

import base64
import io
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUNDLE_PATH = ROOT / "runtime.tar.xz"
RUNTIME_DIR = Path("/tmp/clearpay-runtime")

if not (RUNTIME_DIR / "app.py").exists():
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    archive_bytes = BUNDLE_PATH.read_bytes()
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:xz") as archive:
        archive.extractall(RUNTIME_DIR)

sys.path.insert(0, str(RUNTIME_DIR))
from app import app as app  # noqa: E402,F401
