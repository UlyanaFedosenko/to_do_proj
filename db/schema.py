from pydantic import BaseModel, constr
from typing import Optional


class UserBase(BaseModel):
    first_name: str
    last_name: Optional[str]
    username: str
    password: constr(min_length=6)


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str]
    status: str
    user_id: int


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
