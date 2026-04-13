# RISCO DBMS (Outdated Read Me)

A CLI-based financial management system for organizations to track revenue, expenses, clients, and risk alerts. Built with Python and PostgreSQL, designed to be upgraded to a FastAPI + Flutter full-stack application.

---

## Tech Stack
- Python 3.11
- PostgreSQL
- psycopg2 — PostgreSQL driver
- tabulate — CLI table formatting
- python-dotenv — environment variable management

---

## Project Structure

### Root
| File | Purpose |
|------|---------|
| `db.py` | PostgreSQL connection. Single source for all database access. |
| `models.py` | Dataclasses mirroring database tables. Used by services to return structured data instead of raw tuples. |
| `requirements.txt` | All Python dependencies. |
| `.env` | Database credentials. Never committed to git. |

---

### `services/`
Business logic and all database queries. No printing, no input, no menus — just functions that talk to the database. When migrating to FastAPI, these files are reused directly as the API layer.

| File | Purpose |
|------|---------|
| `auth.py` | User registration, login, and password hashing. |
| `organizations.py` | Creating and retrieving organizations. |
| `members.py` | Adding and listing organization members and their roles. |
| `clients.py` | Adding and listing clients. |
| `revenue.py` | Adding revenue records. Calculates MRR, reliable revenue, and top client dependency. |
| `expenses.py` | Adding expense records. Calculates burn rate and critical vs non-critical breakdown. |
| `risk_alerts.py` | Fetching risk alerts filtered by type and status. |
| `snapshots.py` | Generating base, best, and worst case financial snapshots. |
| `overview.py` | Calculating cash runway, headcount, and cash balance for the dashboard. |

---

### `cli/`
Presentation layer. Handles all menus, user input, and output formatting. Calls services for all data operations. Replaced by FastAPI routes and Flutter UI in the full-stack version.

| File | Purpose |
|------|---------|
| `main.py` | Entry point. Launches the authentication menu. |

#### `cli/menus/`
Each file corresponds to one screen in the application.

| File | Purpose |
|------|---------|
| `auth.py` | Register, login, and exit menu. |
| `dashboard.py` | Main dashboard. Displays cash balance, burn rate, runway, and risk alerts on entry. |
| `expenses.py` | Expense Intelligence screen. Shows burn rate, critical breakdown, and expense risk alerts. |
| `revenue.py` | Revenue Intelligence screen. Shows MRR, client reliability, dependency percentage, and revenue risk alerts. |

#### `cli/menus/operations/`
Operations submenu for all data entry and management actions.

| File | Purpose |
|------|---------|
| `main.py` | Operations submenu entry point. |
| `members.py` | Add and view organization members. |
| `clients.py` | Add and view clients. |
| `revenue_entry.py` | Form to record a new revenue entry. |
| `expense_entry.py` | Form to record a new expense entry. |

#### `cli/utils/`
Shared utilities used across all menus.

| File | Purpose |
|------|---------|
| `display.py` | Tabulate wrappers for consistent table formatting and ASCII graphs. |
| `prompts.py` | Input helpers with validation for emails, amounts, dates, and other common fields. |
| `session.py` | Stores the logged-in user and organization in memory. Read by menus and services to avoid passing IDs as parameters everywhere. |
| `logger.py` | Centralized logging setup. All modules import the logger from here. |

---

### `logs/`
Application logs generated at runtime. Not committed to git.

| File | Purpose |
|------|---------|
| `app.log` | Generated automatically on first run. Records info, warnings, and errors. |

---

## Setup

1. Clone the repository
2. Create and activate the conda environment
```bash
conda create -n riscoCLI python=3.11
conda activate riscoCLI
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python cli/main.py
```

---

## Architecture Notes
- Services are completely decoupled from the CLI layer. When migrating to FastAPI, services are reused directly as route handlers.
- Models are dataclasses — easily converted to Pydantic models for FastAPI with minimal changes.
- Session state is held in memory during the CLI session. Replaced by JWT tokens in the full-stack version.
```

---

### `.gitignore`
```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Environment
.env
.env.*

# Logs
logs/*.log

# Conda / virtualenv
env/
venv/
.conda/

# IDEs
.vscode/
.idea/
*.suo
*.user

# OS
.DS_Store
Thumbs.db
desktop.ini

# Distribution
dist/
build/
*.egg-info/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Database
*.sql
*.dump