import re


def Slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def IsNullOrEmpty(value: str | None) -> bool:
    return value is None or value.strip() == ""
