""" Pydantic schemas for API request and response validation """
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
 
class UserCreate(BaseModel):
    """ Validates input before insertion into Users Table """
    email: str
    password: str = Field(min_length=8)
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    """ Validates login credentials """
    email: str
    password: str

class UserResponse(BaseModel):
    """ Reads data from Users Table """
    id: int
    email: str
    first_name: str
    last_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrganizationCreate(BaseModel):
    """ Validates input before insertion into Organization Table """
    org_name: str

class OrganizationJoinRequest(BaseModel):
    """ Validates input before Updating Organization Table """
    user_id: int
    org_name: str

class OrganizationResponse(BaseModel):
    """ Read data from Organization Table """
    id: int
    org_name: str

    model_config = ConfigDict(from_attributes=True)

class RoleCreate(BaseModel):
    """ Validates input before insertion into Roles Table """
    role_name: str
    permission_level: int

class RoleUpdate(BaseModel):
    """ Validates input before Updating Roles Table """
    role_name: str | None = None
    permission_level: int | None = None

class RoleResponse(BaseModel):
    """ Reads data from Roles Table """
    id: int
    role_name: str
    permission_level: int

    model_config = ConfigDict(from_attributes=True)
class OrgMemberCreate(BaseModel):
    """ Validates input before insertion into orgMember Table """
    member_id: int
    organization_id: int
    role_id: int
    added_by: int

class OrgMemberResponse(BaseModel):
    """ Reads data from orgMember Table """
    member_id: int
    organization_id: int
    role_id: int
    added_by: int

    model_config = ConfigDict(from_attributes=True)

class ClientsCreate(BaseModel):
    """ Validate input before insertion into clients table """
    organization_id: int
    name: str
    email: str
    contact_number: str | None = None
    reliability_score: int


class ClientsUpdate(BaseModel):
    """ Validates input before updating clients Table """
    name: str | None = None
    email: str | None = None
    contact_number: str | None = None
    reliability_score: int | None = None

class ClientsResponse(BaseModel):
    """ Reads data from clients table """
    id: int
    organization_id: int
    name: str
    email: str
    contact_number: str | None
    reliability_score: int

    model_config = ConfigDict(from_attributes=True)
    

class RevenueCreate(BaseModel):
    """ Validates input before insertion into Revenue Table """
    client_id: int
    revenue_type: str
    date_expected: datetime
    amount: int

class RevenueUpdate(BaseModel):
    """ Validates input before updating Revenue Table """
    date_received: datetime | None = None
    amount: int | None = None

class RevenueResponse(BaseModel):
    """ Reads data from Revenue table """
    id: int
    client_id: int
    revenue_type: str
    date_expected: datetime
    date_received: datetime | None
    amount: int

    model_config = ConfigDict(from_attributes=True)


class ExpenseCreate(BaseModel):
    """ Validates input before insertion into Expense Table """
    organization_id: int
    urgency: str
    expense_type: str
    date: datetime
    amount: int

class ExpenseUpdate(BaseModel):
    """ Validates input before updating Expense Table """
    urgency: str | None = None
    expense_type: str | None = None
    date: datetime | None = None
    amount: int | None = None

class ExpenseResponse(BaseModel):
    """ Reads data from expense table """
    id: int
    organization_id: int
    urgency: str
    expense_type: str
    date: datetime
    amount: int

    model_config = ConfigDict(from_attributes=True)


class RiskAlertUpdate(BaseModel):
    """ Validates input before updating RiskAlerts Table """
    status: str | None = None
    resolved_at: datetime | None = None

class RiskAlertResponse(BaseModel):
    """ Reads data from Risk Alert table """
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
    """ Validates input before insertion into Financial Snapshot Table """
    organization_id: int
    snapshot_type: str

class SnapshotResponse(BaseModel):
    """ Reads data from Financial Snapshots table """
    id: int
    organization_id: int
    snapshot_date: datetime
    cash_balance: int
    snapshot_type: str
    monthly_revenue: int
    monthly_expense: int

    model_config = ConfigDict(from_attributes=True)