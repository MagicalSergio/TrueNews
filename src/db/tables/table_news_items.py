from .main_base import MainBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, ForeignKey, Integer
import time


class NewsItemDBEntity(MainBase):
    __tablename__ = "news_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    source_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sources.id", use_alter=True), nullable=True
    )
    published_at: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[int] = mapped_column(
        nullable=False, default=lambda: int(time.time())
    )
