from flask import Flask
from flask_restful import Api

from ma import ma
from db import db
from resources.item import Item, ItemList

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app=app)
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")


@app.route('/')
def home():
	return "Hello! my first flask app"


@app.before_first_request
def create_tables():
	db.create_all()


if __name__ == "__main__":
	db.init_app(app)
	ma.init_app(app)
	app.run(port=5000, debug=True)
