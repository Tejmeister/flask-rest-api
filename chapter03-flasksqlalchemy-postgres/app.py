import os
from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from ma import ma
from db import db
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from dotenv import load_dotenv
import psycopg2
from flask_migrate import Migrate

print(psycopg2.apilevel)
app = Flask(__name__)
if os.path.isfile(".env"):
    print("loading .env file")
    load_dotenv(".env")
swag = Swagger(app)  # , config=swg.config)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app=app)
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

db.init_app(app)
migrate = Migrate(app, db)



@app.route('/')
def home():
    return "Hello! my first flask app"


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    ma.init_app(app)
    app.run(port=5002, debug=True)

