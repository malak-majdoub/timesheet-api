from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_user
from db import db_timesheet
from db.database import get_db
from db.models import DbUser
from schemas import UserBase, TimeSheetBase,TimeSheetDisplayBase

router = APIRouter(
    prefix="/timesheet",
    tags=["Timesheet"]
)

@router.post("/",response_model= TimeSheetDisplayBase, description="create timesheet",status_code=status.HTTP_201_CREATED)
def create_timesheet(request:TimeSheetBase ,db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    return db_timesheet.create_timesheet(request, current_user, db)
