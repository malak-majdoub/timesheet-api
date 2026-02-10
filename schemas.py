from pydantic import BaseModel, EmailStr, ConfigDict,Field
from datetime import date
from enums import UserRole, TimesheetStatus
from typing import Optional
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.EMPLOYEE
    manager_id: Optional[int] = None


class UserCreate(UserBase):
    password: str


class UserDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: str
    role: UserRole
    manager_id: Optional[int]


class UserAuth(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole


# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    description: Optional[str]


# Timesheet Entry schemas
class TimesheetEntryBase(BaseModel):
    project_id: int
    date: date
    hours: float
    description: Optional[str] = None


class TimesheetEntryCreate(TimesheetEntryBase):
    timesheet_id: int


class TimesheetEntryUpdate(BaseModel):
    project_id: Optional[int] = None
    date: Optional[date] = None
    hours: Optional[float] = None
    description: Optional[str] = None


class TimesheetEntryDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    employee_id: int
    project_id: int
    date: date
    hours: float
    description: Optional[str]

class TimeSheetBase(BaseModel):
    week_number: int = Field(..., ge = 1, le = 53)
    year: int= Field(..., ge = 2020, le = 2030)

class TimeSheetDisplayBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    week_number: int
    year: int
    employee_id: int
    status: TimesheetStatus

class TimeSheetSubmitDisplayBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    week_number: int
    year: int
    status: TimesheetStatus
    submitted_at: datetime
    entries_count: int
