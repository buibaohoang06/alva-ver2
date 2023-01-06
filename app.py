from flask import Flask

app = Flask(__name__)

#Configs
app.config['SECRET_KEY'] = 'f7ed244257464aa7e089f61909e90b82'
app.config['UPLOAD_FOLDER'] = '/upload'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dcjiwbfn:mm0k1YE4Qll7i7MSEg3AGefubeR5iuKz@john.db.elephantsql.com/dcjiwbfn'