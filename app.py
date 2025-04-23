import os
import requests
import qrcode
import io
import base64
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Replace with your real PayKaun API key
PAYKAUN_API_KEY = "1f7b7cd419b507496aa40de6c19ad599"

@app.route('/')
def home():
    return "Hello from PayKaun Backend!"

@app.route('/create-order', methods=['POST'])
def create_order():
    data = request.json

    payload = {
        "customer_mobile": data["mobile"],
        "user_token": PAYKAUN_API_KEY,
        "amount": data["amount"],
        "order_id": data["order_id"],
        "redirect_url": data["redirect_url"],
        "remark1": data.get("remark1", ""),
        "remark2": data.get("remark2", "")
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post("https://www.wkpay.in/api/create-order", data=payload, headers=headers)
    return jsonify(response.json())

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

@app.route("/pay")
def payment_page():
    name = request.args.get("name")
    amount = request.args.get("amount")
    order_id = request.args.get("order_id")

    payload = {
        "amount": amount,
        "name": name,
        "orderid": order_id
    }

    headers = {
        "Authorization": f"Bearer {PAYKAUN_API_KEY}"
    }

    res = requests.post("https://wkapi.paykass.in/api/upi/create", json=payload, headers=headers)
    data = res.json()

    payment_link = data.get("payment_url", "#")

    # Generate QR code as base64 image
    qr = qrcode.make(payment_link)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    html = f"""
    <html>
    <head>
        <title>Pay via UPI</title>
        <style>
            body {{
                font-family: sans-serif;
                text-align: center;
                padding: 40px;
            }}
            .button {{
                background: #4CAF50;
                color: white;
                padding: 12px 20px;
                text-decoration: none;
                border-radius: 6px;
                display: inline-block;
                margin-top: 20px;
            }}
            .qr-code {{
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <h2>Pay ₹{amount} for Order #{order_id}</h2>
        <p>Hi {name}, click below to pay via UPI:</p>
        <a href="{payment_link}" class="button">Pay Now via UPI</a>
        <div class="qr-code">
            <p>Or scan this QR code:</p>
            <img src="data:image/png;base64,{qr_base64}" width="200" height="200"/>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
