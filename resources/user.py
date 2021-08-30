from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel
from schemas.user import UserSchema
from passlib.context import CryptContext

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
        )


def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)


"""
User Registration APIs - for creating users in the database
User Login API - for providing a user jwt access token
User Test APIs for testing user's get, post and delete
"""


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)
        user.password = encrypt_password(user.password)

        if UserModel.find_by_username(user.username):
            return {'message': f'username {user.username} already exists'}

        user.save_to_db()
        return {"message": f"user {user.username} created successfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(_id=user_id)
        if not user:
            return {"message": f"user {user.username} does not exist"}, 404

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(_id=user_id)
        if not user:
            return {"message": f"user {user.username} does not exist"}, 404

        user.delete_from_db()
        return {"message": f"user {user.username} deleted successfully"}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)

        user = UserModel.find_by_username(user_data.username)

        if user and user.password and check_encrypted_password(user_data.password, user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "invalid user credentials"}


class UserList(Resource):
    @classmethod
    def get(cls):
        return {"users": user_list_schema.dump(UserModel.find_all())}
