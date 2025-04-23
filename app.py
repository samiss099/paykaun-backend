import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from PayKaun Backend!"

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PAYKAUN_API_KEY = "1f7b7cd419b507496aa40de6c19ad599"  # Get this from PayKaun Dashboard

@app.route('/create-payment', methods=['POST'])
def create_payment():
    data = request.json
    amount = data.get("amount")
    order_id = data.get("order_id")
    name = data.get("name")

    payload = {
        "amount": amount,
        "name": name,
        "orderid": order_id,
    }

    headers = {
        "Authorization": f"Bearer {PAYKAUN_API_KEY}"
    }

    res = requests.post("https://wkapi.paykass.in/api/upi/create", json=payload, headers=headers)
    
    if res.status_code == 200:
        return jsonify(res.json())
    else:
        return jsonify({"error": "Failed to create payment", "details": res.text}), 400
