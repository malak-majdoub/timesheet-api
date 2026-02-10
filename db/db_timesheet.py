from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from db.models import DbUser, DbTimesheet, DbTimesheetEntry
from enums import TimesheetStatus
from schemas import UserBase, TimeSheetBase, TimesheetEntryCreate


def create_timesheet(request: TimesheetEntryCreate, current_user: DbUser, db:Session):
    new_timesheet = DbTimesheet (
        employee_id = current_user.id,
        week_number = request.week_number,
        year = request.year
    )
    try:
        db.add(new_timesheet)
        db.commit()
        db.refresh(new_timesheet)
        return new_timesheet
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code= 409, detail="Timesheet already exists")

def submit_timesheet(timesheet_id:int, current_user:DbUser, db:Session):
    timesheet = db.query(DbTimesheet).filter(DbTimesheet.id == timesheet_id).first()
    if not timesheet:
        raise HTTPException(status_code= 404, detail="Timesheet not found")
    if timesheet.employee_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your timesheet")
    if timesheet.status != TimesheetStatus.DRAFT:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Status is not DRAFT(already submitted/approved")
    timesheet_entry = db.query(DbTimesheetEntry).filter(DbTimesheetEntry.timesheet_id == timesheet_id).all()
    if len(timesheet_entry) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No entries in this timesheet")
    updated_timesheet = {
        "status" :TimesheetStatus.SUBMITTED,
        "submitted_at": datetime.now(),
    }
    db.query(DbTimesheet).filter(DbTimesheet.id == timesheet_id).update(updated_timesheet)
    db.commit()
    submited_timesheet = db.query(DbTimesheet).filter(DbTimesheet.id == timesheet_id).first()
    return {
        "id": submited_timesheet.id,
        "employee_id": submited_timesheet.employee_id,
        "week_number": submited_timesheet.week_number,
        "year": submited_timesheet.year,
        "status": submited_timesheet.status,
        "submitted_at": submited_timesheet.submitted_at,
        "entries_count": len(timesheet_entry)
    }
