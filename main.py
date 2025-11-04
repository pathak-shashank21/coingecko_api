import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("COINGECKO_API_KEY")
BASE_URL = "https://api.coingecko.com/api/v3"

headers = {
    "x-cg-demo-api-key": API_KEY
}

def ping():
    """Test connection to CoinGecko API"""
    response = requests.get(f"{BASE_URL}/ping", headers=headers)
    if response.status_code == 200:
        print("Connection successful:", response.json())
    else:
        print("Failed to connect:", response.status_code, response.text)

if __name__ == "__main__":
    ping()
