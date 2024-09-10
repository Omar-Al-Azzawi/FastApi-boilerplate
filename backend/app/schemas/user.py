from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    createdAt: datetime
    updatedAt: datetime

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
