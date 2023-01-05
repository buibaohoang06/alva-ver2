from app import app
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    hashed_password = db.Column(db.String(), unique=False, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime())
    phone_number = db.Column(db.String(), unique=True, nullable=False)
    verified = db.Column(db.Boolean(), default=False)

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

class Orders(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.String(), unique=True, nullable=False)
    asset_id = db.Column(db.String(), unique=False, nullable=False)
    seller = db.Column(db.String(), unique=False, nullable=False)
    buyer = db.Column(db.String(), unique=False, nullable=False)
    amount = db.Column(db.Integer(), unique=False, nullable=False)
    created_at = db.Column(db.DateTime())

class Verify(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    verify_key = db.Column(db.String(), unique=True, nullable=False)
