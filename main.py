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
