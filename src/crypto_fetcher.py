# src/crypto_fetcher.py
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE_URL = "https://api.coingecko.com/api/v3"


def fetch_coin_data(coin_id, retries=3, wait_between_calls=60):
    """Fetch detailed data for a single coin from CoinGecko, waiting 1 minute between calls."""
    url = f"{BASE_URL}/coins/{coin_id}"
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                m = data.get("market_data", {})
                print(f" [{coin_id}] fetched successfully. Waiting {wait_between_calls}s before next call...")
                time.sleep(wait_between_calls)  # wait 1 minute after *each* successful call
                return {
                    "id": data.get("id"),
                    "symbol": data.get("symbol"),
                    "name": data.get("name"),
                    "current_price": m.get("current_price", {}).get("usd"),
                    "market_cap": m.get("market_cap", {}).get("usd"),
                    "market_cap_rank": data.get("market_cap_rank"),
                    "total_volume": m.get("total_volume", {}).get("usd"),
                    "high_24h": m.get("high_24h", {}).get("usd"),
                    "low_24h": m.get("low_24h", {}).get("usd"),
                    "price_change_percentage_24h": m.get("price_change_percentage_24h"),
                    "last_updated": data.get("last_updated"),
                }

            elif response.status_code == 429:
                print(f" [{coin_id}] Rate limited. Sleeping {wait_between_calls}s...")
                time.sleep(wait_between_calls)

            else:
                print(f" [{coin_id}] HTTP {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f" [{coin_id}] Error: {e}")
            time.sleep(wait_between_calls)

    print(f" [{coin_id}] Failed after {retries} retries.")
    return None


def fetch_all_coins(coin_ids):
    """Fetch multiple coins using ThreadPoolExecutor (effectively sequential due to delay)."""
    results = []
    print(f" Fetching {len(coin_ids)} coins (waiting 60s between each call)...")
    with ThreadPoolExecutor(max_workers=1) as executor:  # single worker for safety
        futures = [executor.submit(fetch_coin_data, cid) for cid in coin_ids]
        for future in as_completed(futures):
            data = future.result()
            if data:
                results.append(data)
    print(f" Successfully fetched {len(results)} / {len(coin_ids)} coins.")
    return results


def main():
    # Step 1: Get top 50 coin IDs
    print(" Getting top 50 coin IDs...")
    url = f"{BASE_URL}/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 50, "page": 1}
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    coin_ids = [coin["id"] for coin in response.json()]

    # Step 2: Fetch all coins (with enforced delay)
    all_data = fetch_all_coins(coin_ids)

    # Step 3: Save results
    Path("data").mkdir(exist_ok=True)
    with open("data/coins.json", "w") as f:
        json.dump(all_data, f, indent=2)
    print(" Saved all data to data/coins.json")

    # Step 4: Preview
    print("\nFirst 3 records:")
    print(json.dumps(all_data[:3], indent=2))


if __name__ == "__main__":
    main()
