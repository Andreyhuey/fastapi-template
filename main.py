from fastapi import FastAPI, Query, Path
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
@app.get("/list-items")
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
    description: Optional[str] = None # to make it an optional field, this works for python (3.10 <)
    price: float
    tax: float | None = None # to make it an optional field, this works for certain versions of python (3.10 >)

# creates a price with tax field when the tax is provided
@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

# Query Parameters and String Validation

@app.get("/items")
async def read_items(q: str | None = Query(None, min_length=3, max_length=10, title = "Sample query string", description="This is a sample query string", deprecated=True, alias='item-query')):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# never name your function the same thing as your parameter
@app.get('/items_hidden')
async def hidden_query_route(hidden_query: str | None = Query(None, include_in_schema=False)):
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {"hidden_query": "Not found"}


## Path Parameters and Numeric Validations

@app.get("/items_validation/{item_id}")
async def read_items_validation(
    *,
    item_id: int = Path (..., title="The ID of the item to get", ge=10, le=100)
    , q: str = 'hello'):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

