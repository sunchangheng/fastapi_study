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
