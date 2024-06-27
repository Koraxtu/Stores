# from flask import request #Flask
from flask_smorest import abort, Blueprint # type: ignore
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models import StoreModel
from schemas import StoreSchema
from db import db

#import uuid
from typing import Any


blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self) -> list:
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data) -> tuple[dict, int]:
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return store, 201


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id: str) -> Any:
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id) -> Any:
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}