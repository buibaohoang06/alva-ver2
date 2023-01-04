from flask import Flask

app = Flask(__name__)

#Configs
app.config['SECRET_KEY'] = 'f7ed244257464aa7e089f61909e90b82'
app.config['UPLOAD_FOLDER'] = '/upload'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./instance/database.db'