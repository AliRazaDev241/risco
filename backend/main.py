"""Initialized FastAPI app and includes all routers"""

from fastapi import FastAPI
from routers import (
    users,
    organizations,
)

app = FastAPI(title="RISCO")

@app.get("/")
def root():
    return {"message": "RISCO API is running"}

app.include_router(users.router)
app.include_router(organizations.router)
"""
app.include_router(clients.router)

app.include_router(roles.router)
app.include_router(organization_members.router)
app.include_router(revenue.router)
app.include_router(expenses.router)
app.include_router(risk_alerts.router)
app.include_router(financial_snapshots.router)
"""