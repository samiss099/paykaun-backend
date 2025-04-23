from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/create-order', methods=['POST'])
def create_order():
    data = request.json

    payload = {
        "customer_mobile": data["mobile"],
        "user_token": "1f7b7cd419b507496aa40de6c19ad599",
        "amount": data["amount"],
        "order_id": data["order_id"],
        "redirect_url": data["redirect_url"],
        "remark1": data.get("remark1", ""),
        "remark2": data.get("remark2", "")
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post("https://www.wkpay.in/api/create-order", data=payload, headers=headers)

    return jsonify(response.json())
