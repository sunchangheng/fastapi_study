#!./usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2020-07-20
# Author: Jimmy
"""
运行：uvicorn main:app --reload
"""
import random
from datetime import datetime, timedelta, time
from enum import Enum
from typing import Optional, List, Set, Dict
from uuid import UUID, uuid1

from fastapi import FastAPI, Body, Query, Path, Cookie
from pydantic import Field, HttpUrl, BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float = 88
    is_offer: bool = False


def get_random():
    """10秒之后获取一个随机数"""
    time.sleep(10)
    return random.randint(1, 100)


@app.get("/")
async def read_root():
    """根目录"""
    print('根目录')
    r_data = 55

    return {"Hello": "World", 'r_data': r_data}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    """获取一个Item"""
    return {"item_id": item_id, "q": q}


"""
使用BaseModel的数据转换
"""


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    print('item_id', item_id)
    print('获取到的item', item)

    data = {"item_name": item.name, "item_id": item_id}
    return data


"""
顺序很重要
/users/me
/users/{user_id}
当path前缀一样时，路径匹配时会按照写顺序优先匹配
"""


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


"""
使用枚举类，做类型的切换。并且会有一个好的前端接口显示。
"""


@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


"""
当后端想要接收一个完整的文件路径时，前端需要加个`\`转移`\`
"""


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "tiger"}, {"item_name": "pig"}, {"item_name": "fox"}]


@app.get("/animal/")
async def read_animal(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


"""
给可选参数一个默认值`None`
"""


@app.get("/items1/{item_id}")
async def read_item1(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


"""
bool类型转换器

前端可以传入：
1/0
True/False
true/false
on/off
yes/no
"""


@app.get("/items2/{item_id}")
async def read_item2(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


"""
多个路径参数
http://localhost:8000/users/1/items/hello%20world?q=option&short=yes
"""


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        item_id: str, user_id: int, short: bool = False, q: Optional[str] = None
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


"""
必传参数
"""


@app.get("/items3/{item_id}")
async def read_user_item3(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


"""
使用 pydantic 创建一个数据 model

0. 良好的文档显示
1. 数据有验证作用
2. 数据有类型转换作用
3. 有良好的编辑器支持
"""


class Goods(BaseModel):
    name: str = Field(..., example="Foo2")
    description: Optional[str] = Field(None, example="A very nice Item2")
    price: float = Field(..., example=35.42)
    tax: Optional[float] = Field(None, example=3.22)

    # 增加一个schema。方式一。
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "name": "Foo",
    #             "description": "A very nice Goods",
    #             "price": 35.4,
    #             "tax": 3.2,
    #         }
    #     }


@app.post("/goods/")
async def create_goods(item: Goods = Body(
    ...,
    example={
        "name": "Foo3",
        "description": "A very nice Item3",
        "price": 35.43,
        "tax": 3.23,
    },
)):  # 定义这个item作为一个参数
    print('测试中', item.__dict__)

    item.name = 'tommy'

    data = item.dict()
    if item.tax:
        print('in here')
        price_with_tax = item.price + item.tax
        data.update({'price_with_tax': price_with_tax})

    return data


"""
请求体 + 路径参数 + 请求参数

你可以同时设置路径参数和请求体。

以及额外的请求体参数传递
"""


@app.put('/goods/{goods_id}/')
def update_goods(goods_id: int, goods: Goods, q: str = None, other_q: int = Body(11)):
    """更新一个产品"""
    print('others', other_q)
    result = {"goods_id": goods_id, **goods.dict()}
    if q:
        result.update({'q': q})

    return result


"""
请求参数 + 字符串验证
https://fastapi.tiangolo.com/tutorial/query-params-str-validations/
"""


@app.get('/book')
def read_book(q: Optional[str] = Query(..., min_length=2, max_length=10, regex="^fixedquery$")):  # 添加验证
    print('获取到的参数', q)
    results = {'books': [
        {'book_id': 1, 'name': 'book1'},
        {'book_id': 2, 'name': 'book2'},
    ]}
    if q:
        results.update({'q': q})
    return results


# 请求参数获取多个值
@app.get('/class/')
def read_class(q: Optional[List[int]] = Query([1, 4], title='list query', alias='q-list', deprecated=True)):
    # def read_class(q: list = Query(["foo", "bar"])):
    print('获取到的班级', q)
    return {'code': 1, 'q': q}


"""
路径参数与数字验证
"""


@app.get('/book/{book_id}')
def get_book(
        book_id: int = Path(..., title='The id of the item to get'),
        q: Optional[str] = Query(None, alias="item-query"),
):
    results = {'book_id': book_id}
    if q:
        results.update({'q': q})
    return results


# Python语法：如果你将带有默认值的参数放在没有默认值的参数前面，Python会报错。
@app.get('/phone/{item_id}/')
def get_phone(q: str, item_id: int = Path(..., title="The ID of the item to get")):
    # 路径参数最后会通过关键字获取，所以先写请求参数，再写路径参数也没有关系
    print(locals())
    return 'ok'


@app.get('/food/{item_id}')
def get_food(*, item_id: int = Path(3, gt=2, le=10), q: str):
    data = {'q': q, 'item_id': item_id}
    if q:
        data.update({'q': q})
    return data


@app.get('/food1/{item_id}')
def get_food1(*, item_id: float = Path(3, gt=2.3), q: str):
    data = {'q': q, 'item_id': item_id}
    if q:
        data.update({'q': q})
    return data


class Lesson(BaseModel):
    id: int
    desc: str
    image: str = None


"""
请求体 - 更多的参数
"""


# 1. 混合参数
@app.put('/lesson/{lesson_id}')
def read_lesson(
        lesson: Lesson,
        limit: str = Query(...),
        lesson_id: int = Path(...),
):
    print(locals())
    print(lesson.__dict__)

    data = {'limit': limit, 'lesson_id': lesson_id, **lesson.dict()}
    return data


# 2. 多个请求体参数和多个请求参数、路径参数

class User1(BaseModel):
    username: str
    age: int


@app.post('/lesson/{lesson_id}')
def create_lesson(
        *,  # 为了规范语法
        lesson_id: int = Path(...),  # 路径参数
        user: User1,  # body参数
        lesson: Lesson,  # body参数
        limit: str,  # 请求参数，必传
        other_body: str = Body(...)  # 其他body参数，必传
):
    print('locals', locals())

    return {
        'lesson_id': lesson_id,
        'user': user,
        'lesson': lesson,
        'limit': limit,
        'other_body': other_body
    }


@app.put('/lesson1/')
def lesson1(lesson: Lesson = Body(..., embed=True)):
    print('locals', locals())
    print('我是一个小小鸟', lesson)
    return {'request': lesson}


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


@app.post('/user/')
def create_user(user: User):
    print('user', user.__dict__)

    data = {'code': 1, 'data': {'user': user}}
    return data


@app.put('/user/')
def edit_user(user: User):
    return {'user': user}


class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    users: List[User]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    print(images[0])
    print(images[1])
    return images


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    print(weights)
    return weights


"""
uuid demo
"""


@app.put('/item3/{item_id}')
def read_item3(
        item_id: UUID,
        # 7f0af3b3-240c-429a-8425-9f6095f43d9e
        start_datetime: Optional[datetime] = Body(None),
        end_datetime: Optional[datetime] = Body(None),
        repeat_at: Optional[time] = Body(None),
        process_after: Optional[timedelta] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    print(start_datetime, type(start_datetime))
    print('uuid', item_id, type(item_id))
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }


@app.get('/cookies/')
def read_cookies(ads_id: str = Cookie(None,)):
    print('获取到的cookies ads_id', ads_id)
    return {"ads_id": ads_id}
