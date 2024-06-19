from flask import request #Flask
from flask_smorest import abort, Blueprint # type: ignore
from flask.views import MethodView
from schemas import StoreSchema
from db import stores
import uuid
from typing import Any


blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self) -> Any:
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data) -> tuple[dict, int]:
        for store in stores:
            if store_data["name"] == store["name"]:
                abort(400, message="Bad request. Ensure unique store name.")

        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id: str) -> Any:
        try:
            inventory = stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")
        else:
            if len(inventory) == 0:
                return {"message": "No store inventory."}, 204
            return inventory, 200

    def delete(self, store_id) -> Any:
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")
