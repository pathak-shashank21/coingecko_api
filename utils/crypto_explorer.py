import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.coingecko.com/api/v3"
API_KEY = os.getenv("COINGECKO_API_KEY")
HEADERS = {"x-cg-demo-api-key": API_KEY} if API_KEY else None

CACHE_FILE = Path("data/explorer_cache.json")


def _get(url: str, params: Optional[Dict] = None) -> Any:
    """Safe GET with minimal retries."""
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] GET failed for {url}: {e}")
        return None


def check_connection() -> bool:
    """Ping API to check if endpoint works."""
    url = f"{BASE_URL}/ping"
    data = _get(url)
    if data and "gecko_says" in data:
        print(" API Connection OK:", data["gecko_says"])
        return True
    else:
        print(" API Connection failed.")
        return False


def get_coin_list(limit: int = 20, force_refresh: bool = False) -> List[Dict]:
    """Fetch list of all supported coins (cached)."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

    if CACHE_FILE.exists() and not force_refresh:
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
            if "coins" in cache:
                print(" Loaded coins list from cache.")
                return cache["coins"]

    url = f"{BASE_URL}/coins/list"
    data = _get(url)
    if not data:
        return []
    # Limit preview
    coins_preview = data[:limit]
    print(f" Retrieved {len(data)} total coins, showing first {limit}:")
    for c in coins_preview:
        print(f" - {c['id']:20s} | {c['symbol']:6s} | {c['name']}")
    # Cache
    with open(CACHE_FILE, "w") as f:
        json.dump({"coins": data, "timestamp": time.time()}, f, indent=2)
    return data


def inspect_market_fields(vs_currency="usd", per_page=5):
    """Fetch /coins/markets for a few coins and show columns/fields."""
    url = f"{BASE_URL}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1,
    }
    data = _get(url, params=params)
    if not data:
        print(" No data returned.")
        return
    sample = data[0]
    print("\n Sample Coin Data:")
    print(json.dumps(sample, indent=2))
    print("\n Available Columns:")
    for k in sample.keys():
        print(" -", k)


def fetch_single_coin(coin_id="bitcoin"):
    """Fetch and print detailed single coin info safely."""
    url = f"{BASE_URL}/coins/{coin_id}"
    params = {"localization": "false"}
    d = _get(url, params)
    if not d:
        return
    print(f"\n {coin_id.upper()} Info Snapshot:")
    print("Name:", d.get("name"))
    print("Symbol:", d.get("symbol"))
    print("Market data keys:", list(d.get("market_data", {}).keys())[:10])


def explorer_summary():
    """Quick full check summary."""
    print("=== CoinGecko API Explorer ===\n")
    if not check_connection():
        return
    print("\n Step 1: Coin List Preview")
    get_coin_list(limit=10)

    print("\n Step 2: Market Data Columns")
    inspect_market_fields(per_page=3)

    print("\n Step 3: Single Coin Sample")
    fetch_single_coin("bitcoin")

    print("\n Explorer complete. Use crypto_fetcher.py next.")
    

if __name__ == "__main__":
    explorer_summary()
