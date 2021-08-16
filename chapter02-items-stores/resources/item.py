from flask_restful import Resource, request
from marshmallow import ValidationError

from models.item import ItemModel
from schemas.item import ItemSchema

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):

	@classmethod
	def get(cls, name: str):
		item = ItemModel.find_by_name(name=name)
		if item:
			return item_schema.dump(item), 200
		return {"message": "Item not found"}

	@classmethod
	def post(cls, name: str):
		if ItemModel.find_by_name(name=name):
			return dict(message="Item with name already exists"), 400

		item_json = request.get_json()
		item_json["name"] = name

		print(f"item_json={item_json}")

		try:
			item = item_schema.load(item_json)
		except ValidationError as err:
			return err.messages, 400

		try:
			item.save_to_db()
		except Exception as err:
			return dict(message="Error inserting."), 500

		return item_schema.dump(item), 201

	@classmethod
	def put(cls, name: str):
		item_json = request.get_json()
		item = ItemModel.find_by_name(name=name)
		if item:
			# update the existing Item
			item.price = item_json["price"]
		else:
			# insert the item
			item_json["name"] = name
			try:
				item = item_schema.load(item_json)
			except ValidationError as err:
				return err.messages, 400

		item.save_to_db()

		return item_schema.dump(item), 200

	@classmethod
	def delete(cls, name: str):
		item = ItemModel.find_by_name(name=name)
		if item:
			item.delete_from_db()
			return {"message": "Item deleted"}, 200
		return dict(message="Item not found to be deleted"), 404


class ItemList(Resource):
	@classmethod
	def get(cls):
		return dict(items=item_list_schema.dump(ItemModel.find_all())), 200
