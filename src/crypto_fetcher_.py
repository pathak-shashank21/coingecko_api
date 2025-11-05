# src/crypto_fetcher.py

import requests
import json
from pathlib import Path


def fetch_top_coins(vs_currency="usd", limit=50):
    """
    Fetch top cryptocurrencies by market cap from CoinGecko API.
    Returns a list of dicts containing the selected fields.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": "false",
    }

    print(f"🔍 Fetching top {limit} coins from CoinGecko...")
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return []

    # Required fields for analysis
    required_fields = [
        "id",
        "symbol",
        "current_price",
        "market_cap",
        "market_cap_rank",
        "total_volume",
        "high_24h",
        "low_24h",
        "price_change_percentage_24h",
        "last_updated",
    ]

    # Extract only required fields
    cleaned_data = []
    for coin in data:
        coin_info = {field: coin.get(field) for field in required_fields}
        cleaned_data.append(coin_info)

    print(f"✅ Retrieved {len(cleaned_data)} coins successfully.")
    return cleaned_data


def save_to_json(data, filepath="data/coins.json"):
    """
    Save fetched coin data to JSON file.
    """
    Path(filepath).parent.mkdir(exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"💾 Saved {len(data)} coin records to {filepath}")


def preview_data(data, n=3):
    """
    Print a short preview of the fetched data.
    """
    print("\n📊 Sample Data Preview:")
    print(json.dumps(data[:n], indent=2))


def main():
    """
    Fetch top coin data and save it locally.
    """
    coins = fetch_top_coins(limit=50)
    if coins:
        save_to_json(coins)
        preview_data(coins)
    else:
        print("⚠️ No data fetched. Check API or network connection.")


if __name__ == "__main__":
    main()
