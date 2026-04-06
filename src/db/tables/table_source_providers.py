from .main_base import MainBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
import time


class SourceProviderDBEntity(MainBase):
    __tablename__ = "source_providers"

    id: Mapped[int] = mapped_column(primary_key=True)
    system_name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    public_name: Mapped[str] = mapped_column(String(64), nullable=False)
    canonical_url: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[int] = mapped_column(
        nullable=False, default=lambda: int(time.time())
    )
