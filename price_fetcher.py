import time

import requests

URL = "https://steamcommunity.com/market/priceoverview/"

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


def get_price(
        market_hash_name: str,
        appid: int = 730,
        currency: int = 5,
        retries: int = 3,
) -> dict | None:
    """
    Получает цену предмета со Steam Market.
    При лимите запросов (429) ждёт с увеличивающейся паузой и повторяет.
    При сетевой ошибке — тоже повторяет.
    Возвращает None, если получить данные не удалось.
    """
    params = {
        "appid": appid,
        "currency": currency,
        "market_hash_name": market_hash_name,
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(URL, params=params, headers=HEADERS, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"  сетевая ошибка: {type(e).__name__}")
            if attempt < retries:
                time.sleep(10)
                continue
            return None

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429:
            wait = 60 * attempt
            print(f"  лимит запросов, попытка {attempt}/{retries}, жду {wait} с.")
            time.sleep(wait)
            continue

        print(f"  ошибка {response.status_code}")
        return None

    print("  не удалось получить цену")
    return None