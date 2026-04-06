from datetime import datetime, timezone
from icecream import ic
import re

MONTHS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}


class DateNormalizer:
    @staticmethod
    def normalize(date_str: str, base_date: datetime | None = None) -> int:
        if re.match(r"\d{4}-\d{2}-\d{2}T", date_str):
            return DateNormalizer.from_iso_8601(date_str)

        if re.match(r"^\d{2}\s+\S+,\s+\d{2}:\d{2}$", date_str):
            return DateNormalizer.from_ru_short(date_str, base_date)

        if any(month in date_str for month in MONTHS):
            return DateNormalizer.from_ru_verbose(date_str)

        if re.match(r"^\d{2}:\d{2}$", date_str):
            return DateNormalizer.from_time_only(date_str, base_date)

        raise ValueError(f"Неизвестный формат даты: {date_str}")

    # 2026-03-26T04:05:17+03:00  ->  1774487117
    @staticmethod
    def from_iso_8601(str: str):
        return int(datetime.fromisoformat(str).astimezone(timezone.utc).timestamp())

    # 28 марта 2026 года, 22:36  ->  1774487117
    @staticmethod
    def from_ru_verbose(str: str) -> int:
        parts = str.replace(",", "").split()
        day, month, year, _, time = parts
        hour, minute = time.split(":")
        dt = datetime(int(year), MONTHS[month], int(day), int(hour), int(minute))
        return int(dt.timestamp())

    # "18:24" -> 1774487117
    @staticmethod
    def from_time_only(str: str, base_date: datetime | None = None) -> int:
        base = base_date or datetime.now()
        hour, minute = str.split(":")
        dt = base.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
        return int(dt.timestamp())

    # "05 апреля, 23:27" -> 1774487117
    @staticmethod
    def from_ru_short(str: str) -> int:
        base = datetime.now()
        parts = str.replace(",", "").split()
        day, month, time = parts
        hour, minute = time.split(":")
        dt = datetime(base.year, MONTHS[month], int(day), int(hour), int(minute))
        return int(dt.timestamp())
