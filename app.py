from flask import Flask, request
from flask_smorest import abort # type: ignore
from db import items, stores
import uuid

app = Flask(__name__)

@app.get("/store")
def get_stores() -> dict:
    return {"stores": list(stores.values())}

@app.post("/store")
def create_store() -> tuple[dict, int]:
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure store name is included in the JSON payload.")

    for store in stores:
        if store_data["name"] == store["name"]:
            abort(400, message="Bad request. Ensure unique store name.")

    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201

@app.get("/store/<string:store_id>")
def get_store(store_id: str) -> tuple[dict, int]:
    try:
        inventory = stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")
        return {}, 0
    else:
        if len(inventory) == 0:
            return {"message": "No store inventory."}, 204
        return inventory, 200

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")

@app.post("/item")
def create_item() -> tuple[dict, int]:
    item_data = request.get_json()
    if ("price" not in item_data or 
        "store_id" not in item_data or 
        "name" not in item_data):
        abort(400, message=f"Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.{item_data}")

    for item in items.values():
        if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
            abort(400, message=f"Bad request. Ensure unique item name.{item_data}")

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201
   
@app.get("/item")
def get_all_items() -> dict:
    return {"items": list(items.values())}

@app.get("/item/<string:item_id>")
def get_item_in_store(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    correctItem = request.get_json()
    if "name" not in correctItem and "price" not in correctItem:
        abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload.")
    
    try:
        item = items[item_id]
        item |= correctItem
        return item
    except KeyError:
        abort(404, message="Item not found.")