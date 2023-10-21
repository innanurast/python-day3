from flask_restx import Namespace, Resource, fields
from flask import request
from flask import jsonify, json
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from ..utils import db
from ..models.users import Users
from ..logs.log import flasklogger

auth_ns = Namespace('auth', 'Namespace for auth')

# .model() digunakan untuk mendefiniskan atribut dari model tersebut
# digunakan untuk melakukan validasi data yang diterima dan memberikan struktur respons
auth_model = auth_ns.model(
    # mendefinisikan model users dengan atribut id, username, password
    'Users', {
        'id': fields.Integer(description = "Ini adalah user"),
        'username': fields.String(description = "Ini adalah username"),
        'password': fields.String(description = "Ini adalah password")
    }
)

@auth_ns.route('/SignUp')
class SignUp(Resource):
    @auth_ns.expect(auth_model)
    @auth_ns.doc(
        description = "Sign Up for User"
    )
    def post(self):
        """An sign up for new account"""

        data = request.get_json()

        flasklogger.info(f"password original = {data.get('password)')}")
        try:
            data = request.get_json()
            new_user = Users(
                username = data.get('username'),
                password = generate_password_hash(data.get('password'))
            )

            flasklogger.info(f"Data User sign up =  {new_user}")
            flasklogger.info(f"pass hash =  {new_user.password}")

            db.session.add(new_user)
            db.session.commit()

            return [], HTTPStatus.OK

        except Exception as e:
            print("Error Post : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
@auth_ns.route("/signin")
class SignIn(Resource):
    @auth_ns.expect(auth_model)
    @auth_ns.doc(
        description = "Sign In for User"
    )
    def post(self):
        """An sign in for new account"""

        data = request.get_json()

        try:
            user = Users.query.filter_by(username = data.get('username')).first()
            print(f"user db : {user.username}")
            print(f"pass db : {user.password}")
            check_password = check_password_hash(user.password, data.get('password'))

            print(f"check pass : {check_password}")
            flasklogger.info(f"check_password =  {check_password}")

            if user and check_password:
                access_token = create_access_token(identity= user.username)
                refresh_token = create_refresh_token(identity= user.username)

            response = {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

            return response, HTTPStatus.OK

        except Exception as e:
            print("Error Get : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """Refresh JWT token"""

        try:
            username = get_jwt_identity()
            
            access_token = create_access_token(identity= username)

            response = {'access_token': access_token}, HTTPStatus.OK

        except Exception as e:
            print("Error refresh : ", e)
            return [], HTTPStatus.BAD_REQUEST

