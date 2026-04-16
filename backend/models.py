""" ORM Models - each class maps to a database table in the schema via SQL Alchemy"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    CheckConstraint,
    ForeignKey,
)
from db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        """Defines how the class represents itself when printed"""
        return f"<User {self.first_name} {self.last_name}>"


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    org_name = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Organization {self.org_name}>"


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role_name = Column(String(50), unique=True, nullable=False)
    permission_level = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("permission_level IN (1, 2, 3)", name="chk_permission_level"),
    )

    def __repr__(self):
        return f"<Role {self.role_name} Permission {self.permission_level}>"


class OrganizationMembers(Base):
    __tablename__ = "organization_members"

    member_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    added_by = Column(Integer, ForeignKey("users.id"), nullable=False)


class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contact_number = Column(String(20), unique=True, nullable=True)
    reliability_score = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("reliability_score BETWEEN 1 AND 100", name="chk_reliability_score"),
        )

    def __repr__(self):
        return f"<Client {self.name}>"


class Revenue(Base):
    __tablename__ = "revenue"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    revenue_type = Column(String(20), nullable=False)
    date_expected = Column(DateTime, nullable=False)
    date_received = Column(DateTime, nullable=True)
    amount = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "revenue_type IN ('One_Time', 'Recurring')", name="chk_revenue_type"
        ),
        CheckConstraint("amount > 0", name="chk_revenue_amount"),
    )

    def __repr__(self):
        return f"<Revenue {self.amount}>"


class Expenses(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    urgency = Column(String(20), nullable=False)
    expense_type = Column(String(20), nullable=False)
    date = Column(DateTime, nullable=False)
    amount = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "expense_type IN ('One_Time', 'Recurring')", name="chk_expense_type"
        ),
        CheckConstraint(
            "urgency IN ('Critical', 'Non-Critical')", name="chk_urgency"
        ),
        CheckConstraint("amount > 0", name="chk_expense_amount"),
    )

    def __repr__(self):
        return f"<Expense {self.amount}>"


class RiskAlerts(Base):
    __tablename__ = "risk_alerts"

    id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=True)
    revenue_id = Column(Integer, ForeignKey("revenue.id"), nullable=True)
    urgency_level = Column(Integer, nullable=False)
    status = Column(String(20), default="Open", nullable=False)
    description = Column(String(255), nullable=True)
    deadline = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    resolved_at = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint("urgency_level BETWEEN 1 AND 3", name="chk_urgency_level"),
        CheckConstraint("status IN ('Open', 'Resolved', 'Ignored')", name="chk_status"),
        CheckConstraint(
            "(expense_id IS NULL) <> (revenue_id IS NULL)", name="chk_one_source"
        ),
    )

    def __repr__(self):
        return f"<RiskAlert {self.urgency_level} {self.status} {self.description}>"


class FinancialSnapshots(Base): 
    __tablename__ = "financial_snapshots"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    snapshot_date = Column(DateTime, server_default=func.now(), nullable=False)
    cash_balance = Column(Integer, default=0, nullable=False)
    snapshot_type = Column(String(20), default="Base", nullable=False)
    monthly_revenue = Column(Integer, nullable=False)
    monthly_expense = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("snapshot_type IN ('Base', 'Best', 'Worst')", name="chk_snapshot_type"),
        CheckConstraint("monthly_revenue >= 0", name="chk_monthly_revenue"),
        CheckConstraint("monthly_expense >= 0", name="chk_monthly_expenses"),
    )

    def __repr__(self):
        return f"<Balance {self.cash_balance} Revenue {self.monthly_revenue} Expense {self.monthly_expense}>"
