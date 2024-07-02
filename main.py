from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

## Path Parameters

@app.get("/")
def hello():
    return {"message": "welcome to a go to FastAPI backend"}

@app.get("/wait")
def wait():
    return {"wait": "this works well now"}


fake_items_db = [{"item_name": "Foo"},{"item_name": "Moo"},{"item_name": "Coo"},{"item_name": "Hoo"}, ]

## Query Parameters
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

## Request Body
class Item(BaseModel):
    name: str
    description: Optional[str] = None # to make it an optional field
    price: float
    tax: float | None = None # to make it an optional field, this works for certain versions of python

# creates a price with tax field when the tax is provided
@app.post("/items")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
