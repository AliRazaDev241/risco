# Product Requirements Document (Current State)

## Core Problem Solved
RISCO helps startups and SMBs track cash flow, burn rate, cash runway, client concentration risk (HHI), and revenue reliability without requiring complex, enterprise-level accounting tools. It abstracts financial modeling into an accessible dashboard that automatically calculates risk factors based on revenue and expense logging.

## What a User Can Actually Accomplish Today

As of the current implementation, a user can accomplish the following end-to-end flows:

### 1. Account & Organization Management
- **Registration and Login**: Users can create an account and authenticate using an email and password.
- **Organization Creation**: Users can create a new organization workspace.
- **Joining Organizations**: Users can join an existing organization if they know the organization name and are permitted (though current API permits joining if the user ID and org name match the join request).
- **Member Management**: Users can add other members to their organization and assign them roles (e.g., `"coowner"`, `"stakeholder"`), as well as remove members.

### 2. Client & Cash Flow Tracking
- **Client Roster**: Users can add clients with their contact details to an organization to track where revenue is coming from.
- **Revenue Logging**: Users can log expected or received revenue (one-time or recurring) tied to specific clients. They can update a revenue entry when payment is actually received.
- **Expense Logging**: Users can log critical and non-critical expenses (one-time or recurring).

### 3. Financial Intelligence & Reporting
- **Dashboard Overview**: Users can view a dashboard that calculates real-time `cash_runway` (months left at current burn), `burn_rate` (total monthly expenses), `monthly_revenue` (revenue strictly received this month), and a running `cash_balance` that carries forward.
- **Risk Metrics**: Users can view intelligent financial metrics:
  - **Revenue Concentration Risk**: Calculated via the Herfindahl-Hirschman Index (HHI) to show if the business is dangerously reliant on a single client.
  - **Revenue Reliability Score**: A weighted average score of how reliable clients are at paying on time.
  - **Reliable Revenue**: Expected revenue adjusted by the reliability of the clients producing it.
- **Financial Snapshots & Graphs**: The system automatically generates and upserts monthly Base/Best/Worst case snapshots every time revenue or expenses are modified. Users can request time-series graph data for these snapshots across specific date ranges to visualize their `cash_balance`, `monthly_revenue`, or `monthly_expense` trends.

## Not Yet Implemented (Stubbed or Planned Features)

The following features exist in documentation or as database schemas, but are **not yet implemented or enforced** in the actual codebase:

- **JWT Authentication & Token Sessions**: While login works and validates passwords, the system does not yet issue JWTs or maintain token-based sessions. The API does not enforce bearer token auth.
- **RBAC Enforcement**: The database contains a `Roles` table with varied permission levels, and users can be assigned roles. However, the API does not currently read a user's token to enforce Role-Based Access Control on specific actions (e.g., any client can theoretically hit the API to add a member if they construct the request payload).
- **Predictions (ANN-based forecasting)**: The predictive analysis module for generating Base/Worst/Best case financial forecasts using Artificial Neural Networks (ANNs) is purely a stub. Snapshot data is currently saved but not meaningfully forecasted by an AI model.
- **Integrations**: There are no third-party integrations (e.g., Stripe, Plaid, QuickBooks). All revenue and expense data must be entered and updated manually via the endpoints.
- **Risk Alerts**: The database schema supports `RiskAlerts`, but there are no API routers, endpoints, or background tasks implemented to generate or resolve these alerts.
