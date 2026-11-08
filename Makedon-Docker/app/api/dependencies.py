from app.services.TaskService import TaskService
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.db.session import get_db


def get_task_service(db: Session = Depends(get_db)):
    '''
    method for dep injection
    '''
    return TaskService(db)


