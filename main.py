from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Path Parameters

@app.get("/")
def hello():
    return {"message": "welcome to a go to FastAPI backend"}

@app.get("/wait")
def wait():
    return {"wait": "this works well now"}


fake_items_db = [{"item_name": "Foo"},{"item_name": "Moo"},{"item_name": "Coo"},{"item_name": "Hoo"}, ]

# Query Parameters
@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

@app.get("/items/{item_id}")
async def get_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short: 
        item.update(
            {
                "description": "Lorem ipsum dolor sit amet, consecutor adipiscing "
            }
        )
    return item  

@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False): 
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short: 
        item.update(
            {
                "description": "Lorem ipsum dolor sit amet, consecutor adipiscing "
            }
        )
        return item

