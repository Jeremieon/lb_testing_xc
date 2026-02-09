"""
CRUD App - Basic CRUD operations for testing URI-based routing
Run with: uvicorn app_crud:app --host 0.0.0.0 --port 8002
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="CRUD App")

# In-memory storage
items: Dict[int, dict] = {}
item_id_counter = 1

class Item(BaseModel):
    name: str
    description: str
    price: float

@app.get("/")
async def root():
    return {"app": "crud-app", "message": "Use /items for CRUD operations"}

@app.get("/items")
async def get_items():
    """GET all items"""
    return {"app": "crud-app", "items": items}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """GET single item"""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"app": "crud-app", "item": items[item_id]}

@app.post("/items")
async def create_item(item: Item):
    """CREATE new item"""
    global item_id_counter
    items[item_id_counter] = item.dict()
    item_id = item_id_counter
    item_id_counter += 1
    return {"app": "crud-app", "message": "Item created", "item_id": item_id, "item": items[item_id]}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """UPDATE existing item"""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item.dict()
    return {"app": "crud-app", "message": "Item updated", "item": items[item_id]}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """DELETE item"""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"app": "crud-app", "message": "Item deleted", "item_id": item_id}

@app.get("/health")
async def health():
    return {"status": "healthy", "app": "crud-app"}
