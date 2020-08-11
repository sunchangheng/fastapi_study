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
        print('前', request.state.__dict__)
        request.state.db = SessionLocal()
        response = await call_next(request)
    except Exception as e:
        print('出现异常', e)
        return response
    finally:
        print('后', request.state.__dict__)
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
