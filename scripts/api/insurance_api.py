from flask import Flask, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

class InsuranceAPI:
    def __init__(self):
        self.policies = []

    def generate_policy(self):
        return {
            "policy_id": random.randint(1000, 9999),
            "customer_name": random.choice(["Alice", "Bob", "Charlie"]),
            "premium_amount": round(random.uniform(5000, 20000), 2),
            "status": random.choice(["Active", "Expired"]),
            "issued_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_policies(self):
        return jsonify(self.policies)

    def create_policy(self, payload):
        new_policy = {
            "policy_id": random.randint(1000, 9999),
            "customer_name": payload.get("customer_name", "Unknown"),
            "premium_amount": payload.get("premium_amount", 0),
            "status": payload.get("status", "Active"),
            "issued_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.policies.append(new_policy)
        return jsonify(new_policy), 201

api_handler = InsuranceAPI()

@app.route("/")
def home():
    return "✅ Insurance API is running!"

@app.route("/insurance", methods=["GET"])
def get_insurance():
    return api_handler.get_policies()

@app.route("/insurance", methods=["POST"])
def post_insurance():
    payload = request.get_json()
    return api_handler.create_policy(payload)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
