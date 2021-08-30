import os

import psycopg2
from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api

if os.path.isfile(".env"):
    print("loading .env file")
    load_dotenv(".env")

from db import db
from ma import ma
from oa import oauth

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.github_login import GithubLogin, GithubAuthorize
from resources.user import UserLogin, UserRegister, User, UserList

_ = psycopg2.apilevel
app = Flask(__name__)
swag = Swagger(app)  # , config=swg.config)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///data.db")
app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
app.config["JWT_SECRET_KEY"] = os.environ["FLASK_JWT_SECRET_KEY"]
api = Api(app=app)
jwt = JWTManager(app)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(GithubLogin, "/login/github", "/login/github/")
api.add_resource(GithubAuthorize, "/login/github/authorized", endpoint="github.authorized")
api.add_resource(UserLogin, "/user/login")
api.add_resource(UserRegister, "/user/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserList, "/users")
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
    oauth.init_app(app)
    app.run(port=5000, debug=True)
