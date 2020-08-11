from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """request body schema"""
    pass


class Item(ItemBase):
    """response schema"""
    id: int
    owner_id: int

    class Config:
        orm_mode = True     # # 将告诉Pydantic模型读取数据，即使它不是dict而是ORM模型（或任何其他具有属性的任意对象）。


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    """request body schema"""
    password: str


class User(UserBase):
    """response schema"""
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True     # 将告诉Pydantic模型读取数据，即使它不是dict而是ORM模型（或任何其他具有属性的任意对象）。

