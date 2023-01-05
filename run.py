from app import app
from index import indexbp
from api import apibp
from error import errorbp

app.register_blueprint(indexbp)
app.register_blueprint(apibp)
app.register_blueprint(errorbp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)