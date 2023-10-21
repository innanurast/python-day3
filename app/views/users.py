from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields
from ..utils import db
from ..models.users import Users
from ..logs.log import flasklogger

#namespace digunakan untuk mengelompokkan route yang berkaitan dengan entitas tertentu
#nama namespace digunakan untuk sebagai nama endpoint, nanti jadinya /users
users_ns = Namespace('users', description='Namespace for users')

# .model() digunakan untuk mendefiniskan atribut dari model tersebut
# digunakan untuk melakukan validasi data yang diterima dan memberikan struktur respons
users_model = users_ns.model(
    # mendefinisikan model users dengan atribut id, username, password
    'Users', {
        'id': fields.Integer(description = "Ini adalah user"),
        'username': fields.String(description = "Ini adalah username"),
        'password': fields.String(description = "Ini adalah password")
    }
)

@users_ns.route('/') #mendefinisikan route /users/
class UserGetPost(Resource):
    #resource berisi :
    # self : mengakses properti atau metode lain dari kelas resource
    # args : berisi nilai parameter URL misal /users/<int:user_id>, jadi bisa mengambil user_id
    # kwargs : berisi nilai parameter query string, misal terdapat parameter ?=name=Nia, nisa mengambil query name
    # data : berisi json yang di body request

    # .doc() untuk memberikan keterangan di swaggernya 
    @users_ns.marshal_list_with(users_model) 
    # mashal_list_with digunakan untuk mengkonversi banyak objek ke format JSON
    @users_ns.doc(description = "Get all users")
    def get(self):
        """Get All Data Users"""
        try:
            data_users = Users.query.all()
            print("data berhasil : ", data_users)
            flasklogger.info(f"Data User =  {data_users}")

            # return data, 200
            # return {
            #     "status": 200,
            #     "message": "Berhasil mengambil data user",
            #     "data": data_users
            # }
            return data_users, HTTPStatus.OK
    
        except Exception as e:
            # print("Error : ", e)
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
        
    
    @users_ns.doc(
        description = "Create New User"
    )
    @users_ns.expect(users_model)  # menggunakan model "users_model" untuk validasi input di body
    @users_ns.marshal_with(users_model) # untuk mengkonversi satu objek ke format JSON
    def post(self):
        """Get New Data User"""

        try:
            new_user = request.get_json()
            print(f"data : {new_user}") #ketika sudah dipatikan aman tidak butuh lagi function seperti print input kalau di kava console.log
            
            new_input_user = Users(
                username = new_user.get('username'),
                password = new_user.get('password'),
            )

            flasklogger.info(f"Data User =  {new_input_user}")
            db.session.add(new_input_user)
            db.session.commit()

            return [], HTTPStatus.CREATED

        except Exception as e:
            print("Error Post : ", e)
            return [], HTTPStatus.BAD_REQUEST


@users_ns.route('/<int:user_id>')
class UserGetPutDelete(Resource):
    @users_ns.doc(
            description = "Get user data by id", 
            params = {"user_id": "Id user"}
    )
    @users_ns.marshal_list_with(users_model)
    def get(self, user_id):
        """Get user data by id"""
        try:
            data = Users.query.get_or_404(user_id)
            return data, HTTPStatus.OK

        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
        
    @users_ns.marshal_with(users_model)
    @users_ns.expect(users_model)
    @users_ns.doc(
        description = "Update user by Id",
        params = {
            "user_id" : "An Id a given user for method PUT by id"
        }
    )
    def put(self, user_id):
        """Update User Data by Id Unique"""
        try:
            user_to_update = Users.query.get_or_404(user_id)

            data = users_ns.payload

            user_to_update.username = data['username'],
            user_to_update.password = data['password']

            db.session.commit()

            return [], HTTPStatus.OK
        
        except Exception as e:
            print("Error update by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    @users_ns.marshal_with(users_model)
    @users_ns.doc(
        description = "Delete by user id",
        params = {
            "user_id" : "An Id a given user for method PUT by id"
        }
    )
    def delete(self, user_id):
        """Delete User Data by Id Unique"""
        try:
            user_to_delete = Users.query.get_or_404(user_id)
    
            db.session.delete(user_to_delete)
            db.session.commit()

            return [], HTTPStatus.OK
        
        except Exception as e:
            print("Error delete by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
