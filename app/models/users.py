from ..utils  import db

class Users(db.Model): #digunakan untuk membaut tabel pada database 
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

def __repr__(self):
    return f'<users {self.username}>' 