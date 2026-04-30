"""Pydantic schemas for API request and response validation"""

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime, timezone


class UserCreate(BaseModel):
    """Validates input before insertion into Users Table"""

    email: str
    password: str = Field(min_length=8)
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    """Validates login credentials"""

    email: str
    password: str


class UserResponse(BaseModel):
    """Reads data from Users Table"""

    id: int
    email: str
    first_name: str
    last_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrganizationCreate(BaseModel):
    """Validates input before insertion into Organization Table"""

    org_name: str


class OrganizationJoinRequest(BaseModel):
    """Validates input before Updating Organization Table"""

    user_id: int
    org_name: str


class OrganizationResponse(BaseModel):
    """Read data from Organization Table"""

    id: int
    org_name: str

    model_config = ConfigDict(from_attributes=True)


class AddMemberRequest(BaseModel):
    email: str
    role_name: str
    added_by: int


class UpdateRoleRequest(BaseModel):
    role_id: int


class RoleCreate(BaseModel):
    role_name: Literal["Owner", "Co_Owner", "Stakeholder"]
    permission_level: Literal[1, 2, 3]


class RoleResponse(BaseModel):
    """Reads data from Roles Table"""

    id: int
    role_name: str
    permission_level: int

    model_config = ConfigDict(from_attributes=True)


class OrgMemberResponse(BaseModel):
    """Reads data from orgMember  Table"""

    member_id: int
    organization_id: int
    role_id: int
    added_by: int

    model_config = ConfigDict(from_attributes=True)


class ClientsCreate(BaseModel):
    """Validate input before insertion into clients table"""

    organization_id: int
    name: str
    email: str
    contact_number: str | None = None
    reliability_score: int

class ClientsResponse(BaseModel):
    """Reads data from clients table"""

    id: int
    organization_id: int
    name: str
    email: str
    contact_number: str | None
    reliability_score: int

    model_config = ConfigDict(from_attributes=True)

class RevenueCreate(BaseModel):
    client_name: str  # lookup by name instead of raw FK
    revenue_type: Literal["One_Time", "Recurring"]
    date_expected: datetime
    date_received: datetime | None = None
    amount: int = Field(gt=0)

class RevenueUpdate(BaseModel):
    """Validates input before updating Revenue Table"""

    date_received: datetime | None = None
    
    @field_validator("date_received")
    @classmethod
    def must_not_be_future(cls, v):
        if v is None:
            return v
        if v > datetime.now(timezone.utc):
            raise ValueError("date_received cannot be in the future")
        return v

class RevenueResponse(BaseModel):
    """Reads data from Revenue table"""

    id: int
    client_id: int
    revenue_type: str
    date_expected: datetime
    date_received: datetime | None
    amount: int

    model_config = ConfigDict(from_attributes=True)

class RevenueListItem(BaseModel):
    id: int
    client_name: str
    client_email: str
    date_expected: datetime
    date_received: datetime | None
    amount: int

    model_config = ConfigDict(from_attributes=True)

class RevenuePage(BaseModel):
    items: list[RevenueListItem]
    total_pages: int
    current_page: int

class ExpenseCreate(BaseModel):
    organization_id: int
    urgency: Literal["Critical", "Non-Critical"]
    expense_type: Literal["One_Time", "Recurring"]
    date: datetime
    amount: int = Field(gt=0)


class ExpenseUpdate(BaseModel):
    """Validates input before updating Expense Table"""

    urgency: str | None = None
    expense_type: str | None = None
    date: datetime | None = None
    amount: int | None = None


class ExpenseResponse(BaseModel):
    """Reads data from expense table"""

    id: int
    organization_id: int
    urgency: str
    expense_type: str
    date: datetime
    amount: int

    model_config = ConfigDict(from_attributes=True)

class ExpenseListItem(BaseModel):
    urgency: str
    expense_type: str
    date: datetime
    amount: int
    model_config = ConfigDict(from_attributes=True)

class ExpensePage(BaseModel):
    items: list[ExpenseListItem]
    total_pages: int
    current_page: int

class RiskAlertUpdate(BaseModel):
    """Validates input before updating RiskAlerts Table"""

    status: str | None = None
    resolved_at: datetime | None = None


class RiskAlertResponse(BaseModel):
    """Reads data from Risk Alert table"""

    id: int
    expense_id: int | None
    revenue_id: int | None
    urgency_level: int
    status: str
    description: str | None
    deadline: datetime
    created_at: datetime
    resolved_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class SnapshotCreate(BaseModel):
    organization_id: int
    snapshot_type: Literal["Base", "Best", "Worst"]


class SnapshotResponse(BaseModel):
    """Reads data from Financial Snapshots table"""

    id: int
    organization_id: int
    snapshot_date: datetime
    cash_balance: int
    snapshot_type: str
    monthly_revenue: int
    monthly_expense: int

    model_config = ConfigDict(from_attributes=True)
