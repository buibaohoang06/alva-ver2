from app import app
from index import indexbp

app.register_blueprint(indexbp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)