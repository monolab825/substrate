import requests
import json

# Define the JSON-RPC request payload
payload = {
    "jsonrpc": "2.0",
    "method": "chain_getBlock",
    "params": ["0x8c761aab180358ace1e13072aa3c30e9cc3d8f3cdfdd075363b6f62b3f23a222"],
    "id": 1
}

# Define the headers
headers = {
    "Content-Type": "application/json"
}

# Define the URL
url = "http://localhost:9944"

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Check if the request was successful
if response.status_code == 200:
    # Print the response content
    print(response.json()['result']['block']['header'])
else:
    # Print an error message
    print("Error:", response.status_code, response.text)
