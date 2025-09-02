from fastapi import Depends, APIRouter
from database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from schemas.auth_schema import CreateUserRequest
from models import Users
from passlib.context import CryptContext

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