import requests
import json
import time

API_URL = "http://10.0.2.47:8000/api/retrieve"

payload = {
    "queries": [
        "physician",
        "doctor visit",
        "gyn",
        "medical care"
    ],
    "top_k": 5
}

# -----------------------------
# SEND REQUEST WITH TIMING
# -----------------------------
start = time.perf_counter()
response = requests.post(API_URL, json=payload)
end = time.perf_counter()

latency = end - start

# -----------------------------
# PRINT RESULTS
# -----------------------------
print(f"Status Code: {response.status_code}")
print(f"Time Taken: {round(latency, 4)} sec")

if response.status_code != 200:
    print("\nError Response:")
    print(response.text)
else:
    print("\nAPI Response:\n")
    print(json.dumps(response.json(), indent=2))
