from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PainBase(BaseModel):
    title: str
    description: str

class PainCreate(PainBase):
    pass

class Pain(PainBase):
    id: int
    created_at: datetime
    user_id: int
    votes_count: Optional[int] = 0
    model_config = ConfigDict(from_attributes=True)

class VoteBase(BaseModel):
    pain_id: int

class Vote(VoteBase):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

       