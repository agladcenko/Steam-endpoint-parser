def parse_price(raw: str | None) -> float | None:
    if not raw:
        return None
    cleaned = (
        raw.replace("руб.", "")
        .replace("\xa0", "")
        .replace(" ", "")
        .replace(",", ".")
        .strip()
    )
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_volume(raw: str | None) -> int | None:
    if not raw:
        return None
    cleaned = raw.replace(",", "").replace("\xa0", "").replace(" ", "").strip()
    try:
        return int(cleaned)
    except ValueError:
        return None