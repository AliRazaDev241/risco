# Login/Register Page
 
## POST /users/
- **Usage:** Register a new user
### Request Body
```json
{
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string"
}
```
 
### Response Body
```json
{
  "id": 0,
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "created_at": "2026-04-30T16:21:27.062Z"
}
```
 
### Errors
| Code | Description |
|------|-------------|
| 400  | Email already registered |
 
---
 
## POST /users/login
- **Usage:** Log in a registered user
### Request Body
```json
{
  "email": "string",
  "password": "string"
}
```
 
### Response Body
```json
{
  "id": 0,
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "created_at": "2026-04-30T16:32:50.647Z"
}
```
 
### Errors
| Code | Description |
|------|-------------|
| 401  | Invalid email or password |
 
---
 
# Organizations Page
 
## GET /organizations/user/{user_id}
- **Usage:** Check if a user has an organization
### Parameters
| Name    | In   | Type    | Required |
|---------|------|---------|----------|
| user_id | path | integer | Yes      |
 
### Response Body
```json
{
  "id": 0,
  "org_name": "string"
}
```
 
### Errors
| Code | Description |
|------|-------------|
| 404  | Organization not found |
 
---
 
## POST /organizations/
- **Usage:** Create a new organization
### Parameters
| Name       | In    | Type    | Required |
|------------|-------|---------|----------|
| creator_id | query | integer | Yes      |
 
### Request Body
```json
{
  "org_name": "string"
}
```
 
### Response Body
```json
{
  "id": 0,
  "org_name": "string"
}
```
 
### Errors
| Code | Description |
|------|-------------|
| 400  | Organization name already taken |
 
---
 
## POST /organizations/join
- **Usage:** Join an existing organization
### Request Body
```json
{
  "user_id": 0,
  "org_name": "string"
}
```
 
### Response Body
```json
{
  "id": 0,
  "org_name": "string"
}
```
 
### Errors
| Code | Description |
|------|-------------|
| 404  | Organization does not exist |
| 403  | User is not a member of the given organization |
 
---
 
# Operations Page
 
## GET /organizations/{org_id}/members/
- **Usage:** List all members of an organization
### Parameters
| Name   | In   | Type    | Required |
|--------|------|---------|----------|
| org_id | path | integer | Yes      |
 
### Response Body
```json
[
  {
    "email": "string",
    "role_name": "string",
    "member_id": 0
  }
]
```
 
### Errors
| Code | Description |
|------|-------------|
| 500  | Failed to fetch members |
 
---
 
## POST /organizations/{org_id}/members/
- **Usage:** Add a member to an organization
- **Note:** role_name must be one of: "coowner", "stakeholder" — "owner" cannot be assigned through this endpoint
### Parameters
| Name   | In   | Type    | Required |
|--------|------|---------|----------|
| org_id | path | integer | Yes      |
 
### Request Body
```json
{
  "email": "string",
  "role_name": "string",
  "added_by": 0
}
```
 
### Errors
| Code | Description |
|------|-------------|
| 201  | Member added successfully |
| 404  | User not found |
| 409  | Member is already part of the organization |
| 500  | Failed to add member |
 
---
 
## DELETE /organizations/{org_id}/members/{member_id}
- **Usage:** Remove a member from an organization
### Parameters
| Name      | In   | Type    | Required |
|-----------|------|---------|----------|
| org_id    | path | integer | Yes      |
| member_id | path | integer | Yes      |
 
### Errors
| Code | Description |
|------|-------------|
| 200  | Member removed successfully |
| 404  | Member is not part of the organization |
| 500  | Failed to remove member |
 
---
 
## POST /clients/
- **Usage:** Add a new client to an organization
### Request Body
```json
{
  "name": "string",
  "email": "string",
  "contact_number": "string or null",
  "organization_id": 0
}
```
 
### Response Body
```json
{
  "id": 0,
  "organization_id": 0,
  "name": "string",
  "email": "string",
  "contact_number": "string or null"
}
```
 
### Notes
- `contact_number` is optional — send null if not provided
- `reliability_score` is managed internally and cannot be set on creation
### Errors
| Code | Description |
|------|-------------|
| 201  | Client added successfully |
| 409  | Client with this email already exists |
| 409  | Client with this contact number already exists |
| 404  | Organization not found |
| 500  | Failed to add client |
 
---
 
## POST /revenue/
- **Usage:** Add a revenue entry
### Request Body
```json
{
  "org_id": 0,
  "client_name": "string",
  "revenue_type": "One_Time",
  "date_expected": "2026-05-01T07:31:13.226Z",
  "date_received": "2026-05-01T07:31:13.226Z or null",
  "amount": 1
}
```
 
### Response Body
```json
{
  "id": 0,
  "client_id": 0,
  "revenue_type": "string",
  "date_expected": "2026-04-30T17:33:10.597Z",
  "date_received": "2026-04-30T17:33:10.597Z or null",
  "amount": 0
}
```
 
### Notes
- `revenue_type` must be one of: "One_Time", "Recurring"
- `date_received` is optional — send null if not yet received
- `date_received` cannot be a future date
- `amount` must be greater than 0
- `client_name` must match an existing client in the organization
### Errors
| Code | Description |
|------|-------------|
| 201  | Revenue added successfully |
| 404  | Client not found |
| 422  | Amount must be greater than 0 |
| 422  | date_received cannot be in the future |
| 500  | Failed to add revenue |
 
---
 
## POST /expenses/
- **Usage:** Add an expense entry
### Request Body
```json
{
  "organization_id": 0,
  "urgency": "Critical",
  "expense_type": "One_Time",
  "date": "2026-04-30T17:33:10.582Z",
  "amount": 1
}
```
 
### Response Body
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
 
### Notes
- `urgency` must be one of: "Critical", "Non-Critical"
- `expense_type` must be one of: "One_Time", "Recurring"
- `amount` must be greater than 0
### Errors
| Code | Description |
|------|-------------|
| 201  | Expense added successfully |
| 404  | Organization not found |
| 422  | Amount must be greater than 0 |
| 500  | Failed to add expense |
 
---
 
# Financial Intelligence Page
 
## GET /financial/intelligence
- **Usage:** Fetch key financial metrics for the Financial Intelligence Page
### Parameters
| Name   | In    | Type    | Required |
|--------|-------|---------|----------|
| org_id | query | integer | Yes      |
 
### Response Body
```json
{
  "revenue_reliability_score": 0,
  "revenue_concentration_risk": 0.5041322314049586,
  "reliable_revenue": 0,
  "total_revenue_expected": 220,
  "actual_revenue": 220
}
```
 
### Notes
- `revenue_reliability_score`: weighted average reliability (0-100), based on client reliability scores
- `revenue_concentration_risk`: HHI index (0.0-1.0), higher = more concentrated = higher risk
- `reliable_revenue`: revenue weighted by client reliability scores
- `total_revenue_expected`: sum of all expected revenue this month
- `actual_revenue`: sum of revenue with date_received set this month
### Errors
| Code | Description |
|------|-------------|
| 404  | Organization not found |
| 500  | Failed to fetch Financial Metrics |
 
---
 
## GET /revenue/
- **Usage:** List revenue entries (5 per page)
### Parameters
| Name         | In    | Type    | Required |
|--------------|-------|---------|----------|
| org_id       | query | integer | Yes      |
| revenue_type | query | string  | Yes      |
| page_no      | query | integer | Yes      |
 
### Response Body
```json
{
  "items": [
    {
      "id": 0,
      "client_name": "string",
      "client_email": "string",
      "date_expected": "2026-04-30T16:41:47.928Z",
      "date_received": "2026-04-30T16:41:47.928Z or null",
      "amount": 0
    }
  ],
  "total_pages": 0,
  "current_page": 0
}
```
 
### Errors
| Code | Description |
|------|-------------|
| 404  | Organization not found |
| 500  | Failed to fetch revenue |
 
---
 
## PATCH /revenue/{revenue_id}
- **Usage:** Update the date received for a revenue entry
### Parameters
| Name       | In   | Type    | Required |
|------------|------|---------|----------|
| revenue_id | path | integer | Yes      |
 
### Request Body
```json
{
  "date_received": "2025-04-30T14:25:41.271Z"
}
```
 
### Response Body
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
 
### Errors
| Code | Description |
|------|-------------|
| 404  | Revenue not found |
| 500  | Failed to update revenue |
 
---
 
## GET /expenses/
- **Usage:** List expense entries (5 per page)
### Parameters
| Name         | In    | Type    | Required |
|--------------|-------|---------|----------|
| org_id       | query | integer | Yes      |
| expense_type | query | string  | Yes      |
| page_no      | query | integer | Yes      |
 
### Response Body
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
 
### Errors
| Code | Description |
|------|-------------|
| 404  | Organization not found |
| 500  | Failed to fetch expenses |
 
---
 
# Dashboard Page
 
## GET /financial/dashboard
- **Usage:** Fetch key financial metrics for the Dashboard Overview
### Parameters
| Name   | In    | Type    | Required |
|--------|-------|---------|----------|
| org_id | query | integer | Yes      |
 
### Response Body
```json
{
  "cash_runway": 0.0,
  "burn_rate": 0,
  "cash_balance": 0,
  "monthly_revenue": 0,
  "headcount": 0
}
```
 
### Notes
- `cash_runway`: months of cash remaining at current burn rate. null if expenses are zero
- `burn_rate`: total expenses this month
- `cash_balance`: previous balance + monthly revenue - monthly expenses
- `monthly_revenue`: actual received revenue this month
- `headcount`: number of members in the organization
### Errors
| Code | Description |
|------|-------------|
| 404  | Organization not found |
| 500  | Failed to fetch Dashboard Metrics |
 

## POST /financial/graph
- **Usage:** Fetches time-series snapshot data for rendering a graph

### Request Body
```json
{
  "org_id": 0,
  "snapshot_type": "Base",
  "metric_type": "cash_balance",
  "start_date": "2026-05-03T10:55:55.060Z",
  "end_date": "2026-05-03T10:55:55.060Z"
}
```

### Request Fields
| Field         | Type    | Required | Allowed Values                              |
|---------------|---------|----------|---------------------------------------------|
| org_id        | integer | Yes      | —                                           |
| snapshot_type | string  | Yes      | `Base`, `Best`, `Worst`                     |
| metric_type   | string  | Yes      | `cash_balance`, `monthly_revenue`, `monthly_expense` |
| start_date    | datetime| Yes      | ISO 8601                                    |
| end_date      | datetime| Yes      | ISO 8601                                    |

### Response Body
```json
[
  {
    "snapshot_date": "2026-05-03T10:55:55.064Z",
    "value": 0
  }
]
```

### Errors
| Code | Description              |
|------|--------------------------|
| 404  | Organization not found   |
| 500  | Failed to fetch graph data |

---
 
# Clients Page
 
---
 
# Risk Alerts
 
---
 
# Role Based Access
