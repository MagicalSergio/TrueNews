from datetime import datetime, timedelta


def calculate_expiry(past_ts: int, now_ts: int, interval: int) -> datetime:
    """
    past_ts: прошлый POSIX timestamp
    now_ts:  текущий POSIX timestamp
    interval: интервал в минутах
    """
    diff_minutes = (now_ts - past_ts) / 60

    if diff_minutes < interval:
        return datetime.fromtimestamp(past_ts) + timedelta(minutes=interval)
    else:
        return datetime.now()
