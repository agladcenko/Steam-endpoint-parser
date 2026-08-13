import json
import time
from datetime import datetime

from price_fetcher import get_price
from listing_parser import get_variants
from parsers import parse_price, parse_volume
from exporter import export_to_excel

DELAY = 4
VARIANTS_DELAY = 6


def load_items(path: str = "items.json") -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_prices(items: list[str]) -> list[dict]:
    results = []

    for index, name in enumerate(items, start=1):
        print(f"[{index}/{len(items)}] {name}")
        data = get_price(name)

        if data is None or not data.get("success"):
            print("  не удалось получить данные")
            results.append({"name": name, "lowest": None, "median": None, "volume": None})
        else:
            results.append({
                "name": name,
                "lowest": parse_price(data.get("lowest_price")),
                "median": parse_price(data.get("median_price")),
                "volume": parse_volume(data.get("volume")),
            })
            print(f"  {data.get('lowest_price')}")

        if index < len(items):
            time.sleep(DELAY)

    return results


def collect_variants(items: list[str]) -> list[dict]:
    rows = []

    for index, name in enumerate(items, start=1):
        print(f"[{index}/{len(items)}] варианты: {name}")
        variants = get_variants(name)

        if not variants:
            continue

        for v in variants:
            rows.append({
                "source": name,
                "variant": v["name"],
                "exterior": v["exterior"],
                "min_price": v["min_price"],
            })

        print(f"  найдено вариантов: {len(variants)}")

        if index < len(items):
            time.sleep(VARIANTS_DELAY)

    return rows


if __name__ == "__main__":
    items = load_items()

    print("=== Цены по списку ===")
    prices = collect_prices(items)

    print("\n=== Варианты по состояниям ===")
    variants = collect_variants(items)

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    export_to_excel(prices, variants, f"prices_{stamp}.xlsx")