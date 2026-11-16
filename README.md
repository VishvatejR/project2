# ClearPay | Invoice-to-PO Decision Desk

A runnable case-study application for PS-1: Finance / Accounts Payable invoice processing.

## Live application

After the Render build completes, use the service URL shown in the Render Dashboard.

- Health: `/api/health`
- API documentation: `/docs`
- Dashboard: `/`

## Features

- PDF invoice upload and text extraction
- Optional Gemini structured extraction for fields the local parser misses
- Deterministic purchase-order matching and policy checks
- Duplicate invoice detection
- Vendor, currency, PO approval, and amount-tolerance validation
- Human-review outcome with rationale
- Real backend execution stages streamed as Server-Sent Events
- Audit history and CSV export
- Five synthetic test scenarios

## Deployment configuration

Render build command: `pip install -r requirements.txt`

Render start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

The root entry point extracts `runtime.tar.xz` to `/tmp/clearpay-runtime` and imports the FastAPI application. This keeps deployment deterministic while preserving the full Python application and frontend inside the archive.

## Local development

The complete editable source project, test suite, sample PDFs, and documentation are in the accompanying ClearPay case-study ZIP. Run it from that extracted project using:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8000
```

## Important boundaries

All sample data is synthetic. An `APPROVED` outcome is a recommendation for normal Accounts Payable review, not a payment instruction. The application does not connect to a real ERP, vendor master, or payment rail. A 2% amount tolerance is a configurable demonstration assumption, not a Zamp policy.
