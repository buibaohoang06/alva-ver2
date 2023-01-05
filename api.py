from flask import Blueprint, request, jsonify
from models import Orders, User
from sqlalchemy import desc

apibp = Blueprint("api", __name__, url_prefix="/orders")

@apibp.route('/getHighestBid', methods=['GET'])
def getHighestBid():
    if request.headers['API_KEY'] == "3fed75676a43f9f6692c714c22bd323a":
        get = Orders.query.filter_by(asset_id=request.args.get('asset_id')).order_by(Orders.amount.desc()).first()
        buyer = User.query.filter_by(user_id=get.buyer).first()
        return jsonify({
            "status": "success",
            "order_id": get.order_id,
            "buyer": buyer.username,
            "email": buyer.email,
            "phone": buyer.phone_number,
            "amount": get.amount
        })
    return jsonify({
        "status": "failed",
        "error": "Unauthorized"
    })