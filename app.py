from __future__ import annotations

import importlib.util
import io
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUNDLE_PATH = ROOT / "runtime.tar.xz"
RUNTIME_DIR = Path("/tmp/clearpay-runtime")

if not (RUNTIME_DIR / "app.py").exists():
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(BUNDLE_PATH.read_bytes()), mode="r:xz") as archive:
        archive.extractall(RUNTIME_DIR)

sys.path.insert(0, str(RUNTIME_DIR))
spec = importlib.util.spec_from_file_location("clearpay_runtime_app", RUNTIME_DIR / "app.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load the bundled ClearPay application module")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
app = module.app
