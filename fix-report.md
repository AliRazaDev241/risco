# HIGHER-RISK CALLOUTS
- **Refactor Snapshot page logic**: The logic was deeply flawed, not just mis-categorizing expenses but also failing to properly carry forward the cash balance logic. I had to rip out the manual `cash_balance = monthly_revenue - monthly_expenses` for non-Base snapshots and replace it with a shared carry-forward logic using the previous Base snapshot balance.
- **Refactor Financial Metrics Logic**: Fetching metrics from raw tables was replaced completely by fetching the latest Base financial snapshot. This is a significant logic shift but aligns the dashboard perfectly with the snapshots and resolves the wrong cash balance type bug simultaneously.

# Bug Report Fixes

## Refactor Snapshot page logic (Critical)
- **Files changed**: `backend/services/snapshots.py`
- **What changed and why**: `_upsert_best` now queries for 'Critical' expenses instead of 'Non-Critical' to actually reflect the minimum viable expenses in a best-case scenario. Additionally, `_upsert_snapshot` now correctly calculates the current cash balance by taking the previous month's `Base` cash balance and applying the current month's revenue/expenses, completely discarding the incorrect logic that simply did `revenue - expenses` for Best and Worst snapshots.
- **Frontend changes**: None needed.
- **Confidence**: HIGH

## Missing reliability_score on client creation (High)
- **Files changed**: `backend/services/clients.py`
- **What changed and why**: Added `reliability_score=100` to the `Clients` constructor during client creation. This provides a default value to satisfy the database `NOT NULL` constraint and prevents the crash upon client insertion.
- **Frontend changes**: None needed (the frontend sends `null`, which the backend now safely defaults during instantiation).
- **Confidence**: HIGH

## Add Revenue bug (High)
- **Files changed**: `backend/schema.py`, `backend/services/revenue.py`, `frontend/src/pages/Operations.jsx`
- **What changed and why**: Updated `schema.RevenueCreate` to expect `client_email` instead of `client_name`. Modified `add_revenue` to query the `clients` table by `email` and `organization_id` instead of `name`, preventing conflicts when multiple clients share the same name.
- **Frontend changes**: Updated the Add Revenue form in `Operations.jsx` to render a "Client Email" input instead of "Client Name", and updated the API payload to send `client_email` accordingly.
- **Confidence**: HIGH

## cash_balance resets negative balances to monthly net (High)
- **Files changed**: `backend/services/calculations.py`
- **What changed and why**: Removed the `cash_balance_previous >= 0` check when carrying forward the previous balance. It now uses the actual previous cash balance even if it is negative, accurately reflecting accumulated debt.
- **Frontend changes**: None needed.
- **Confidence**: HIGH

## Dashboard cash balance fetches wrong snapshot type (High) & Refactor Financial Metrics Logic (Medium)
- **Files changed**: `backend/services/financial.py`
- **What changed and why**: Addressed both issues simultaneously by replacing the raw SQL sums in `get_dashboard_metrics` with a single query fetching the latest `Base` snapshot from `financial_snapshots`. This provides `monthly_revenue`, `monthly_expense`, and `cash_balance` directly. This eliminates duplicated calculation logic and automatically guarantees the cash balance is correctly scoped to the `Base` snapshot.
- **Frontend changes**: None needed.
- **Confidence**: MEDIUM (The refactor replaces the entire metric calculation, which guarantees consistency but relies on `refresh_or_create` being called to keep snapshots up to date).
