from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from db.database import Base
from enums import UserRole


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
