from fastapi import Depends, APIRouter, HTTPException
from database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from schemas.auth_schema import CreateUserRequest
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token_schema import Token
from utils.auth_helper import authenticate_user, create_access_token
from datetime import timedelta

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['auth']
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

@router.post('/',status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,user_request:CreateUserRequest):
    user_model = Users(
        username=user_request.username,
        email=user_request.email,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        hashed_password= bcrypt_context.hash(user_request.password),
        role= user_request.role,
        is_active= True
    )
    db.add(user_model)
    db.commit()


@router.post('/token',response_model=Token)
async def login_for_access_token(db:db_dependency,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    user = authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate the user...")
    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=20))
    return {'access_token':token,'token_type':'bearer'}