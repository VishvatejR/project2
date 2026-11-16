from __future__ import annotations

import base64
import importlib.util
import io
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNTIME_DIR = Path("/tmp/clearpay-runtime")
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

# Extract the complete application bundle first.
with tarfile.open(ROOT / "runtime.tar.xz", mode="r:xz") as archive:
    archive.extractall(RUNTIME_DIR)

# Apply the redesigned static UI as a small overlay, leaving business logic untouched.
parts_dir = ROOT / "ui_update_parts"
encoded_overlay = "".join(
    part.read_text(encoding="ascii").strip()
    for part in sorted(parts_dir.glob("part-*.b64"))
)
overlay_bytes = base64.b64decode(encoded_overlay, validate=True)
with tarfile.open(fileobj=io.BytesIO(overlay_bytes), mode="r:xz") as archive:
    archive.extractall(RUNTIME_DIR)

sys.path.insert(0, str(RUNTIME_DIR))
spec = importlib.util.spec_from_file_location("clearpay_runtime_app", RUNTIME_DIR / "app.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load the bundled ClearPay application module")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
app = module.app
