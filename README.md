# RISCO

A financial risk management system for Startups that face uncertainities in various forms.

---

## Overview

RISCO is a full stack financial database management system built as a student project. It allows organizations to manage their financial data across a structured hierarchy: organizations → members → clients → revenue/expenses → risk alerts → financial snapshots.

The system is designed with a **monolithic 3-tier architecture** — React frontend, FastAPI backend, and Oracle Database — with clean internal layering (routers → services → models) for high cohesion and low coupling.

---

## Tech Stack

| Layer       | Technology                                      |
|-------------|--------------------------------------------------|
| Frontend    | React *(in progress)*                           |
| Backend     | Python 3.11, FastAPI, SQLAlchemy ORM, Pydantic  |
| Database    | Oracle Database 21c Enterprise Edition          |
| Analysis    | NumPy *(planned)*, TensorFlow / Scikit-learn *(planned)* |
| Migrations  | Alembic *(planned)*                             |
| Dev Tooling | Conda, GitHub CLI                               |

---

## Architecture

```
React (Frontend)
      │
      ▼
FastAPI (Backend)
  ├── routers/       ← HTTP layer, request/response handling
  ├── services/      ← Business logic
  ├── models/        ← SQLAlchemy ORM models (database layer)
  └── schemas/       ← Pydantic schemas (API layer)
      │
      ▼
Oracle Database 21c
  └── Pluggable Database: orcl21pdb
```

---

## Features

### Completed
- [x] CLI phase (Python + PostgreSQL)
- [x] Oracle DB migration with full schema (9 tables, 1NF–4NF normalized)
- [x] SQLAlchemy ORM models for all entities
- [x] Pydantic schemas (Create / Update / Response) for all entities
- [x] FastAPI backend with router/service separation
- [x] Structured logging (`db.log`, `error.log`)

### In Progress
- [ ] Remaining routers and services
- [ ] React dashboard

### Planned
- [ ] Predictive analysis module — Base / Worst / Best case financial snapshots using NumPy and client reliability scores
- [ ] ANN model via TensorFlow or Scikit-learn (once sufficient data accumulates)
- [ ] Alembic database migrations
- [ ] GitHub Pages documentation site

---

## Prerequisites

Make sure the following are installed before setting up the project:

- [Python 3.11](https://www.python.org/downloads/)
- [Conda](https://docs.conda.io/en/latest/miniconda.html)
- [Oracle Database 21c](https://www.oracle.com/database/technologies/) (with a configured Pluggable Database)
- [Node.js](https://nodejs.org/) *(for the React frontend, once available)*
- [GitHub CLI](https://cli.github.com/) *(optional)*

> **Oracle setup note:** Ensure the Oracle listener is running and your PDB is configured to open automatically on startup. You can verify your full service name by running `lsnrctl status` in your terminal.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/AliRazaDev241/risco.git
cd risco
```

### 2. Create and activate the Conda environment

```bash
conda create -n risco python=3.11
conda activate risco
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your Oracle credentials (see [Environment Variables](#environment-variables) below).

### 5. Initialize the database

```bash
python init_db.py
```

This creates all tables in your Oracle PDB. Safe to re-run — it only creates tables that don't already exist.

### 6. Start the development server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```env
DB_HOST=localhost
DB_PORT=1521
DB_SERVICE_NAME=orclpdb.bbrouter   # Verify with: lsnrctl status
DB_USER=risco
DB_PASSWORD=your_password_here
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.
---
 
## Project Structure
 
```
risco/
├── backend/
│   ├── routers/             # FastAPI route handlers
│   ├── services/            # Business logic
│   ├── testing/             # Test suite
│   ├── documentation/       # Backend docs
│   ├── logs/                # Runtime log files (db.log, error.log)
│   ├── main.py              # FastAPI app entry point
│   ├── db.py                # Oracle DB connection & session management
│   ├── init_db.py           # Table creation script
│   ├── logger.py            # Structured logging setup
│   ├── models.py            # SQLAlchemy ORM models (all 9 tables)
│   ├── schema.py            # Pydantic schemas (all entities)
│   ├── seed.py              # Database seeding script
│   └── api.md               # API reference notes
│
├── risco-fronntend/         # React frontend (Vite + Tailwind)
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── login.jsx
│   │   │   ├── OrgSelect.jsx
│   │   │   └── Register.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── package.json
│
├── .env                     # Backend environment variables
├── db.env                   # Database-specific environment variables
└── .gitignore
```
 
---


## API Documentation

Once the server is running, interactive API docs are available automatically via FastAPI:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Database Schema

The schema covers 9 tables normalized to 4NF:

| Table                  | Description                                      |
|------------------------|--------------------------------------------------|
| `Users`                | System users with authentication info            |
| `Organization`         | Top-level organizational entities                |
| `Roles`                | Roles within an organization                     |
| `OrganizationMembers`  | Users linked to organizations with roles         |
| `Clients`              | Clients belonging to an organization             |
| `Revenue`              | Revenue records linked to clients                |
| `Expenses`             | Expense records linked to organizations          |
| `RiskAlerts`           | Alerts generated based on financial thresholds   |
| `FinancialSnapshots`   | Periodic financial summaries (Base/Worst/Best)   |

---

## License

This project is for academic purposes. All rights reserved.