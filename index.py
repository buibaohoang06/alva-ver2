from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import *
from hashlib import sha256, md5
from sqlalchemy import desc
from sqlalchemy.exc import OperationalError
from uuid import uuid1
from sqlite3 import IntegrityError
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, EmailField, FileField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from datetime import datetime
import os

#Initialize Blueprint
indexbp = Blueprint("index", __name__, url_prefix="/", template_folder="templates", static_folder="static")

#Functions
def hash_md5(data: str):
    return md5(data.encode('utf-8')).hexdigest()

def hash_sha256(data: str):
    return sha256(data.encode('utf-8')).hexdigest()

def check_hash_sha256(data: str, data_compare: str):
    return hash_sha256(data=data) == data_compare

def check_hash(data: str, data_compare: str):
    return hash_md5(data=data) == data_compare

def hash_image(image_route: str):
    try:
        with open(image_route, 'r', encoding="latin-1") as image_raw:
            return md5(image_raw.read().encode()).hexdigest()
    except Exception as e:
        raise e

def check_exist(asset_id: str):
    try:
        Assets.query.fitler_by(asset_id=asset_id).first().asset_name
        return True
    except AttributeError:
        return False

def create_order(asset_id: str, amount: int, buyer: str, seller: str):
    message = ""
    status = ""
    bill_id = ""
    while True:
        try:
            #Subtract Balance
            wallet = Wallet.query.filter_by(owner=buyer).first()
            if wallet.balance >= amount:
                wallet.balance = wallet.balance - amount
                order = Orders()
                order.order_id, bill_id = str(uuid1)
                order.asset_id = asset_id
                order.amount = amount
                order.buyer = buyer
                order.seller = seller
                db.session.add(order)
                db.session.commit()
                status = "success"
                break
            else:
                status = "danger"
                message = "insufficient funds"
                break
        except IntegrityError:
            continue
        except Exception as e:
            status = "danger"
            message = str(e)
            break
    return {
        "status": status,
        "message": message,
        "bill_id": bill_id
    }

#Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index.login"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

#Forms
class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired()], render_kw={"placeholder": "email"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "password"})
    submit = SubmitField()

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "usernmae"})
    phonenumber = StringField(validators=[InputRequired()], render_kw={"placeholder": "phonenumber"})
    email = StringField(validators=[InputRequired()], render_kw={"placeholder": "email"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "password"})
    submit = SubmitField()

class CreatePost(FlaskForm):
    file_data = FileField(validators=[InputRequired()])
    image_title = StringField(validators=[InputRequired()], render_kw={"placeholder": "Title"})
    image_description = TextAreaField(validators=[InputRequired()], render_kw={"placeholder": "Description"})
    price = IntegerField(validators=[InputRequired()])
    submit = SubmitField()
    
#Routes
@indexbp.route('/', methods=['GET', 'POST'])
def indexpage():
    return render_template('index.html')

@indexbp.route('/marketplace', methods=['GET', 'POST'])
def marketplace():
    page = request.args.get('p', 1)
    try:
        assets = Assets.query.order_by(desc(Assets.id)).paginate(page=page, per_page=12)
    except OperationalError:
        assets = None
    return render_template('marketplace.html', assets=assets)

@indexbp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(f'/user/{current_user.username}')
    form = LoginForm()
    if form.validate_on_submit():
        try:
            if check_hash_sha256(data=form.password.data, data_compare=User.query.filter_by(email=form.email.data).first().hashed_password):
                login_user(User.query.filter_by(email=form.email.data).first())
                flash('Logged in!', 'success')
                return redirect('/')
            else:
                flash('Wrong email or password!', 'danger')
                return redirect('/login')
        except AttributeError:
            db.session.rollback()
            flash('User doesnt exist!', 'danger')
            return redirect('/login')
        except Exception as e:
            print(str(e))
            db.session.rollback()
            flash('Error occurred!', 'danger')
            return redirect('/login')
    return render_template('auth.html', page="login", form=form)

@indexbp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(f'/user/{current_user.username}')
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User()
            user.username = form.username.data
            user.hashed_password = hash_sha256(data=form.password.data)
            user.email = form.email.data
            user.phone_number = form.phonenumber.data
            user.user_id = hash_md5(form.username.data)
            user.created_at = datetime.now()
            db.session.add(user)
            db.session.commit()
            flash('Successfully registered user. Please login again!', 'success')
            return redirect('/login')
        except Exception as e:
            print(str(e))
            flash('Error occurred!', 'danger')
            return redirect('/register')
    return render_template('auth.html', page="register", form=form)

@indexbp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out!')
    return redirect('/login')

@indexbp.route('/user/<username>', methods=['GET', 'POST'])
def user(username: str):
    page = request.args.get('page', 1)
    user_lookup = User.query.filter_by(username=username).first()
    assets = Assets.query.filter_by(owner=user_lookup.user_id).order_by(desc(Assets.id)).paginate(page=page, per_page=9)
    return render_template('user.html', user=user_lookup, assets=assets)

@indexbp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    asset = Assets.query.filter_by(owner=current_user.user_id)
    #Create Post Form
    create = CreatePost()
    if create.validate_on_submit():
        try:
            image = create.file_data.data
            uuid = str(uuid1())
            image.save(f'static/uploaded/{uuid}.png')
            #Hash image
            image_hash = hash_image(f'static/uploaded/{uuid}.png')
            if os.path.exists(f'static/uploaded/{image_hash}.png'):
                os.remove(f'static/uploaded/{uuid}.png')
                flash('Image already existed in database!', 'danger')
                return redirect('/dashboard')
            else:
                os.rename(f'static/uploaded/{uuid}.png', f'static/uploaded/{image_hash}.png')
                #Push image to database
                asset = Assets()
                asset.asset_id = uuid
                asset.asset_name = create.image_title.data
                asset.asset_hash = image_hash
                asset.asset_route = f'static/uploaded/{image_hash}.png'
                asset.asset_description = create.image_description.data
                asset.price = int(create.price.data)
                asset.owner = current_user.user_id
                db.session.add(asset)
                db.session.commit()
                flash('Image uploaded!', 'success')
                return redirect('/dashboard')
        except Exception as e:
            print(str(e))
            flash('Error occurred', 'danger')
            return redirect('/dashboard')
    return render_template('dashboard.html', current_user=current_user, create=create)

@indexbp.route('/asset/<asset>', methods=['GET', 'POST'])
@login_required
def view_product(asset_id: str):
    product = Assets.query.filter_by(asset_id=asset_id).first()
    return render_template('asset.html', asset=product)

@indexbp.route('/purchase', methods=['GET', 'POST'])
@login_required
def buy():
    asset_id = request.args.get('asset_id')
    if check_exist(asset_id=asset_id):
        asset = Assets.query.filter_by(asset_id=asset_id).first()
        if request.method == "POST" and request.args.get('purchase') == 1:
            order = create_order(
                asset_id = asset_id,
                buyer=current_user.user_id,
                seller=asset.owner,
                amount = asset.price
            )
            flash(order['message'], order['message'])
            return redirect('/purchase')
        return render_template('buy.html', asset=asset)
    return abort(404)
