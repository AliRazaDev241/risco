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
    "role_name": "string"
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

## POST /revenue/
- **Usage:** Add a revenue entry

### Request Body
```json
{
  "client_name": "string",
  "revenue_type": "One_Time",
  "date_expected": "2026-04-30T17:33:10.596Z",
  "date_received": "2026-04-30T17:33:10.596Z",
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
  "date_received": "2026-04-30T17:33:10.597Z",
  "amount": 0
}
```

### Errors
| Code | Description |
|------|-------------|
| 201  | Revenue added successfully |
| 404  | Client not found |
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

### Errors
| Code | Description |
|------|-------------|
| 201  | Expense added successfully |
| 404  | Organization not found |
| 500  | Failed to add expense |

# Financial Intelligence Page

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
      "date_received": "2026-04-30T16:41:47.928Z",
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









# Dashboard Page


# Clients Page


# Risk Alerts


# Role Based Access


## POST /users/
- Usage: 

### Parameter

### Request Body

### Response Body

### Errors
- 400: 