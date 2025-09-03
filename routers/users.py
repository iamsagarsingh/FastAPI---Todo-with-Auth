from fastapi import APIRouter, Depends, HTTPException
from database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from utils.auth_helper import get_current_user
from starlette import status
from models import Users
from schemas.user_schema import UserVerification
from passlib.context import CryptContext

router = APIRouter(
    prefix='/api/v1/users',
    tags=['users']
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

@router.get('/',status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate the user...")
    user_model = db.query(Users).filter(Users.id == user.get('user_id')).first()
    return user_model

@router.post('/password',status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency,db:db_dependency,user_verification:UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not verify the users..")
    user_model = db.query(Users).filter(Users.id == user.get('user_id')).first()
    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong password!!")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()