22 findings: 1 Critical, 9 High, 4 Medium, 8 Low; 1 of 19 open GitHub issues confirmed stale/misunderstanding

## Organizations

### [SEVERITY: Medium] — Organization Joining Router Bugged
- **Source:** GitHub issue #2 (valid)
- **Location:** `backend/routers/organization_members.py`, `add_member` and Frontend Onboarding Page
- **What's wrong:** `add_member` eagerly inserts users directly into `organization_members`. This eager insertion bypasses the frontend's specific onboarding "Join Organization" page, rendering that UI flow completely useless.
- **Why it matters:** The system's architectural flow is short-circuited. Users are forced into an organization without explicitly accepting an invitation via the intended onboarding UI.
- **Proposed fix:** Change `add_member` to generate and store a secure invite code in the database instead of eager insertion. The member then inputs this code on the "Join Organization" page to officially join.

### [SEVERITY: Low] — Currency Table Missing
- **Source:** GitHub issue #5 (valid)
- **Location:** `backend/models.py`, `Organization` model
- **What's wrong:** The `Organization` table lacks a `currency` column to specify the organization's base currency.
- **Why it matters:** Future AI models or multi-national organizations will have unstandardized financial data.
- **Proposed fix:** Add `currency = Column(String(10), default="USD")` to the `Organization` model.

### [SEVERITY: Low] — Add Notifications Table
- **Source:** GitHub issue #10 (valid)
- **Location:** `backend/models.py`
- **What's wrong:** There is no schema or logic for a notifications system.
- **Why it matters:** Users won't know when they are added to organizations or when important events happen.
- **Proposed fix:** Create a `Notifications` SQLAlchemy model.

### [SEVERITY: Low] — Display Currency and Org Name on Pages
- **Source:** GitHub issue #12 (valid)
- **Location:** Frontend UI
- **What's wrong:** The frontend does not currently retrieve or display the organization currency/name globally.
- **Why it matters:** Users might lose context on which organization they are currently viewing.
- **Proposed fix:** Add UI elements in the frontend dashboard layout to render this context.

### [SEVERITY: High] — Role Based Access Control Missing
- **Source:** GitHub issue #15 (valid)
- **Location:** `backend/models.py` and all routers
- **What's wrong:** Although the `Roles` table has a `permission_level`, no endpoints actually enforce it via dependencies.
- **Why it matters:** Any user in the organization can access any endpoint, leading to privilege escalation.
- **Proposed fix:** Implement a FastAPI dependency (e.g. `require_permission(level)`) and attach it to sensitive routers.

### [SEVERITY: High] — Access Control Bug lets you remove yourself
- **Source:** GitHub issue #19 (valid)
- **Location:** `backend/routers/organization_members.py`, `remove_member`
- **What's wrong:** The `remove_member` endpoint accepts an `org_id` and `member_id` but does not prevent the caller from removing themselves, nor does it enforce owner-only permissions.
- **Why it matters:** An owner can accidentally orphan an organization by removing themselves.
- **Proposed fix:** Add a check `if current_user.id == member_id: raise HTTPException(...)` and enforce owner role.

## Users

### [SEVERITY: Low] — Forgot Password and Remember Me Option
- **Source:** GitHub issue #13 (valid)
- **Location:** `backend/routers/auth.py`
- **What's wrong:** No endpoints exist for password reset flows.
- **Why it matters:** Users who forget passwords are locked out permanently.
- **Proposed fix:** Implement `/forgot-password` and `/reset-password` endpoints.

## Clients


### [SEVERITY: Medium] — Add Client Page Routers
- **Source:** GitHub issue #8 (valid)
- **Location:** `backend/routers/clients.py`
- **What's wrong:** The client router only contains a POST endpoint. It lacks GET, DELETE, and heatmap data aggregation.
- **Why it matters:** Users cannot view or manage clients once created.
- **Proposed fix:** Add `GET /clients/`, `DELETE /clients/{id}`, and heatmap analytics endpoints.

## Revenue


### [SEVERITY: Medium] — Revenue and Expenses Data Type
- **Source:** GitHub issue #17 (valid)
- **Location:** `backend/models.py`, `Revenue` and `Expenses` models
- **What's wrong:** `amount` columns are defined as `Integer`.
- **Why it matters:** Financial calculations lose cents/decimals accuracy.
- **Proposed fix:** Change `Integer` to `Float` or `Numeric` for monetary columns.

## Expenses

### [SEVERITY: High] — Recurring Payment isn't recurring
- **Source:** GitHub issue #3 (valid)
- **Location:** `backend/main.py`
- **What's wrong:** Revenue and expenses have `revenue_type = 'Recurring'`, but there is no scheduled background task to automatically generate the subsequent month's entries.
- **Why it matters:** Expected recurring financials are missing from future calculations unless manually duplicated.
- **Proposed fix:** Implement a daily/monthly background job to copy recurring entries into the new month.

## FinancialSnapshots


### [SEVERITY: High] — Background and Scheduled Tasks
- **Source:** GitHub issue #9 (valid)
- **Location:** `backend/main.py`
- **What's wrong:** Financial snapshots and scores are only computed when triggered by an active request. There are no cron/scheduled jobs to compute these overnight.
- **Why it matters:** Data might be stale if no user has visited the dashboard or triggered an update recently.
- **Proposed fix:** Use a library like APScheduler to trigger snapshot refreshes periodically.

### [SEVERITY: Low] — Graph render message missing
- **Source:** GitHub issue #20 (valid)
- **Location:** Frontend UI
- **What's wrong:** When the API returns no graph data, the UI displays a generic error instead of a friendly empty state.
- **Why it matters:** Poor user experience for brand new organizations.
- **Proposed fix:** Handle empty arrays gracefully in the frontend chart component.

## Financial Intelligence


## Predictions

### [SEVERITY: Low] — Add Predictions Table
- **Source:** GitHub issue #11 (valid)
- **Location:** `backend/models.py`
- **What's wrong:** The described AI predictions table does not exist.
- **Why it matters:** Feature is missing.
- **Proposed fix:** Implement the `Predictions` model as outlined in the issue.

## Others / General

### [SEVERITY: Low] — Comment Code thoroughly
- **Source:** GitHub issue #14 (valid)
- **Location:** Repository-wide
- **What's wrong:** The codebase lacks sufficient docstrings for pylint compliance.
- **Why it matters:** Technical debt and harder maintainability.
- **Proposed fix:** Add module, class, and function docstrings everywhere.

### [SEVERITY: Low] — Data Population
- **Source:** GitHub issue #16 (valid)
- **Location:** Repository-wide
- **What's wrong:** No script to seed large amounts of sample data.
- **Why it matters:** Difficult for developers to test scale and AI features.
- **Proposed fix:** Create a robust faker seed script.

### [SEVERITY: Medium] — Risk Alerts
- **Source:** GitHub issue #18 (valid)
- **Location:** `backend/models.py` and `backend/main.py`
- **What's wrong:** The `RiskAlerts` table exists, but there is no background logic evaluating revenue/expenses to actually generate the alerts.
- **Why it matters:** The risk alerts feature is non-functional.
- **Proposed fix:** Add a background worker that scans for unpaid past-due revenue or critical expenses and inserts records into `RiskAlerts`.
