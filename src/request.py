import requests
import os
from dotenv import load_dotenv

url = "https://api.akahu.io/v1/transactions"

load_dotenv()
appToken = os.getenv("APP_TOKEN")
token = os.getenv("TOKEN")

# Define the headers dictionary
headers = {
    "Authorization": f"Bearer {token}",
    "X-Akahu-Id": appToken,
    "Content-Type": "application/json"
}

params = {
    "start": "2026-05-07T23:59:59.999+13:00",
    "end": "2026-05-14T23:59:59.999+13:00"
}

# Pass the headers into the GET request
response = requests.get(url, headers=headers, params=params)
print(response)
data = response.json()

for tx in data["items"]:
    print("-" * 60)
    print(f"Date:        {tx['date']}")
    print(f"Description: {tx['description']}")
    print(f"Amount:      ${tx['amount']}")
    print(f"Balance:     ${tx['balance']}")
    print(f"Type:        {tx['type']}")

    if "merchant" in tx:
        print(f"Merchant:    {tx['merchant']['name']}")

    if "category" in tx:
        print(f"Category:    {tx['category']['name']}")

    if "meta" in tx:
        print(f"Meta:        {tx['meta']}")
