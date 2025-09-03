from fastapi import APIRouter, Depends, HTTPException
from database import sessionLocal
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated
from utils.auth_helper import get_current_user
from models import Todos

router = APIRouter(
    prefix='/api/v1/admin',
    tags=['admin']
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get('/todo',status_code=status.HTTP_200_OK)
async def real_all(db:db_dependency,user:user_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Could not validate user or user is not admin.")
    todos = db.query(Todos).all()
    return todos

@router.delete('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency,user:user_dependency,todo_id:int):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Could not validate user or user is not admin.")
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo not found..")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()