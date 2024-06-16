from flask import Flask, request
from db import items, stores
import uuid

app = Flask(__name__)

@app.get("/store")
def get_stores() -> dict:
    return {"stores": list(stores.values())}

@app.post("/store")
def create_store() -> tuple[dict, int]:
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201

@app.post("/item")
def create_item(name: str) -> tuple[dict, int]:
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201

@app.get("/item")
def get_all_items() -> dict:
    return {"items": list(items.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id: str) -> tuple[dict, int]:
    try:
        inventory = stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404
    else:
        if len(inventory) == 0:
            return {"message": "No store inventory"}, 204
        return inventory, 200

@app.get("/item/<string:item_id>")
def get_item_in_store(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item not found"}, 404