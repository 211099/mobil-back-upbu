from utils.db import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(400), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)




    def __init__(self,email,password,name,phone_number):
        self.email = email
        self.password = password
        self.name = name
        self.phone_number = phone_number