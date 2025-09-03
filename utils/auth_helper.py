from typing import Annotated
from starlette import status
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from models import Users
from datetime import timedelta, datetime, timezone

load_dotenv()

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='api/v1/auth/token')
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def authenticate_user(db,username:str,password:str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,os.getenv("SECRET_KEY"),algorithms=[os.getenv('ALGORITHM')])
        username:str = payload.get('sub')
        user_id:int = payload.get('id')
        user_role:str = payload.get('role')
        if(username is None or user_id is None):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate the user")
        return {'username':username,'user_id':user_id,'user_role':user_role}
    except JWTError:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate the user")
    
def create_access_token(username:str,user_id:str,role:str,expires_delta=timedelta):
    encode = {'sub':username,'id':user_id,'role':role}
    expires= datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,os.getenv('SECRET_KEY'),algorithm=os.getenv('ALGORITHM'))