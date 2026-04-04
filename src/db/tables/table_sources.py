from .main_base import MainBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Boolean
import time


class SourceDBEntity(MainBase):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    system_name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    source_provider_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("source_providers.id", use_alter=True),
        nullable=False,
    )
    source_provider: Mapped["SourceProviderDBEntity"] = relationship(back_populates="sources")
    parser_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("parsers.id", use_alter=True),
        nullable=True,
    )
    created_at: Mapped[int] = mapped_column(
        nullable=False,
        default=lambda: int(time.time()),
    )
    enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="1",
        nullable=False,
    )
