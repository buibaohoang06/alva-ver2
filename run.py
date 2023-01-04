from app import app
from index import indexbp
from api import apibp

app.register_blueprint(indexbp)
app.register_blueprint(apibp)

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True, host="0.0.0.0", port=80)