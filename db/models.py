from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum, DateTime,UniqueConstraint
from sqlalchemy.orm import relationship
from db.database import Base
from enums import UserRole, TimesheetStatus


class DbUser(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    manager_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    # Self-referential relationship
    manager = relationship("DbUser", remote_side=[id], backref="team_members")
    
    # Relationships
    timesheet_entries = relationship("DbTimesheetEntry", back_populates="employee", cascade="all, delete-orphan")
    timesheet = relationship("DbTimesheet", foreign_keys="DbTimesheet.employee_id",back_populates="employee",cascade="all, delete-orphan")
    reviewed_timesheet = relationship("DbTimesheet", foreign_keys="DbTimesheet.reviewed_by",back_populates="reviewer",cascade="all, delete-orphan")


class DbProject(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    # Relationships
    timesheet_entries = relationship("DbTimesheetEntry", back_populates="project")


class DbTimesheetEntry(Base):
    __tablename__ = 'timesheet_entries'
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    date = Column(Date, nullable=False)
    hours = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    
    # Relationships
    employee = relationship("DbUser", back_populates="timesheet_entries")
    project = relationship("DbProject", back_populates="timesheet_entries")

class DbTimesheet(Base):
    __tablename__ = 'timesheets'
    id = Column(Integer, primary_key=True, index=True)
    week_number = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(Enum(TimesheetStatus), default=TimesheetStatus.DRAFT, nullable=False)
    rejection_comment = Column(String, nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    reviewed_by = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), nullable=True)
    employee_id=Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), nullable=False)

    #Relations
    employee = relationship("DbUser", foreign_keys=[employee_id], back_populates="timesheet")
    reviewer = relationship("DbUser", foreign_keys=[reviewed_by], back_populates="reviewed_timesheet")

    #Constraints
    __table_args__ = (
        UniqueConstraint('employee_id', 'week_number', 'year', name='unique_employee_week_timesheet'),
    )
