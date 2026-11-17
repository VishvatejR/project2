from __future__ import annotations

import base64
import importlib.util
import io
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "runtime"

if not (RUNTIME / "app.py").exists():
    encoded = "".join(
        part.read_text(encoding="ascii").strip()
        for part in sorted((ROOT / "bundle").glob("part-*.b64"))
    )
    payload = base64.b64decode(encoded, validate=True)
    RUNTIME.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:xz") as archive:
        archive.extractall(RUNTIME)

(RUNTIME / "samples").mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(RUNTIME))
spec = importlib.util.spec_from_file_location("ledgerguard_runtime_app", RUNTIME / "app.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load ClearPay LedgerGuard runtime")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
app = module.app
