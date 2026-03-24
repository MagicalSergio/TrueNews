from datetime import datetime, timezone
from icecream import ic

class DateNormalizer():
    @staticmethod
    def from_iso_8601(str: str):
        return int(datetime.fromisoformat(str).astimezone(timezone.utc).timestamp())
