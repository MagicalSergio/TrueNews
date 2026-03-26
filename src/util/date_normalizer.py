from datetime import datetime, timezone
from icecream import ic

class DateNormalizer():
    # 2026-03-26T04:05:17+03:00  ->  1774487117
    @staticmethod
    def from_iso_8601(str: str):
        return int(datetime.fromisoformat(str).astimezone(timezone.utc).timestamp())
