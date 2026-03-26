from .main_base import MainBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer
import time


class SourceDBEntity(MainBase):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_provider_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("source_providers.id", use_alter=True), nullable=False
    )
    parser_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("parsers.id", use_alter=True), nullable=True
    )
    created_at: Mapped[int] = mapped_column(
        nullable=False, default=lambda: int(time.time())
    )
