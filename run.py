from app import app
from index import indexbp
from api import apibp
<<<<<<< HEAD
from error import errorbp

app.register_blueprint(indexbp)
app.register_blueprint(apibp)
app.register_blueprint(errorbp)
=======

app.register_blueprint(indexbp)
app.register_blueprint(apibp)
>>>>>>> d2e877d417e99c90ac91ea6216310fa9bd5072bb

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True, host="0.0.0.0", port=80)