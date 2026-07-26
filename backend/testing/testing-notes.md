## Location
`backend/services/revenue.py` -> `add_revenue` and `update_revenue`

## What's hard to test
Testing that "a revenue write with date_received set should trigger both reliability scoring AND a snapshot upsert" (checkpoint priority 2) is impossible within the scope of testing the `services` module.

## Why
The side-effects (triggering `client_service.update_reliability_score` and `snapshot_service.refresh_or_create`) are implemented in `backend/coordinators/revenue_coordinator.py`. The `services/revenue.py` functions themselves only execute the DB inserts/updates and do not invoke any coordinators or other services. Therefore, a unit test covering `services/revenue.py` can only verify the row is written, but cannot mock or assert against the coordinator, as the dependency flows the other way (coordinator -> service).

## Proposed refactor
If the intent is for the service layer to handle its own side-effects directly, the side-effect logic should be moved from `coordinators/revenue_coordinator.py` into `services/revenue.py`. Alternatively, if the current architecture (coordinator orchestrating services) is preferred, unit tests verifying these side-effects should be placed in a `test_revenue_coordinator.py` file testing the `coordinators/` folder, rather than `backend/testing/test_revenue.py`.
