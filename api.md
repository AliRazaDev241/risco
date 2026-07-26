# Drift Log: API.md vs. Current Codebase

Before presenting the corrected API documentation, here is a record of every place the previous `api.md` doc was wrong, missing, or stale compared to the actual codebase:

1. **Endpoint Path Mismatch for Graphs**: 
   - `api.md` listed `POST /financial/graph`. 
   - **Code**: The endpoint is actually implemented as `POST /snapshots/graph` (defined in `routers/snapshots.py` which mounts with the `/snapshots` prefix).
2. **Role Naming / Casing Inconsistency**:
   - `api.md` stated `role_name` must be one of `"coowner", "stakeholder"`. 
   - **Code**: There's internal drift here. `schema.RoleCreate` expects `"Owner", "Co_Owner", "Stakeholder"`. However, `services/organization_members.py` strictly checks against `ASSIGNABLE_ROLES = {"coowner", "stakeholder"}`. The old API doc accurately reflected the service logic, but contradicted the Pydantic schema validation. We document the service requirement here.
3. **Empty Sections**:
   - `api.md` contained empty headers for `# Clients Page`, `# Risk Alerts`, and `# Role Based Access`. 
   - **Code**: This is technically accurate because there are no GET endpoints for clients, and no router files/endpoints for risk alerts or RBAC management. The code only contains schemas for risk alerts, but no actual API endpoints exist.
4. **Error Message Wording**:
   - `api.md` for `POST /organizations/join` listed a 403 error description as "User is not a member of the given organization".
   - **Code**: The actual error returned is `"You have not been added to this organization, contact your admin"`.

---

# Corrected API Documentation

> **Note on Authentication:**
> JWT/RBAC is planned but **NOT YET IMPLEMENTED**. None of the endpoints currently validate a Bearer token or enforce RBAC permissions from a token context. Authorization relies entirely on explicit parameters (like `creator_id` or `added_by` in the request body).

## Users

### POST /users/
- **Usage:** Register a new user
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Request Body:**
```json
{
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string"
}
```
- **Response Body:**
```json
{
  "id": 0,
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "created_at": "2026-04-30T16:21:27.062Z"
}
```
- **Errors:**
  - `400`: Email already registered

### POST /users/login
- **Usage:** Log in a registered user
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```
- **Response Body:**
```json
{
  "id": 0,
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "created_at": "2026-04-30T16:32:50.647Z"
}
```
- **Errors:**
  - `401`: Invalid email or password

---

## Organizations

### GET /organizations/user/{user_id}
- **Usage:** Check if a user has an organization
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Parameters:**
  - `user_id` (path, integer)
- **Response Body:**
```json
{
  "id": 0,
  "org_name": "string"
}
```
- **Errors:**
  - `404`: No organization found

### POST /organizations/
- **Usage:** Create a new organization
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Parameters:**
  - `creator_id` (query, integer)
- **Request Body:**
```json
{
  "org_name": "string"
}
```
- **Response Body:**
```json
{
  "id": 0,
  "org_name": "string"
}
```
- **Errors:**
  - `400`: Organization name already taken

### POST /organizations/join
- **Usage:** Join an existing organization
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Request Body:**
```json
{
  "user_id": 0,
  "org_name": "string"
}
```
- **Response Body:**
```json
{
  "id": 0,
  "org_name": "string"
}
```
- **Errors:**
  - `404`: Organization does not exist
  - `403`: You have not been added to this organization, contact your admin

---

## Organization Members

### GET /organizations/{org_id}/members/
- **Usage:** List all members of an organization
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Parameters:**
  - `org_id` (path, integer)
- **Response Body:**
```json
[
  {
    "email": "string",
    "role_name": "string",
    "member_id": 0
  }
]
```
- **Errors:**
  - `500`: Failed to fetch members

### POST /organizations/{org_id}/members/
- **Usage:** Add a member to an organization
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Note:** `role_name` must be one of `"coowner"`, `"stakeholder"` based on service-level assignment limits. `"owner"` cannot be assigned here.
- **Parameters:**
  - `org_id` (path, integer)
- **Request Body:**
```json
{
  "email": "string",
  "role_name": "string",
  "added_by": 0
}
```
- **Response (201 Created):**
```json
{
  "detail": "user@example.com added successfully as coowner"
}
```
- **Errors:**
  - `404`: User not found or No role found
  - `409`: Member is already part of the organization (or invalid assignable role)
  - `500`: Failed to add member

### DELETE /organizations/{org_id}/members/{member_id}
- **Usage:** Remove a member from an organization
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Parameters:**
  - `org_id` (path, integer)
  - `member_id` (path, integer)
- **Errors:**
  - `200`: Member removed successfully
  - `404`: Member is not part of the organization
  - `500`: Failed to remove member

---

## Clients

### POST /clients/
- **Usage:** Add a new client to an organization
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Request Body:**
```json
{
  "name": "string",
  "email": "string",
  "contact_number": "string",
  "organization_id": 0
}
```
- **Response Body (201 Created):**
```json
{
  "id": 0,
  "organization_id": 0,
  "name": "string",
  "email": "string",
  "contact_number": "string"
}
```
- **Notes:**
  - `contact_number` is optional (can be null).
  - `reliability_score` is managed internally and cannot be set on creation.
- **Errors:**
  - `409`: Client with this email already exists OR Client with this contact number already exists
  - `404`: Organization not found
  - `500`: Failed to add client

---

## Revenue

### POST /revenue/
- **Usage:** Add a revenue entry
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Request Body:**
```json
{
  "org_id": 0,
  "client_name": "string",
  "revenue_type": "One_Time",
  "date_expected": "2026-05-01T07:31:13.226Z",
  "date_received": "2026-05-01T07:31:13.226Z",
  "amount": 1
}
```
- **Response Body (201 Created):**
```json
{
  "id": 0,
  "client_id": 0,
  "revenue_type": "string",
  "date_expected": "2026-04-30T17:33:10.597Z",
  "date_received": "2026-04-30T17:33:10.597Z",
  "amount": 0
}
```
- **Notes:**
  - `revenue_type` must be `"One_Time"` or `"Recurring"`.
  - `date_received` is optional (null if not yet received).
  - `date_received` cannot be a future date (returns 422 if so).
  - `amount` must be > 0.
- **Errors:**
  - `404`: Client not found
  - `422`: Amount must be greater than 0 / date_received cannot be in the future
  - `500`: Failed to add revenue

### GET /revenue/
- **Usage:** List revenue entries (paginated, 5 per page)
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Parameters:**
  - `org_id` (query, integer)
  - `revenue_type` (query, string)
  - `page_no` (query, integer)
- **Response Body:**
```json
{
  "items": [
    {
      "id": 0,
      "client_name": "string",
      "client_email": "string",
      "date_expected": "2026-04-30T16:41:47.928Z",
      "date_received": "2026-04-30T16:41:47.928Z",
      "amount": 0
    }
  ],
  "total_pages": 0,
  "current_page": 0
}
```
- **Errors:**
  - `404`: Organization not found
  - `500`: Failed to fetch revenue

### PATCH /revenue/{revenue_id}
- **Usage:** Update the date received for a revenue entry
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Parameters:**
  - `revenue_id` (path, integer)
- **Request Body:**
```json
{
  "date_received": "2025-04-30T14:25:41.271Z"
}
```
- **Response Body:**
```json
{
  "id": 22,
  "client_id": 23,
  "revenue_type": "Recurring",
  "date_expected": "2026-04-30T12:28:57",
  "date_received": "2025-04-30T14:25:41",
  "amount": 10000
}
```
- **Errors:**
  - `404`: Revenue not found
  - `500`: Failed to update revenue

---

## Expenses

### POST /expenses/
- **Usage:** Add an expense entry
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Request Body:**
```json
{
  "organization_id": 0,
  "urgency": "Critical",
  "expense_type": "One_Time",
  "date": "2026-04-30T17:33:10.582Z",
  "amount": 1
}
```
- **Response Body (201 Created):**
```json
{
  "id": 0,
  "organization_id": 0,
  "urgency": "string",
  "expense_type": "string",
  "date": "2026-04-30T17:33:10.606Z",
  "amount": 0
}
```
- **Notes:**
  - `urgency` must be `"Critical"` or `"Non-Critical"`.
  - `expense_type` must be `"One_Time"` or `"Recurring"`.
  - `amount` must be > 0.
- **Errors:**
  - `404`: Organization not found
  - `422`: Amount must be greater than 0
  - `500`: Failed to add expense

### GET /expenses/
- **Usage:** List expense entries (paginated, 5 per page)
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Parameters:**
  - `org_id` (query, integer)
  - `expense_type` (query, string)
  - `page_no` (query, integer)
- **Response Body:**
```json
{
  "items": [
    {
      "urgency": "string",
      "expense_type": "string",
      "date": "2026-04-30T16:48:18.289Z",
      "amount": 0
    }
  ],
  "total_pages": 0,
  "current_page": 0
}
```
- **Errors:**
  - `404`: Organization not found
  - `500`: Failed to fetch expenses

---

## Financial Intelligence

### GET /financial/intelligence
- **Usage:** Fetch key financial metrics for the Financial Intelligence Page
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Parameters:**
  - `org_id` (query, integer)
- **Response Body:**
```json
{
  "revenue_reliability_score": 0,
  "revenue_concentration_risk": 0.5041322314049586,
  "reliable_revenue": 0,
  "total_revenue_expected": 220,
  "actual_revenue": 220
}
```
- **Notes:**
  - `revenue_reliability_score`: weighted average reliability (0-100), based on client reliability scores
  - `revenue_concentration_risk`: HHI index (0.0-1.0), higher = more concentrated = higher risk
  - `reliable_revenue`: revenue weighted by client reliability scores
  - `total_revenue_expected`: sum of all expected revenue this month
  - `actual_revenue`: sum of revenue with `date_received` set this month
- **Errors:**
  - `404`: Organization not found
  - `500`: Failed to fetch intelligence metrics

### GET /financial/dashboard
- **Usage:** Fetch key financial metrics for the Dashboard Overview
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Parameters:**
  - `org_id` (query, integer)
- **Response Body:**
```json
{
  "cash_runway": 0.0,
  "burn_rate": 0,
  "cash_balance": 0,
  "monthly_revenue": 0,
  "headcount": 0
}
```
- **Notes:**
  - `cash_runway`: months of cash remaining at current burn rate. null if expenses are zero.
  - `burn_rate`: total expenses this month.
  - `cash_balance`: previous balance + monthly revenue - monthly expenses.
  - `monthly_revenue`: actual received revenue this month.
  - `headcount`: number of members in the organization.
- **Errors:**
  - `404`: Organization not found
  - `500`: Failed to fetch Dashboard Metrics

---

## Snapshots (Graph)

### POST /snapshots/graph
- **Usage:** Fetches time-series snapshot data for rendering a graph
- **Auth:** Not enforced (JWT/RBAC planned but NOT YET IMPLEMENTED)
- **Request Body:**
```json
{
  "org_id": 0,
  "snapshot_type": "Base",
  "metric_type": "cash_balance",
  "start_date": "2026-05-03T10:55:55.060Z",
  "end_date": "2026-05-03T10:55:55.060Z"
}
```
- **Request Fields:**
  - `snapshot_type`: `Base`, `Best`, `Worst`
  - `metric_type`: `cash_balance`, `monthly_revenue`, `monthly_expense`
- **Response Body:**
```json
{
  "date_range_start": "2026-01-01T00:00:00.000Z",
  "date_range_end": "2026-05-03T00:00:00.000Z",
  "data": [
    {
      "snapshot_date": "2026-05-03T10:55:55.064Z",
      "value": 0
    }
  ]
}
```
- **Notes:**
  - `date_range_start` / `date_range_end`: bounds for snapshot data available for this org and snapshot type.
  - `data`: filtered results within the requested date range.
- **Errors:**
  - `404`: Organization not found
  - `500`: Failed to fetch Graph Data
