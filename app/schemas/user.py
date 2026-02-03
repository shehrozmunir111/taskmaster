from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from email_validator import validate_email, EmailNotValidError

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

    @field_validator("email")
    @classmethod
    def validate_real_email(cls, v):
        try:
            # check_deliverability=True ensures the domain actually exists and has MX records
            v = validate_email(v, check_deliverability=True).normalized
            return v
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {str(e)}")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    role: str

    class Config:
        from_attributes = True # SQLAlchemy object → JSON

class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str
    full_name: str