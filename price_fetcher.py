import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://steamcommunity.com/market/",
}

def get_price(market_hash_name: str, appid: int = 730, currency: int = 5) -> dict:
    url = "https://steamcommunity.com/market/priceoverview/"
    params = {
        "appid": appid,
        "currency": currency,
        "market_hash_name": market_hash_name,
    }
    response = requests.get(url, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    result = get_price("AK-47 | Redline (Field-Tested)")
    print(result)