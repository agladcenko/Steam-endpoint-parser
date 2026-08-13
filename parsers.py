def parse_price(raw: str | None) -> float | None:
    """'3 382,64 руб.' -> 3382.64"""
    if not raw:
        return None
    cleaned = (
        raw.replace("руб.", "")
        .replace("\xa0", "")   # неразрывный пробел — Steam его использует
        .replace(" ", "")
        .replace(",", ".")
        .strip()
    )
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_volume(raw: str | None) -> int | None:
    """'133,216' -> 133216 (запятая = разделитель тысяч)"""
    if not raw:
        return None
    cleaned = raw.replace(",", "").replace("\xa0", "").replace(" ", "").strip()
    try:
        return int(cleaned)
    except ValueError:
        return None