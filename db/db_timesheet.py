from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from db.models import DbUser, DbTimesheet
from schemas import UserBase, TimeSheetBase


def create_timesheet(request: TimeSheetBase, current_user: DbUser, db:Session):
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