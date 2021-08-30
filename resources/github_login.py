from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource

from models.user import UserModel
from oa import github
from flask import g, url_for, request


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(callback=url_for("github.authorized", _external=True))


class GithubAuthorize(Resource):
    """
    Get authorization
    Create user
    Save github token to user
    Create access token
    Return JWT
    Tokengetter will then use the current user to load token from database
    """

    @classmethod
    def get(cls):
        resp = github.authorized_response()
        if resp is None or resp.get('access_token') is None:
            return {"error": request.args.get('error'),
                    "error_description": request.args.get('error_description')}

        g.access_token = resp['access_token']
        github_user = github.get('user')
        github_username = github_user.data['login']

        user = UserModel.find_by_username(_username=github_username)
        if not user:
            user = UserModel(username=github_username, password=None)
            user.save_to_db()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200
