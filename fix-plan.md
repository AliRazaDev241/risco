# Fix Plan

## Critical
1. **Refactor Snapshot page logic** - Update `_upsert_best` and `_upsert_worst` in `backend/services/snapshots.py` to properly categorize expenses and carry forward previous cash balance.

## High
2. **Missing reliability_score on client creation** - Provide a default `reliability_score=100` during client creation in `backend/services/clients.py`.
3. **Add Revenue bug** - Update the client query in `backend/services/revenue.py` to filter by `email` instead of `name` to prevent collisions.
4. **cash_balance resets negative balances to monthly net** - Remove the `cash_balance_previous >= 0` constraint in `backend/services/calculations.py` to allow negative balances to carry forward.
5. **Dashboard cash balance fetches wrong snapshot type** - Add `snapshot_type = 'Base'` filter when fetching `prev_balance` in `backend/services/financial.py`.

## Medium
6. **Refactor Financial Metrics Logic** - Modify `get_dashboard_metrics` in `backend/services/financial.py` to query `financial_snapshots` instead of aggregating raw revenue/expenses tables.

## Low
(No findings in `backend/services/` for this severity)
