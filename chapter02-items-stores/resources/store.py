from flask_restful import Resource, request
from marshmallow import ValidationError

from models.store import StoreModel
from schemas.store import StoreSchema

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):

	@classmethod
	def get(cls, name: str):
		store = StoreModel.find_by_name(name=name)
		if store:
			return store_schema.dump(store), 200
		return {"message": "Store not found"}

	@classmethod
	def post(cls, name: str):
		if StoreModel.find_by_name(name=name):
			return dict(message="Store with name already exists"), 400

		store = StoreModel(name=name)
		try:
			store.save_to_db()
		except Exception as err:
			return dict(message="Error inserting."), 500

		return store_schema.dump(store), 201

	@classmethod
	def delete(cls, name: str):
		store = StoreModel.find_by_name(name=name)
		if store:
			store.delete_from_db()
			return {"message": "Store deleted"}, 200
		return {"message": "Store not found to be deleted"}, 404


class StoreList(Resource):
	@classmethod
	def get(cls):
		return {"stores": store_list_schema.dump(StoreModel.find_all())}, 200
