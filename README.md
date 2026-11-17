# ClearPay LedgerGuard | AP Control Desk

Clean deployment root for the PS-1 Finance / Accounts Payable case study.

The Docker entry point reconstructs the tested application from the ordered source bundle in `bundle/part-*.b64`. The complete editable source, tests, sample generator, synthetic data, policy notes, and demo runbook are provided separately in the project ZIP.

## What it demonstrates

- Real PDF upload, text extraction, and optional OCR fallback
- Supplier identity, invoice identity, PO status and currency checks
- Two-way unit-price and three-way goods-receipt matching
- Cumulative split-invoice controls against prior approved invoices
- Duplicate detection, tax arithmetic, evidence excerpts and confidence
- Live backend execution stages, reasoned outcomes, review queue and audit export
- Human disposition with an auditable rationale; no payment is initiated

## Demo assumptions and boundaries

All sample suppliers, invoices, purchase orders and receipts are synthetic. The 2% amount tolerance is a configurable demonstration assumption, not a Zamp policy. A match recommendation is not a payment instruction. This prototype does not connect to a live ERP, vendor master, banking or payment rail. The free Render service stores its demo history in local SQLite, which may reset if the instance is replaced. Multi-line invoice-to-PO mapping is transparently routed for human review where the single-line demo PO register cannot support a safe match.

## Run locally

Install the root `requirements.txt`, then run `uvicorn app:app --host 0.0.0.0 --port 8000`. For development and automated tests, use the full project folder in the supplied ZIP and follow its README.

## Render

Deploy this branch as a Docker web service from the root Dockerfile. The service listens on Render's `PORT`. Verify `/api/health` before the demo.

Useful routes: `/`, `/api/health`, `/api/demo/happy-path/stream`, `/api/runs`, `/api/exceptions`, `/api/purchase-orders`, `/api/export.csv`, `/docs`.
