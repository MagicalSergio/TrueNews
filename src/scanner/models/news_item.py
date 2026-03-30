from dataclasses import dataclass

@dataclass
class NewsItem:
    url: str
    title: str
    text: str
    timestamp: int
