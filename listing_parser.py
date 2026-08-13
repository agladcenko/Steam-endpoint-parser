import json
import time
from urllib.parse import quote

import requests

from price_fetcher import HEADERS

BASE_URL = "https://steamcommunity.com/market/listings/730/"
ANCHOR = "window.SSR.loaderData"


def _extract_loader_data(html: str) -> list | None:
    start = html.find(ANCHOR)
    if start == -1:
        return None

    bracket = html.find("[", start)
    if bracket == -1:
        return None

    try:
        data, _ = json.JSONDecoder().raw_decode(html[bracket:])
    except json.JSONDecodeError:
        return None

    return data


def _find_payload(outer: list) -> dict | None:
    for item in outer:
        if not isinstance(item, str):
            continue
        try:
            parsed = json.loads(item)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict) and "buckets" in parsed:
            return parsed
    return None


def _build_variants(payload: dict) -> list[dict]:
    variants = []
    for bucket in payload.get("buckets") or []:
        raw_price = bucket.get("min_price")
        variants.append({
            "name": bucket.get("bucket_id"),
            "exterior": bucket.get("localized_name_inside_group"),
            "min_price": int(raw_price) / 100 if raw_price and int(raw_price) > 0 else None,
        })
    return variants


def get_variants(
        market_hash_name: str,
        retries: int = 3,
        delay: int = 5,
) -> list[dict] | None:

    url = BASE_URL + quote(market_hash_name)

    for attempt in range(1, retries + 1):
        response = requests.get(url, headers=HEADERS, timeout=20)

        if response.status_code != 200:
            print(f"  страница недоступна ({response.status_code})")
            return None

        outer = _extract_loader_data(response.text)
        payload = _find_payload(outer) if outer else None

        if payload is not None:
            return _build_variants(payload)

        if attempt < retries:
            print(f"  SSR-данные неполные, попытка {attempt}/{retries}")
            time.sleep(delay)

    print("  не удалось получить данные о вариантах")
    return None


if __name__ == "__main__":
    for v in get_variants("AK-47 | Redline (Field-Tested)") or []:
        print(f"{v['exterior']:<32} {v['min_price']}")