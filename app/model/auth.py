from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET_KEY = "010bbe14f0d1bc8d0fadbe8ed3f1190da1eac6f3eedf90eb245f9462edd035e9"
ALGORITHM = "H256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None

class UserInDB(User):
    hashed_password: str