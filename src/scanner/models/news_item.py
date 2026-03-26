class NewsItem:
    url: str
    title: str
    text: str
    timestamp: int

    def __init__(self, url: str, title: str, text: str, timestamp: int):
        self.url = url
        self.title = title
        self.text = text
        self.timestamp = timestamp

    def __str__(self):
        return (
            f"News(\n"
            f"    url={self.url}\n"
            f"    title={self.title}\n"
            f"    text={self.text[:100]}...\n"
            f"    timestamp={self.timestamp}...\n"
            f")"
        )
