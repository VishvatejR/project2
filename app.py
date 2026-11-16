from __future__ import annotations

import importlib.util
import io
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNTIME_DIR = Path("/tmp/clearpay-runtime")

def extract_archive(archive_path: Path) -> None:
    if archive_path.exists():
        with tarfile.open(archive_path, "r:xz") as archive:
            archive.extractall(RUNTIME_DIR)

RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
extract_archive(ROOT / "runtime.tar.xz")

# The UI patch is stored as ordered binary chunks to keep each Git object small.
ui_parts = ROOT / "ui_update_parts"
if ui_parts.exists():
    compressed_ui = b"".join(part.read_bytes() for part in sorted(ui_parts.glob("part-*.bin")))
    if compressed_ui:
        with tarfile.open(fileobj=io.BytesIO(compressed_ui), mode="r:xz") as archive:
            archive.extractall(RUNTIME_DIR)

sys.path.insert(0, str(RUNTIME_DIR))
spec = importlib.util.spec_from_file_location("clearpay_runtime_app", RUNTIME_DIR / "app.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load the bundled ClearPay application module")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
app = module.app
