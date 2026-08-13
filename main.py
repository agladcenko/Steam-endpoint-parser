import json
import time

from price_fetcher import get_price

DELAY = 4  


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
                "lowest": data.get("lowest_price"),
                "median": data.get("median_price"),
                "volume": data.get("volume"),
            })
            print(f"  {data.get('lowest_price')}")

        if index < len(items):
            time.sleep(DELAY)

    return results


if __name__ == "__main__":
    items = load_items()
    prices = collect_prices(items)
    print(f"\nСобрано: {len(prices)} позиций")