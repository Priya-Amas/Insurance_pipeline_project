import os
import json
import requests
from datetime import datetime

# Folder to store the generated JSON files
OUTPUT_FOLDER = "data/json"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# API endpoint
API_URL = "http://localhost:5000/insurance"

# How many records/files to create
NUM_FILES = 5

for i in range(NUM_FILES):
    payload = {
        "customer_name": f"User_{i+1}",
        "premium_amount": 10000 + i * 100,
        "status": "Active" if i % 2 == 0 else "Expired"
    }

    # Send POST request to API
    response = requests.post(API_URL, json=payload)
    if response.status_code == 201:
        data = response.json()
        # Save each response as a separate JSON file
        filename = f"insurance_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i+1}.json"
        with open(os.path.join(OUTPUT_FOLDER, filename), "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ File created: {filename}")
    else:
        print(f"❌ Failed to POST record {i+1}: {response.status_code}")
