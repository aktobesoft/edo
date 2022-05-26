from typing import Union
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from catalogs.user.models import User
from core.db import database

auth_Router = APIRouter()

SECRET_KEY = "uYE4XB2Sex8S754LTtLPKIcNhoLgcRzwKVmPyT1tNKQbJYNP3iSGkP1hXe5QKFww"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[str, None] = None
    username: Union[str, None] = None

class UserModel(BaseModel):
    id: Union[int, None] = 0
    username: Union[str, None] = None
    email: Union[str, None] = None
    is_active: Union[bool, None] = None

class UserInDB(UserModel):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user(email: str)->UserModel:
    query = select(User.email, User.name.label('username'), User.is_active.label('is_active'), User.id, User.hashed_password).where((User.email == email) | (User.name == email))
    result = await database.fetch_one(query)
    if result == None:
        return result
    return dict(result)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        if username is None:
            raise credentials_exception
        token_data = TokenData(email = email, username = username)
    except JWTError:
        raise credentials_exception
    user = await get_user(email = token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if not current_user['is_active']:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@auth_Router.post("/token", response_model=Token, tags=["login for access token"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user['username'], "email": user['email']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}#, "username": user['username'], "email": user['email']}

async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if user is None or not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return user