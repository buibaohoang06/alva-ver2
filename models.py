from app import app
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    hashed_password = db.Column(db.String(), unique=False, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime())
    phone_number = db.Column(db.String(), unique=True, nullable=False)

class Assets(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    asset_id = db.Column(db.String(), unique=True, nullable=False)
    asset_name = db.Column(db.String(), unique=True, nullable=False)
    asset_hash = db.Column(db.String(), unique=True, nullable=False)
    asset_route = db.Column(db.String(), unique=True, nullable=False)
    asset_description = db.Column(db.String(), unique=False, nullable=False)
    price = db.Column(db.Integer(), unique=False, nullable=False)
    owner = db.Column(db.String(), unique=False, nullable=False)
    creation_date = db.Column(db.DateTime())

class Wallet(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    wallet_id = db.Column(db.String(), unique=True, nullable=False)
    balance = db.Column(db.String(), unique=False, nullable=False, default=0)
    wallet_owner = db.Column(db.String(), unique=True, nullable=False)

class Transactions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    transaction_id = db.Column(db.String(), unique=True, nullable=False)
    transaction_type = db.Column(db.String(), unique=False, nullable=False)
    amount = db.Column(db.Integer(), unique=False, nullable=False)
    owner = db.Column(db.String(), unique=True, nullable=False)

class Orders(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.String(), unique=True, nullable=False)
    asset_id = db.Column(db.String(), unique=True, nullable=False)
    seller = db.Column(db.String(), unique=False, nullable=False)
    buyer = db.Column(db.String(), unique=False, nullable=False)
    amount = db.Column(db.Integer(), unique=False, nullable=False)

