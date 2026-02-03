from datetime import timedelta, timezone, datetime

from fastapi import HTTPException, Security, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

import bcrypt
from jose import jwt, JWTError
from typing import Annotated, List

from app.core.config import settings

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="/login",
    # Scopes allow us to describe permissions, but simple role checks work too
    scopes={"admin": "Admin access", "user": "User access"}
)

SECRET_KEY = settings.SECRET_KEY.get_secret_value()
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(email: str, user_id: int, role: str, expires_delta: timedelta):
    """Create JWT token with user identity and role."""
    encode = {
        'sub': email,
        'id': user_id,
        'role': role
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """Decode JWT and return user info (email, id, role)."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role', 'user')

        if email is None or user_id is None:
            raise HTTPException(status_code=401, detail="User validation failed.")

        return {'email': email, 'id': user_id, 'role': role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid.")

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

# --- Role Based Access Checker ---
class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict = Depends(get_current_user)):
        if user['role'] not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Operation not permitted"
            )
        return user