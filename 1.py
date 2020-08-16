from typing import List, Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl, Field

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class User(BaseModel):
    name: str = Field(..., min_length=5, max_length=32)
    password: str
    email: str = Field(..., )
    # tags: list = []
    # tags: List[str] = []    # 指定列表里面的类型
    tags: Set[str] = set()
    # avatar: Optional[Image] = None
    avatar: Optional[List[Image]] = None


class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    users: List[User]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer
