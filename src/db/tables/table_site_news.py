from .main_base import MainBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, ForeignKey
import time


class SiteNewsItemDBEntity(MainBase):
    __tablename__ = "site_news"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    source_provider_id: Mapped[int] = mapped_column(
        ForeignKey("source_providers.id"), nullable=False
    )
    published_at: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[int] = mapped_column(nullable=False, default=lambda: int(time.time()))
