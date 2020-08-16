[官方文档](https://fastapi.tiangolo.com/tutorial/first-steps/)

## 依赖

FastApi站在巨人的肩膀之上

- `Starlette` 负责web部分
- `Pydantic ` 负责数据部分

## 安装

```
pip install fastapi
pip install uvicorn
```

## 示例

### 创建

创建一个`main.py`文件并写入以下内容

```
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

### 运行

通过以下命令运行服务器

```
uvicorn main:app --reload
```

### 查看效果

1. http://127.0.0.1:8000/items/5?q=somequery
2. 交互式API文档： http://127.0.0.1:8000/docs
3. 可选的API文档： http://127.0.0.1:8000/redoc

## 示例升级

现在修改 `main.py` 文件来从 `PUT` 请求中接收请求体。

我们借助 Pydantic 来使用标准的 Python 类型声明请求体。

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```



## 路径操作

### path

路径从`/` 开始

所以，如果你的URL是以下：

```
https://example.com/items/foo
```

则你的路径是

```
/items/foo
```

> 路径通常也成为为“端点”或“路由”

### operation

当我们构建**APIs**时，通常使用这些特定的HTTP方法来执行特定的操作。

- `POST`: to create data.
- `GET`: to read data.
- `PUT`: to update data.
- `DELETE`: to delete data.

因此，在**OpenAPI**中，每一个HTTP方法我们都叫做一个`operation`

#### Define a *path operation decorator*

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```



### 预定值

导入`Enum`并创建一个继承自`str`和从继承的子类`Enum`。

通过从`str`API 继承，文档将能够知道这些值必须是类型，`string`并且能够正确呈现。

然后创建具有固定值的类属性，这些值将是可用的有效值：

```
from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
```

### 顺序很重要

当前缀路径一样时，注意，把匹配优先级较高的路径写在前面

### 转义文件路径

转义文件路径，后端为了得到完整的显示路径，前端访问的时候要在路径前加个`\`转义

## 请求参数

默认的请求参数在视图函数的参数里接收，接收时可以做类型**验证与转换**

```
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

**ps:**可以给可选参数传一个默认值`None`,使其变成一个可选参数

#### 请求参数转换

前端传递布尔类型

当你的视图函数路径准备接受一个`bool`值时，那么你的前端可以这样传递

```
http://127.0.0.1:8000/items/foo?short=1/0
# or
http://127.0.0.1:8000/items/foo?short=True/False
# or
http://127.0.0.1:8000/items/foo?short=true/false
# or
http://127.0.0.1:8000/items/foo?short=on/off
# or
http://127.0.0.1:8000/items/foo?short=yes/no
```

#### 多个路径参数多个请求参数

当声明多个路径参数和多个请求参数时，**后端**接收时，不需要按顺序写

> ```
> http://localhost:8000/users/1/items/hello%20world?q=option&short=yes
> ```

```
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    item_id: str, user_id: int, short: bool = False,  q: Optional[str] = None
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```

#### 必传参数

后端接收参数**不给默认值**就好

> http://localhost:8000/items3/foo_item?needy=hello

```
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
```

**可选与必传的示例**

当然你也可以传一些必传的，一些可选的。**必传的要在可选的前面声明**

```
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
```

在这里例子中, 这三个请求参数:

- `needy`,  `str` 必传
- `skip`, `int`  可选的 默认值  `0`.
- `limit`,  `int`可选的 默认 不传



## Request Body[¶](https://fastapi.tiangolo.com/tutorial/body/#request-body)

当你需要把数据从客户端发送到后端时，你需要在`request body`中发送

`request body` 是客户端发送到服务端的

`response body` 是服务端发送给客户端的

服务端总是会 发送`response body`,而客户端并**不总是**发送`request body`

> 发送`request body` 你可以使用这些方法: `POST` (the more common), `PUT`, `DELETE` or `PATCH`.
>
> 当你使用`GET`请求发送`request body`在规范里没有明确定义，但是FastAPI支持它，仅适用于极端/复杂的用例
>
> 由于不鼓励，带有Swagger UI的交互式文档在使用GET时不会显示正文的文档，中间的代理可能不支持它。

### 创建一个数据model


0. 良好的文档显示
1. 数据有验证作用
2. 数据有类型转换作用
3. 有良好的编辑器支持


```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```

>  name: str		# 声明name的类型为str
>
>  description: Optional[str] = None		# 类型为str， 默认值为None

### 请求体 + 路径参数

你可以同时设置路径参数和请求体。

```
@app.put('/goods/{goods_id}/')
def update_goods(goods_id: int, goods: Goods):
    """更新一个产品"""
    print('获取到产品', goods)

    return {'goods_id': goods_id, **goods.dict()}
```

### 请求体 + 路径参数 + 请求参数

你甚至可以三个一起组合

```
@app.put('/goods/{goods_id}/')
def update_goods(goods_id: int, goods: Goods, q: str = None):
    """更新一个产品"""
    result = {"item_id": goods_id, **goods.dict()}
    if q:
        result.update({'q': q})

    return result
```



**参数根据以下规则被解析**

- 如果在路径中声明了参数，那么该参数被解析为**路径参数**
- 如果参数是**单一类型**(like `int` `float` `str` `bool`,etc) ，这将被解析为**请求参数**
- 如果参数声明类型为`Pydantic model`，这将解析为**请求体**

### 额外的请求体参数传递

```
@app.put('/goods/{goods_id}/')
def update_goods(goods_id: int, goods: Goods, q: str = None, other_q: int=Body(11)):
    """更新一个产品"""
    print('others', other_q)
    result = {"goods_id": goods_id, **goods.dict()}
    if q:
        result.update({'q': q})

    return result
```

```
# 在这种情况下，FastAPI期望得到如下的请求体
{
    "goods": {
        "name": "Foo",
        "price": 45.2,
        "tax": 2.3
    },
    "other_q": 55
}
```

## 请求参数与字符串验证

**FastAPI** 允许你声明其他其他信息和验证你的信息

```
@app.get('/book')
def read_book(q: Optional[str] = Query(default=None, max_length=10)):   # 添加验证
        print('获取到的参数', q)
        results = {'books': [
            {'book_id': 1, 'name': 'book1'},
            {'book_id': 2, 'name': 'book2'},
        ]}
        if q:
            results.update({'q': q})
        return results
```

> Query 里面可以添加默认值和长度验证

### 默认值

```
q: str = Query(None)
```

### 添加更多的条件

```
q: str = Query(None, min_length=3, max_length=50)
```

### 添加正则匹配

```
q: str = Query(None, min_length=3, max_length=50, regex="^fixedquery$")
```

### 使其必须

当你需要通过`Query`声明一个参数时，你可以使用`...`作为第一个参数 **使其必须**

```
q: str = Query(..., min_length=3)
```

### 请求参数列表/多个值

```
# 请求参数获取多个值
@app.get('/class/')
def read_class(q: Optional[List[str]] = Query(None)):
    print('获取到的班级', q)	# 获取到的班级 ['1', '2']

    return 'ok'
```

**前端请求**

```
localhost:8000/class/?q=1&q=2
```

**后端**的`q`参数将获得一个列表

还会得到一个良好交互文档支持。

#### 设置一个默认值

```
q: List[str] = Query(["foo", "bar"])
```

#### Using `list`

当然你也可以使用`python`内置的`list`代替`List`

```
def read_class(q: list = Query(["foo", "bar"])):
```

**ps:**但这种方式已经将列表的类型固定为`str`

### Query更多的元数据设置

**通用验证和元数据**

- `alias`
- `title`
- `description`
- `deprecated`

**`string`的验证和元数据**

- `min_length`
- `max_length`
- `regex`

## 路径参数与数字验证

> http://localhost:8000/book/2?item-query=哈哈

```
@app.get('/book/{book_id}')
def get_book(
        book_id: int = Path(..., title='The id of the item to get'),
        q: Optional[str] = Query(None, alias="item-query"),
):
    results = {'book_id': book_id}
    if q:
        results.update({'q':  q})
    return results
```

### 参数的顺序问题

```
# Python语法：如果你将带有默认值的参数放在没有默认值的参数前面，Python会报错。
@app.get('/phone/{item_id}/')
def get_phone(q: str, item_id: int = Path(..., title="The ID of the item to get")):
    # 路径参数最后会通过关键字获取，所以先写请求参数，再写路径参数也没有关系
    print(locals())
    return 'ok'
```

### 技巧：按照你想要的顺序排序参数

如果你想要声明一个`q`参数，而且没有`Query`也没有`默认值`，并且有一个路径参数使用`path`的`item_id`路径参数。并且你想要按你想要的顺序写参数。`Python`有一个特殊的语法支持。

通过`*`作为函数的第一个参数。

`Python`不会对`*`做任何操作，但它将知道后面所有参数都应称为关键字参数（键值对），也成为`kwargs`，即使它们没有默认值。

```
from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    *, item_id: int = Path(..., title="The ID of the item to get"), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

## 数字验证：大于或等于

> localhost:8000/food/2/?q=hello

```
@app.get('/food/{item_id}')
def get_food(*, item_id: int = Path(3, gt=2, le=10), q: str):
    data = {'q': q, 'item_id': item_id}
    if q:
        data.update({'q': q})
    return data
```

- gt 大于
- ge 大于等于
- lt 小于
- le 小于等于

**这个验证器同样适用于`float`类型的参数**

## body 更多的参数

### 路径参数 + 请求参数 + 请求体

```
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
```



### 更多的参数和请求体

**这个例子基本上包括所有的参数了**

> localhost:8000/lesson/1/?limit=10

```
# body
{
   "user": {
       "username": "sunchangheng",
       "age": 20
   },
   "lesson": {
       "id": 88,
        "desc": "我是一只小小鸟"
   },
   "other_body": "我是风儿"
}
```

```
@app.post('/lesson/{lesson_id}')
def create_lesson(
        *,  # 为了规范语法
        lesson_id: int = Path(...),  # 路径参数
        user: User,  # body参数
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

```

### 嵌入单个主体参数

即使仅声明了一个参数，您也可以指示FastAPI将主体嵌入键中。

**语法：** `Body(..., embed=True)`

> localhost:8000/lesson1

**请求体**将变成嵌套的

```
{
   "lesson": {
       "id": 88,
        "desc": "我是一只小小鸟"
   }
}
```

```
@app.put('/lesson1/')
def lesson1(lesson: Lesson = Body(..., embed=True)):
    print('locals', locals())
    print('我是一个小小鸟', lesson)
    return {'request': lesson}
```

## body Field

[官方参考文档](https://fastapi.tiangolo.com/tutorial/body-fields/)

您可以使用`Query`，`Path`和`Body`在路径操作函数参数中声明其他验证和元数据的方式相同，也可以使用`Pydantic`的`Field`在`Pydantic Model`内部声明验证和元数据。

```
class User(BaseModel):
    name: str = Field(..., min_length=5, max_length=32)
    password: str
    email: str = Field(..., )


@app.post('/user/')
def create_user(user: User):
    print('user', user.__dict__)

    data = {'code': 1, 'data': {'user': user}}
    return data
```

## body 嵌套模型

### 列表嵌套

```
class User(BaseModel):
    name: str = Field(..., min_length=5, max_length=32)
    password: str
    email: str = Field(..., )
    tag: list = []

@app.put('/user/')
def edit_user(user: User):
    return {'user': user}
```

### 列表嵌套 - 指定列表元素类型

```
from typing import List

class User(BaseModel):
    name: str = Field(..., min_length=5, max_length=32)
    password: str
    email: str = Field(..., )
    # tags: list = []
    tags: List[str] = []    # 指定列表里面的类型
```

### 集合类型

但是随后我们考虑了一下，意识到标签不应该重复，它们可能是唯一的字符串。

```
from typing import Set

class User(BaseModel):
    name: str = Field(..., min_length=5, max_length=32)
    password: str
    email: str = Field(..., )
    # tags: list = []
    # tags: List[str] = []    # 指定列表里面的类型
    tags: Set[str] = set()

@app.put('/user/')
def edit_user(user: User):
    return {'user': user}
```

**注意**：当你接收到一个重复的数据时，这也会转换成一组唯一的数据。

### Nested Models[¶](https://fastapi.tiangolo.com/tutorial/body-nested-models/#nested-models)

每一个`Pydantic Model `的属性都有类型

```
class Image(BaseModel):
    url: str
    name: str


class User(BaseModel):
    name: str = Field(..., min_length=5, max_length=32)
    password: str
    email: str = Field(..., )
    avatar: Optional[Image] = None
```

`FastAPI`期望得到以下格式的回复

```
{
   "name": "su111",
   "password": "xxxx",
   "email": "hello world",
   "tags": ["3", "5", 1,1 ],
   "avatar": {
      "url": "https://google.com/",
      "name": "google"
   }
}
```

### 特殊的类型和验证

除了普通的类型`int` `str` `float`等之外，你可以使用从`str`继承的更复杂的单一类型。

```
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str
```

该字符串将被检查为有效的URL，并在JSON Schema / OpenAPI中进行记录。

### 带有子模型的类型属性

```
class Image(BaseModel):
    url: HttpUrl
    name: str


class User(BaseModel):
    name: str = Field(..., min_length=5, max_length=32)
    password: str
    email: str = Field(..., )
    # tags: list = []
    # tags: List[str] = []    # 指定列表里面的类型
    # tags: Set[str] = set()
    # avatar: Optional[Image] = None
    avatar: Optional[List[Image]] = None
```

`FastAPI`期望得到以下格式的回复

```
{
   "name": "su111",
   "password": "xxxx",
   "email": "hello world",
   "avatar": [
      {
      "url": "https://google.com/",
      "name": "google"
   },
   {
      "url": "https://github.com/",
      "name": "github"
   }
   ]
}

```

### 深层嵌套模型

```
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
```

期望得到的回复

```
{
    "name": "offer1",
    "description": "简介",
    "price": 111,
    "users": [
        {
            "name": "su111",
            "password": "xxxx",
            "email": "hello world",
            "tags": ["3", "5", 1, 1],
            "avatar": [
                {
                    "url": "https://google.com/",
                    "name": "google"
                },
                {
                    "url": "https://github.com/",
                    "name": "github"
                }
            ]
        }, {
            "name": "su111",
            "password": "xxxx",
            "email": "hello world",
            "tags": ["3", "5", 1, 1],
            "avatar": [
                {
                    "url": "https://google.com/",
                    "name": "google"
                },
                {
                    "url": "https://github.com/",
                    "name": "github"
                }
            ]
        }
    ]
}
```

### body 传一个列表

```
class Image(BaseModel):
    url: HttpUrl
    name: str


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images

```

期望得到的回复

```
[
    {"name": "google", "url": "https://google.com"},
    {"name": "github", "url": "https://github.com"}
]
```

### body 传一个字典

```
from typing import Dict

from fastapi import FastAPI

app = FastAPI()


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights
```

> 请记住，JSON仅支持将字符串作为键。
>
> 但是Pydantic具有自动数据转换功能。
>
> 这意味着，即使您的API客户端只能将字符串作为键发送，只要这些字符串包含纯整数，Pydantic就会对其进行转换并验证它们。
>
> 而且您收到的作为权重的字典实际上将具有int键和浮点值。

### 总结

借助FastAPI，您将拥有Pydantic模型提供的最大灵活性，同时保持您的代码简单，简短和优美。

- 编辑器支持（自动补全）
- 数据转换（也叫解析/序列化）
- 数据验证
- schema documentation
- automatic docs

## Pydantic schema[¶](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#pydantic-schema_extra)

您可以使用Config和schema_extra声明Pydantic模型的示例，**ps:**这个示例将会在**文档的请求体默认值**体现

**方式一**：schema_extra

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

**方式二:**   字段附加参数

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

> **注意**
>
> 请记住，出于文档目的，传递的那些额外参数不会添加任何验证，而只会添加注释。

### body 附加参数

与`Field`添加附加参数相同，也可以对`Path`，`Query`，`Body`等进行相同的操作。

```
from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        ...,
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
```



## 额外的数据类型

目前为止，常见的数据类型有

- `int`
- `float`
- `str`
- `bool`

### 其他的数据类型

- `uuid`
  -  "Universally Unique Identifier",在许多数据库和系统中通常作为ID使用。

- `datetime.datetime`
- `datetime.date`
- `datetime.time`
- `datetime.timedelta`
- `frozenset`
- `bytes`
- `Decimal`
- [更多其他Pydantic类型](https://pydantic-docs.helpmanual.io/usage/types/)

### 例子

```
from datetime import datetime, time, timedelta
from typing import Optional
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }
```

```
# path 
http://localhost:8000/items/7f0af3b3-240c-429a-8425-9f6095f43d9e
```

```
# body
{
  "start_datetime": "2020-07-30T06:11:18.070Z",
  "end_datetime": "2020-07-30T06:11:18.070Z",
  "repeat_at": "14:23:55.003",
  "process_after": 3600
}
```



## Cookie 参数

```
from typing import Optional

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}
```

> curl -X GET "http://127.0.0.1:8000/items/" -H  "accept: application/json" -H  "Cookie: ads_id=sss"



## Header 参数

### 声明一个Header参数

```
from typing import Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}
```

> curl -X GET "http://127.0.0.1:8000/items/" -H  "accept: application/json" -H  "user-agent: dddd"

### 禁用自动转换

原始的Header参数中，参数名都是以"-“间隔，而且是大小写敏感的，FastAPI会自动进行转换，将”-“转换为”_"，并将变量字符都转换为小写，如`User-Agent`会被自动转换为`user_agent`，如果不想进行这种默认的转换，可以设置`convert_underscores`为`False`

```
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(*, strange_header: str = Header(None, convert_underscores=False)):
    return {"strange_header": strange_header}
```

```
curl -X GET "http://127.0.0.1:8000/items/" -H  "accept: application/json" -H  "strange_header: ssss"
```

> 警告⚠️
>
> 在将convert_underscores设置为False之前，请记住，某些HTTP代理和服务器不允许使用带下划线的标头。

### 重复的Headers

如果接收到重复的Header，一个键可能有多个值，也就是一个列表。

```
from typing import List, Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(x_token: Optional[List[str]] = Header(None)):
    return {"X-Token values": x_token}
```

```
# 请求
curl -X GET "http://127.0.0.1:8000/items/" -H  "accept: application/json" -H  "x-token: hello,nihao"
```

```
# 响应
{
  "X-Token values": [
    "hello,nihao"
  ]
}
```



## 响应Model

您可以在任何路径操作中使用参数`response_model`声明用于响应的模型：

- `@app.get()`
- `@app.post()`
- `@app.put()`
- `@app.delete()`
- etc.

```
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

### 返回与输入相同的数据

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


# Don't do this in production!
@app.post("/user/", response_model=UserIn)
async def create_user(user: UserIn):
    return user
```

现在，每当浏览器使用密码创建用户时，API都会在响应中返回相同的数据。

### 返回与输入不同

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user
```

### 响应模型可以有默认值

```
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
```

例如，如果您的模型在NoSQL数据库中具有很多可选属性，但是您不想发送很长的JSON响应（包含默认值）。

使用`response_model_exclude_unset` 参数（**排除没有设置过的参数**）

> INFO
>
> You can also use:
>
> - `response_model_exclude_defaults=True`
> - `response_model_exclude_none=True`
>
> as described in [the Pydantic docs](https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict) for `exclude_defaults` and `exclude_none`.

使用`response_model_exclude_unset`仅返回显式设置的值。

### 响应包含/排除某个值

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]
```



## Extra Models

继续前面的示例，通常会有多个相关模型。

用户模型尤其如此，因为：

- The **input model** needs to be able to have a password.
- The **output model** should not have a password.
- The **database model** would probably need to have a hashed password.

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

**减少代码的重复**

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

### 多个Response类型

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "size": 5,
    },
}


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]
```

您可以将响应声明为两种类型的联合`Union`，这意味着该响应将是两种类型中的任何一种。

### List of models[¶](https://fastapi.tiangolo.com/tutorial/extra-models/#list-of-models)

同样，您可以声明对象列表的响应。

```
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str = "default"
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"description": "It's my aeroplane"},
]


@app.get("/items/", response_model=List[Item])
async def read_items():
    return items

```

### Response with arbitrary `dict`[¶](https://fastapi.tiangolo.com/tutorial/extra-models/#response-with-arbitrary-dict)

您还可以使用简单的任意dict声明响应，仅声明键和值的类型，而无需使用Pydantic模型。

如果您事先不知道有效的字段/属性名称（Pydantic模型需要字段名称），此案例将很有用。

```
from typing import Dict

from fastapi import FastAPI

app = FastAPI()


@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
```



## 响应状态码

你可以将响应状态码放到**响应体**里，你也可以在使用参数`status_code`声明用于响应的HTTP状态代码：

- `@app.get()`
- `@app.post()`
- `@app.put()`
- `@app.delete()`
- etc.

```
from fastapi import FastAPI

app = FastAPI()


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}

```

> **注意**
>
> `status_code`是在装饰器函数（get post ...）里面使用的

### 关于HTTP状态码

[不错的解释文档](https://blog.csdn.net/qingquanyingyue/article/details/100538568)

这些状态码都有一个识别它们的**名称**，但重要的是的是状态码的数字。

**简而言之**

- `1XX消息` 您很少直接使用它们。 具有这些状态代码的响应不能带有主体。

  这一类型的状态码，代表请求已被接受，需要继续处理。

- `2XX成功` 这些是你最常用的。

  - 默认状态代码为`200`，表示一切正常。
  - `201`，“已创建”。 通常在数据库中创建新记录后使用。
  - 特殊情况是`204`，“无内容”。 当没有内容返回给客户端时使用此响应，因此该响应必须没有正文。

- `3xx重定向` 带有这些状态码的回复可能带有或没有正文，除了`304“ Not Modified”`,不能有一个正文。

- `4xx客户端错误` 这些是您可能最常使用的第二种类型。

  - 对于“未找到”响应，示例为`404`
  - 对于来自客户端的一般错误，您可以仅使用`400`

- `5xx服务器错误`  您几乎永远不会直接使用它们。 当您的应用程序代码或服务器中的某些部分出现问题时，它将自动返回这些状态代码之一。

### 记住名字的捷径¶

```
from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```



## Form Data[¶](https://fastapi.tiangolo.com/tutorial/request-forms/#form-data)

当您需要接收表单字段而不是JSON时，可以使用`Form`

**安装**

```
pip install python-multipart
```

**示例**

```
from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
```

使用`Form`，您可以声明与`Body`（以及`Query`，`Path`，`Cookie`）相同的元数据和验证。

**注意**：`Form`需要明确的声明

>来自表单的数据通常使用“媒体类型” `application/ x-www-form-urlencoded`进行编码。
>
>但是，当表单包含文件时，它将被编码为`multipart / form-data`。 您将在下一章中了解有关处理文件的信息。

> **警告**
>
> 您可以在路径操作中声明多个`Form`参数，但也不能声明希望以JSON形式接收的`Body`字段，因为请求将使用`application/x-www-form-urlencoded` 代替  `application/json`



## 请求文件

您可以使用`File`定义客户端要上传的文件

> 为了接收上传文件，首先需要安装 `python-multipart`
>
> E.g: pip install python-multipart
>
> 这是因为上载的文件作为“表单数据”发送。

```
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    # file 是一个二进制文件
    return {"file_size": len(file)}
```

如果将路径操作函数参数的类型声明为`bytes`，FastAPI将为您读取文件，并且您将接收内容的内容是`bytes`

请记住，这意味着全部内容将存储在内存中。 这将适用于小文件。

### `File` 参数 ``UploadFile``

```
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
```

与`bytes`相比，使用`UploadFile`有几个优点：

- 它使用“假脱机”文件：
  - 存储在内存中的文件大小上限为最大，超过此限制后，文件将存储在磁盘中。
- 这意味着它可以很好地用于大型文件，例如图像，视频，大型二进制文件等，而不会占用所有内存。

- 您可以从上传的文件中获取元数据。

- 它具有类似[file-like](https://docs.python.org/3/glossary.html#term-file-like-object)的异步接口。

- 它公开了一个实际的Python  [`SpooledTemporaryFile`](https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile)对象，您可以将其直接传递给需要类似文件对象的其他库。

**UploadFile**

`UploadFile`有以下属性

- `filename` 具有上传的原始文件名字符串
- `content_type` 上传文件的类型 ，如：MIME type / media type（e.g. image/jpeg）

- `file` 一个[`SpooledTemporaryFile`](https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile)对象，这是实际的Python文件，您可以将其直接传递给需要“类文件”对象的其他函数或库。

`UploadFile`有以下异步方法

- `write(data)`：将`data`(`str` or `bytes`)写入文件。
- `read(size)`: 读`size(int)` bytes/characters 文件
- `seek(offset)`: 转到文件中的字节位置`offset(int)` 
  - 例如：`await myfile.seek(0)`将跳转到文件开头
  - 这是非常有用的，当你`await myfile.read()`一遍之后，还想重新读取一遍
- `close()`：关闭文件

所有这些方法都是`async`, 所以你需要`await`他们

例如，在异步路径操作函数中，您可以使用以下命令获取内容：

```
contents = await myfile.read()
```

如果您位于普通的def路径操作功能之内，则可以直接访问UploadFile.file，例如：

```
contents = myfile.file.read()
```

> **技术细节**
>
> 当您使用`async`方法时，FastAPI在线程池中运行文件方法并等待它们。

### 多文件上传

这是有可能同时上传多个文件的

They would be associated to the same "form field" sent using "form data".

要使用它，声明一个`bytes`/`UploadFile`的`List`

```
from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
```



## 请求Form和文件

你可以同时定义`File`和`Form`来使用表单和文件

```
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
```



## 处理错误

在许多情况下，您需要将错误通知给使用API的客户端。

该客户端可以是带有前端的浏览器，其他人的代码，IoT设备等。

你可能需要告诉客户端：

- 客户端没有足够的权限进行该操作
- 客户端无线访问资源
- 客户端访问的项目资源不存在
- etc

在这些情况下，您通常会返回400（从400到499）范围内的HTTP状态代码。

### 使用`HTTPException`

要将错误的HTTP响应返回给客户端，请使用`HTTPException`

```
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

因为它是Python异常，所以你不需要`return` 它，而是 `raise` 它

这也意味着，如果您在要在路径操作函数内部调用的工具函数内部，并且从该工具函数内部引发`HTTPException`，它将不会在路径操作函数中运行其余代码， 它将立即终止该请求，并将HTTP错误从`HTTPException`发送到客户端。

**返回结果**

1. 如果客户端访问`http://example.com/items/foo`  (an `item_id` `"foo"`), 他将收到HTTP状态代码`200`和JSON响应：

   ```
   {
     "item": "The Foo Wrestlers"
   }
   ```

2. 如果客户端访问`http://example.com/items/bar`  (a non-existent `item_id` `"bar"`),他将收到HTTP状态码`404`（“未找到”错误）和JSON响应：

   ```
   {
     "detail": "Item not found"
   }
   ```

> 引发`HTTPException`时，您可以传递任何可以转换为JSON的值作为参数详细信息，而不仅限于`str`
>
> 您可以传递字典，列表等。
>
> 它们由FastAPI自动处理并转换为JSON。

### 添加自定义标头

在某些情况下，能够将自定义标头添加到HTTP错误很有用。 例如，对于某些类型的安全性。

```
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}
```



![image-20200731115205418](/Users/sunchangheng/Library/Application Support/typora-user-images/image-20200731115205418.png)



### 自定义异常handler

您可以使用`@app.exception_handler()`添加自定义异常处理程序：

```
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```

这里，如果你请求`/unicorns/yolo`, 该路径操作函数将会`raise` 一个 `UnicornException`

但是它将由`unicorn_exception_handler`处理。

因此，您将收到一个干净的错误，HTTP状态代码为`418`，JSON内容为：

```
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

> **技术细节**
>
> 您还可以使用`from starlette.requests import Request`和`from starlette.responses import JSONResponse`
>
> FastAPI提供了一样的`starlette.responses`相同的`fastapi.responses`, 仅仅只是为了方便开发者，

### 覆盖默认的异常处理器（做全局配置）

这些处理程序负责在引发`HTTPException`以及请求包含无效数据时, 返回默认的JSON响应。

您可以使用自己的异常处理程序覆盖它们。

### 覆盖请求验证异常

当请求包含无效数据时，**FastAPI**内部将会跑出一个`RequestValidationError`

想要覆盖它，导入`RequestValidationError`并用`@app.exception_handler(RequestValidationError)`来装饰你`exception handler`

这个`exception handler` 将接收一个`Request`和异常

```
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    
    return {"item_id": item_id}
```

现在，如果你去`/items/foo` 不是获取默认的JSON错误：

```
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

你将会收到下面的报错

```
1 validation error
path -> item_id
  value is not a valid integer (type=type_error.integer)
```

### 覆盖响应验证异常

```
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print('响应异常', exc)
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
```

> FastAPI有自己的`HTTPException`
>
> FastAPI的`HTTPException`继承于Starlette 的 `HTTPException`
>
> 但不同的是，FastAPI的`HTTPException` 允许您添加`headers`到你的响应体中

### 使用`RequestValidationError` body

您可以在开发应用程序时使用它来记录到日志文件并对其进行调试，然后将其返回给用户，等等。

```
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print('请求异常处理', exc)
    print('body', exc.body)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


class Item(BaseModel):
    title: str
    size: int


@app.post("/items/")
async def create_item(item: Item):
    return item
```

### 重用FastAPI的异常处理程序

```
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {exc}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
```

您知道了，可以使用异常，然后重新使用默认的异常处理程序。

在返回默认的异常处理程序之前，可以做一些自定义操作。



## 路径操作配置

### 响应状态码

你可以使用`status_code`自定义响应状态码

您可以直接传递`int`代码，例如`404`

但是如果你不记得数字的含义，你可以使用`status`里的快捷方式常量

```
from typing import Optional, Set

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
```

### 标签

```
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []


@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
```

这将会被自动文档使用

![image-20200731155046194](/Users/sunchangheng/Library/Application Support/typora-user-images/image-20200731155046194.png)

### 请求摘要和描述

```
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []


@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item 创建一个item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item
```

![image-20200731155350042](/Users/sunchangheng/Library/Application Support/typora-user-images/image-20200731155350042.png)

### 从docstring处获取description

由于描述往往很长并且涵盖多行，因此您可以在函数docstring中声明路径操作描述，FastAPI将从那里读取它。

你可以在`docstring`里写`Markdown`，它将会被正确的解析与显示

```
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []


@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
```

### 响应描述

```
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []


@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
```

> OpenAPI指定每个路径操作都需要响应描述。
>
> 因此，如果您不提供任何一种，FastAPI将自动生成一个"Successful response".

### 弃用路径操作

如果需要将路径操作标记为已弃用，但不删除它，则传递参数`deprecated`

```
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]


@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]
```

在交互式文档中，它将明确标记为不推荐使用：

![image](https://fastapi.tiangolo.com/img/tutorial/path-operation-configuration/image04.png)

### 总结

通过将参数传递给路径操作修饰符，可以轻松地为路径操作配置和添加元数据。



## JSON Compatible Encoder[¶](https://fastapi.tiangolo.com/tutorial/encoder/#json-compatible-encoder)

在某些情况下，您可能需要将数据类型（例如Pydantic模型）转换为与JSON兼容的数据（例如`dict`，`list`等）

### 使用`jsonable_encoder`

假设你有一个数据库，它不接收`datetime`对象，因为那些与JSON不兼容

因此，`datetime`对象必须转换为包含ISO格式数据的`str`

同样，该数据库将不会接收Pydantic模型（具有属性的对象），而只会接收字典。

为此，你可以使用`jsonable_encoder`, 它接收一个对象，例如Pydantic模型，并返回JSON兼容版本：

```
from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
```

在这个例子中，它将Pydantic模型转换为`dict`，并将日期时间转换为`str`

它的结果可以使用`json.dumps()`进行编码



## body 更新

### 更新数据使用`PUT`

您可以使用`jsonable_encoder`将输入数据转换为可以存储为JSON的数据（例如，使用NoSQL数据库）。 例如，将`datetime`转换为`str`

```
from typing import List, Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded
```

`PUT`用于接收应替换现有数据的新数据

**警告更换**

这意味着，如果要使用包含以下内容的主体使用PUT更新项目栏：

```
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

因为它不包含已经存储的属性“ tax”：20.2，所以输入模型将采用“ tax”的默认值：10.5。

而且数据将以“new” tax 10.5 保存。

### 用PATCH进行部分更新

你可以使用  [HTTP `PATCH`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH) 操作来进行部分更新

这意味着您只能发送要更新的数据，其余的保持不变。

> 与PUT相比，PATCH不太常用
>
> 更多的团队甚至使用`PUT`进行部分更新
>
> 您可以随意使用它们，FastAPI并没有施加任何限制。

如果要接收部分更新，则在Pydantic模型的`.dict()`中使用参数`exclude_unset`非常有用。

像：`item.dict(exclude_unset=True)`

这将生成仅包含创建项目模型时设置的数据的`dict`，不包括默认值。

然后，您可以使用它来生成仅包含设置的数据（在请求中发送）的`dict`，而忽略默认值：

```
from typing import List, Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
```

> 使用`exclude_unset`你将获取到用户想设置的参数，而不包含`input model`的默认值
>
> 创建存储模型的副本，使用接收到的部分更新（使用`update`参数）更新其属性。
>
> 使用`jsonable_encoder`将model转换成可以存在DB的数据结构



## Dependencies

“依赖注入”在编程中表示，您的代码（在这种情况下，您的路径操作函数）有一种方法可以声明它必须需要使用的东西：`dependencies`

**下面的场景将会很实用**

- 具有共享逻辑（一次又一次地使用相同的代码逻辑）。
- 共享数据库连接
- 强制执行安全性，身份验证，角色要求等。
- 还有很多其他事情

### 创建一个dependency

```
from typing import Optional

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

**在这种情况下，此依赖项期望：**

- 可选查询参数`q`是`str`
- 可选查询参数`skip`是一个`int`，默认情况下为`0`
- 可选的查询参数`limit`，它是一个`int`，默认值为`100`

#### 异步还是不异步¶

都可以， FastAPI将知道该怎么办。



#### FastAPI compatibility

依赖项注入系统的简单性使FastAPI兼容：

- 关系型数据库
- 非关系型数据库
- external packages
- external APIs
- authentication and authorization systems
- API usage monitoring systems
- response data injection systems
- etc.



### 使用类的方式创建dependency

使用**函数式**创建的`dependency`，我们知道编辑器不能为字典提供很多支持（例如自动补全），因为他们不知道其键和值类型。

所以我们可以使用**类方式**创建`dependency`

```
from typing import Optional

from fastapi import Depends, FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
# async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
async def read_items(commons: CommonQueryParams = Depends()):
    print(commons.__dict__)
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return response

```

这样您的编辑器将知道将作为参数公共变量传递的内容，然后它可以帮助您完成**代码补全**，进行**类型检查**等

**不推荐**

```
commons: CommonQueryParams = Depends(CommonQueryParams)
```

**推荐**快捷方式

```
commons: CommonQueryParams = Depends()
```

> 如果这种方式不是很有帮助，请忽视它
>
> It is just a shortcut. Because **FastAPI** cares about helping you minimize code repetition.



### 子依赖项

```
from typing import Optional

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: Optional[str] = None):
    return q


def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}
```

**多次使用相同的依赖项**

禁用`cache`就好

```
async def needy_dependency(fresh_value: str = Depends(get_value, use_cache=False)):
    return {"fresh_value": fresh_value}
```



### 把依赖项放到装饰器处

在某些情况下，您实际上不需要在路径操作函数内返回依赖项的返回值，但是你还是要执行它。

这种情况下，你可以在装饰器处使用`dependencies`接收一个列表来实现。

```
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
```

`dependencies`里的依赖将会被正常执行，但是他们的返回值将不会传递给路径操作函数。

**Dependency requirements**

他们可以声明请求要求（如：请求头）或其他子依赖项

```
async def verify_token(x_token: str = Header(...)):
```

**Raise exceptions**

这些依赖项可以引发异常，与普通依赖项相同

```
raise HTTPException(status_code=400, detail="X-Token header invalid")
```

**Return values**

这些依赖项可以返回值或者不返回，这些返回值将不会被使用到。

因此，您可以重复使用已经在其他地方使用的普通依赖项（返回一个值），即使不使用该值，该依赖项也将被执行

### Dependencies with yield

FastAPI支持依赖项在完成后会**执行一些额外的步骤**

为此，请使用`yield`而不是`return`，并在其后编写额外的步骤。

#### 一个数据库连接的示例

例如，您可以使用它来创建数据库会话并在完成后将其关闭

```
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
```

发送响应之前，仅执行`yield`语句之前和包括的代码

产生的值是注入到路径操作和其他依赖项中的值

传递响应后，将执行`yield`语句之后的代码

> 您可以使用异步或常规函数

**与`yield`和`try`的依赖项**

如果在具有`yield`的依赖项中使用`try`块，则将收到使用依赖项时引发的任何异常。

例如，如果某些代码在中间，其他依赖项或路径操作中的某个点上使数据库事务“回滚”或创建任何其他错误，则您将在依赖项中收到异常。

以相同的方式，无论是否存在异常，您都可以使用`finally`来确保执行退出步骤。

#### 具有yield的子依赖关系

您可以具有任意大小和形状的子依赖关系和子依赖关系的“树”，并且它们中的任何一个或全部都可以使用`yield`

FastAPI将确保每个具有`yield`的依赖项中的“退出代码”以正确的顺序运行

```
from fastapi import Depends


async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)
```

#### Dependencies with `yield` and `HTTPException`

...

#### Context Managers

```
with open("./somefile.txt") as f:
    contents = f.read()
    print(contents)
```

```
class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with MySuperContextManager() as db:
        yield db
```



## 安全

### 安全介绍

有许多方法可以处理安全性，身份验证和授权。

在许多框架和系统中，仅处理安全性和身份验证会花费大量的精力和代码（在许多情况下，可能占编写的所有代码的50％或更多）。

**FastAPI**提供了多种工具，可帮助您以标准方式轻松，快速地处理**Security**，而无需学习和学习所有安全性规范。

#### OAuth2

OAuth2是一个规范，它定义了几种处理身份验证和授权的方式。

它包括使用“第三方”进行身份验证的方法。

**OAuth 1**

OAuth 1，它与OAuth2完全不同，并且更为复杂，因为它直接包含有关如何加密通信的规范

如今它不是很流行

OAuth2没有指定如何加密通信，它希望您使用HTTPS为您的应用程序提供服务。

#### OpenID Connect

#### OpenAPI

### 第一步

假设您在某个域中拥有**后端**API

并且您在另一个域或同一域（或在移动应用程序中）的不同路径中具有**前端**。

而且，您希望使用用户名和密码为前端提供一种与后端进行身份验证的方法。

```
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

### 获取当前用户

在上一节我们已经为我们的路径操作函数添加了安全系统`token`

但这仍然没有用。

```
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    print('user', user)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```



### 简单的OAuth2 密码验证

```
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```



###  带有密码（和哈希）的OAuth2，带有JWT令牌的Bearer

现在我们已经拥有了所有的安全流程，现在让我们使用JWT令牌和安全密码哈希来使应用程序真正安全。

JWT的意思是“ JSON Web令牌”。

这是将JSON对象编码为长而密集的字符串而没有空格的标准。 看起来像这样：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

它没有加密，因此任何人都可以从内容中恢复信息。

但这是签名的。 因此，当您收到发出的令牌时，可以验证您确实发出了令牌。

这样，您可以创建一个有效期为1周的令牌。 然后，当用户第二天带着令牌返回时，您知道他/他仍在登录到系统。

一周后，令牌将过期，用户将无权授权，必须再次登录才能获得新令牌。 而且，如果用户（或第三方）试图修改令牌以更改到期时间，则您将能够发现它，因为签名不匹配。

**安装**

```
pip install passlib
pip install python-jose
pip install bcrypt
```

> main.py

```
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    """验证plain_password的hash值是否是hashed_password"""
    return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


def get_user(db, username: str):
    """假装从数据库获取用户信息"""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    """验证用户名/密码"""
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """生成token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print('新生成的token', encoded_jwt)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """验证token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """获取当前有效的用户"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """登录接口，返回token"""
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """读取当前用户"""
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """读取当前用户的item"""
    return [{"item_id": "Foo", "owner": current_user.username}]
```



## 中间件

“中间件”是一种功能，该功能可在每个请求通过任何特定路径操作**处理之前，**以及每个**响应返回之前**做特定的操作

- 每一个到你应用的`request`
- 它可以对该请求执行**某些操作**或运行**任何需要的代码**。
- 然后它将请求传递给其余的应用程序
- 然后，它将获取应用程序生成的响应（通过某些路径操作）。
- 它可以对响应做出**某些操作**或运行**任何需要的代码**。
- 然后返回响应

> 如果你有写一些**依赖项**与`yield`，那么`exit code`将会在中间件之后执行
>
> If there were any background tasks (documented later), they will run *after* all the middleware.

### 创建中间件

创建一个中间件使用`@app.middleware("http")`装饰一个函数

**中间件接收：**

- `request`
- 一个函数`call_next`, 它接收一个`request`作为参数
  - 此函数会将`request`传递到相应的路径操作。
  - 然后，它返回由相应路径操作生成的`response`

- 然后你可以在最终返回之前，对`response`再做进一步处理

```
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

> **Tip**
>
> 请记住，可以使用“ X-”前缀添加自定义专有响应头
>
> 但是，如果您希望浏览器中的客户端能够看到自定义标头，则需要使用Starlette的CORS文档中记录的参数`expose_headers`将它们添加到CORS配置（CORS（跨源资源共享））中。

>**技术细节**
>
>你也可以`from starlette.requests import Request`
>
>FastAPI只是为了给你提供便利的导入方式，通过FastAPI导入的`Request`还是来自于`starlette.request` 哦



## CORS

[官方文档](https://fastapi.tiangolo.com/tutorial/cors/)

中文：跨站资源请求。指前端在`JavaScript`运行请求后端的代码时，前端与后端的`origin`不同的情况

### Origin

`origin`是协议（`http，https`），域（`myapp.com，localhost，localhost.tiangolo.com`）和端口（`80、443、8080`）的组合。

所以，下面都是不同源的：

- `http://localhost`
- `https://localhost`
- `http://localhost:8080`

### 使用`CORSMiddleware`

```
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
```

默认情况下，`CORSMiddleware`实现使用的默认参数是限制性的，因此您需要显式启用特定的来源，方法或标头，以便允许浏览器在跨域上下文中使用它们。



## SQL数据库

**FastAPI**不强制您使用SQL（关系）数据库。

你可以非常容易的使用`SQLAlchemy`支持的关系数据库

- PostgreSQL
- MySQL
- SQLite
- Oracle
- Microsoft SQL Server, etc.

FastAPI可与任何数据库和任何样式的库一起使用，以与数据库进行通信。

一种常见的模式是使用“ ORM”：“对象关系映射”库。

常见的`ORM`库有

- Django-ORM
- SQLAlchemy ORM
- Peewee

### 创建SQLAlchemy

> sql_app/database.py

```
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

**注意：**参数

```
connect_args={"check_same_thread": False}
```

仅仅`SQLite`数据库需要，其他数据库不需要

> **技术细节**
>
> 默认情况下，假定每个线程将处理一个独立的请求，SQLite将仅允许一个线程与其通信。
>
> 这是为了防止为不同的事情（针对不同的请求）共享同一连接。
>
> 但是在FastAPI中，使用正常功能（def），可以针对同一请求使用多个线程与数据库进行交互，所以我们知道了SQLite为什么需要`connect_args={"check_same_thread": False}`
>
> 另外，我们将确保每个请求都具有依赖关系，从而获得其自己的数据库连接会话，因此不需要该默认机制。

### 创建数据库model文件

> sql_app/models.py

```
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
```

使用`relationship`创建关系，使用model时会给我们提供很多便利的方法



### 创建初始的Pydantic models/schemas

```
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
```

Pydantic的`orm_mode`将告诉Pydantic模型读取数据，即使它不是`dict`而是`ORM模型`（或任何其他具有属性的任意对象）。

这样，不是仅尝试从字典获取id值，如：

```
id = data["id"]
```

它还将尝试从属性获取它，如：

```
id = data.id
```

因此，Pydantic模型与ORM兼容，您可以在路径操作中的`response_model`参数中声明它。

您将能够返回数据库模型, 并且数据从数据库模型中序列化。

SQLAlchemy和许多其他默认情况下是“延迟加载”。

#### Technical Details about ORM mode

例如，这意味着除非您尝试访问将包含该数据的属性，否则它们不会从数据库中获取关系数据。

例如，访问属性`items`

```
current_user.items
```

这时候SQLAlchemy将会去`items`表，获取这个用户的`items`，而不会提前获取好。

如果没有`orm_mode`，则如果您从路径操作返回了SQLAlchemy模型，则该模型将不包含关系数据。

即使您在Pydantic模型中声明了这些关系。

但是在ORM模式下，由于Pydantic本身会尝试从属性访问其所需的数据（而不是假设一个字典），因此您可以声明要返回的特定数据，并且即使从ORM中也可以获取该数据。 

### CRUD utils

> sql_app/crud.py

```
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

> sql_app/main.py

### Main FastAPI app

```
"""
[参考资料](https://fastapi.tiangolo.com/tutorial/sql-databases/)
"""
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)    # 通常，您可能会使用Alembic初始化数据库（创建表等）

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    except Exception as e:
        print('出现异常', e)
        return response
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """创建用户"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """用户列表"""
    users = crud.get_users(db, skip=skip, limit=limit)
    print('users[0].items', users[0].items)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """用户详情"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    """创建用户item"""
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """item列表"""
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
```

### check it

```
uvicorn sql_app.main:app --reload
```



### 使用中间件来连接关闭数据库连接

If you can't use dependencies with `yield` -- for example, if you are not using **Python 3.7** and can't install the "backports" mentioned above for **Python 3.6** -- you can set up the session in a "middleware" in a similar way.

```
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
```

**Dependencies with `yield` or middleware**

Adding a **middleware** here is similar to what a dependency with `yield` does, with some differences:

- It requires more code and is a bit more complex.

- The middleware has to be an`async` function.
    - If there is code in it that has to "wait" for the network, it could "block" your application there and degrade performance a bit.
    - Although it's probably not very problematic here with the way `SQLAlchemy` works.
    - But if you added more code to the middleware that had a lot of I/O waiting, it could then be problematic.

- A middleware is run for every request.

  - So, a connection will be created for every request.
  - Even when the *path operation* that handles that request didn't need the DB.

> **Tip**
>
> 当依赖关系足以满足用例时，最好将依赖关系与yield一起使用。



## 多应用模块

如果要构建应用程序或Web API，则很少将所有内容都放在一个文件中。

FastAPI提供了一种方便的工具，可在保持所有灵活性的同时构建应用程序。

> 如果您来自Flask，那将相当于Flask的蓝图。

### 一个简单的文件结构

```
.
├── app											// 包含所有的代码
│   ├── __init__.py					// 所以app是一个”Python package“
│   ├── main.py
│   └── routers
│       ├── __init__.py
│       ├── items.py				// 子模块items
│       └── users.py				// 子模块users
```

```
# routers/users.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
```

> **Tip**
>
> 你可以认为`APIRouter`是一个"mini `FastAPI`" 类
>
> 支持所有相同的支持操作
>
> All the same parameters, responses, dependencies, tags, etc.

```
# routers/items.py
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.get("/{item_id}")
async def read_item(item_id: str):
    return {"name": "Fake Specific Item", "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],    # 增加了一个tag, 将会在交互式文档里体现
    responses={4003: {"description": "Operation forbidden"}},    # 将会叠加进 `include_router`的`responses`。并在交互式文档里体现
)
async def update_item(item_id: str):
    if item_id != "foo":
        raise HTTPException(status_code=403, detail="You can only update the item: foo")
    return {"item_id": item_id, "name": "The Fighters"}

```

```
# main.py
from fastapi import Depends, FastAPI, Header, HTTPException

from routers import users, items

app = FastAPI()


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(users.router)    # 使用app.include_router（），我们可以将APIRouter添加到主FastAPI应用程序中

# 前缀，标签，响应和依赖项参数（在许多其他情况下）只是FastAPI的一项功能，可帮助您避免代码重复。
app.include_router(
    items.router,
    prefix="/items",    # 注意：/items   后面不要添加 /
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
```

### 多次包含具有不同前缀的同一路由器

> 您也可以在同一路由器上使用.include_router（）多次使用不同的前缀。
>
> 例如，在不同的前缀下公开相同的API（例如， `/api/v1`和 `/api/latest`
>
> 这是您可能真正不需要的高级用法，但是如果您有需要，可以使用。



## 后台任务

您可以定义返回响应后要运行的后台任务。

这对于在请求后需要执行的操作很有用，但是客户端实际上并不需要在接收响应之前等待操作完成。

**例如**：

- 执行操作后发送的电子邮件通知：
  - 由于连接到电子邮件服务器并发送电子邮件的过程通常很慢（几秒钟），因此您可以立即返回响应并在后台发送电子邮件通知。
- 处理数据：
  - 例如，假设您收到的文件必须经过缓慢的处理，您可以返回“Accepted”（HTTP 202）响应，并在后台对其进行处理。

### 使用`BackgroundTasks`

```
import time

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        print('开始处理notification')
        time.sleep(5)
        content = f"notification for {email}: {message}"
        email_file.write(content)
        print('终于搞定了')


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```

### 依赖注入

使用`BackgroundTasks`还可以与依赖项注入系统一起使用，可以在多个级别上声明`BackgroundTasks`类型的参数：在路径操作函数中，在依赖项（可依赖），在子依赖项中，等等。

**FastAPI**知道在每种情况下该怎么做以及如何重用同一对象，以便所有后台任务合并在一起，然后在后台运行：

```
from typing import Optional

from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}

```

**警告**

如果您需要执行大量的后台计算，而不必一定要在同一进程中运行它（例如，您不需要共享内存，变量等），则可能会受益于使用其他更大的工具，例如 **Celery**

它们往往需要更复杂的配置，例如RabbitMQ或Redis等消息/作业队列管理器，但是它们允许您在多个进程（尤其是多个服务器）中运行后台任务。

但是，如果您需要从同一个FastAPI应用程序访问变量和对象，或者需要执行小的后台任务（例如发送电子邮件通知），则只需使用`BackgroundTasks`



## 元数据和文档URL

你可以在你的**FastAPI**应用程序定义几个元数据配置

### Title, description, and version[¶](https://fastapi.tiangolo.com/tutorial/metadata/#title-description-and-version)

```
from fastapi import FastAPI

app = FastAPI(
    title="My Super Project",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="2.5.0",
)


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]

```

**通过这个配置，我们的交互式文档将会是下面的样子**

![img](https://fastapi.tiangolo.com/img/tutorial/metadata/image01.png)

### 为标签创建元数据

```
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        # "description": "Manage items. So _fancy_ they have their own docs.",
        "description": "管理的items，它们有它们自己的docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)


@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]
```

**现在你再看一下你的交互式文档，你将会看到下面的效果**

![](https://fastapi.tiangolo.com/img/tutorial/metadata/image02.png)

> 每个标签元数据字典的顺序还定义了docs UI中显示的顺序。
>
> 例如，即使`users` 的字母顺序在 `items` 的前面，但是它们的顺序是可以定义的，因为我们可以将`items`的元数据添加为列表中的第一个字典。

### OpenAPI URL[¶](https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url)

默认的，OpenAPI schema 的路径是：`/openapi.json`

但是您可以使用参数`openapi_url`对其进行配置

例如，要将其设置为在`/api/v1/openapi.json`中投放

```
from fastapi import FastAPI

app = FastAPI(openapi_url="/api/v1/openapi.json")


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
```

### Docs URLs

- **Swagger UI**: `/docs`
  - 你可以通过`docs_url`设置URL
  - 你还可以通过`docs_url=None`将其禁用
- ReDoc: `redoc`
  - 您可以使用参数`redoc_url`设置其URL
  - 您可以通过设置`redoc_url=None`禁用它

比如，设置 Swagger UI 到`/documentation`

```
from fastapi import FastAPI

app = FastAPI(docs_url="/documentation", redoc_url=None)


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
```



## 静态文件

您可以使用`StaticFiles`从目录自动提供静态文件

**安装依赖**

```
pip install aiofiles
```

**使用**

```
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
```

现在，浏览器只要访问 `/static` 前缀开头的，就可以访问到**static**文件夹下的静态文件



## 测试

**主文件**

```
# main_b.py
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

app = FastAPI()


class Item(BaseModel):
    id: str
    title: str
    description: Optional[str] = None


@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item.id] = item
    return item

```

**测试文件**

```
# test_main_b.py
from fastapi.testclient import TestClient

from .main_b import app

client = TestClient(app)


def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}

```

- `client`向服务端发送参数，可以参照`requests`
- 测试文件使用`test_`开头
- **安装依赖**：`pip install pytest`
- **执行测试**：`pytest`



## 调试

```
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

可以使用**vscode**或者**pycharm**`debugging`运行这个文件



