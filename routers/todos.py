from fastapi import APIRouter, Depends, HTTPException, Path
from database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from schemas.todos_schema import TodoRequest
from starlette import status

router = APIRouter(
    prefix='/api/v1',
    tags=['todos']
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        

db_dependency = Annotated[Session,Depends(get_db)]

@router.get('/')
async def read_all(db:db_dependency):
    todos = db.query(Todos).all()
    return todos

@router.post('/todo',status_code=status.HTTP_201_CREATED)
async def create_Todo(db:db_dependency,todo_request:TodoRequest):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()

@router.put('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency,todo_request:TodoRequest,todo_id:int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Todo not found to update.")
    for key,value in todo_request.model_dump().items():
        setattr(todo_model,key,value)
    db.add(todo_model)
    db.commit()

@router.delete('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency,todo_id:int):
    try:
        db.query(Todos).filter(Todos.id == todo_id).delete()
        db.commit()
    except:
        raise HTTPException(status_code=404,detail="Todo not found to delete")