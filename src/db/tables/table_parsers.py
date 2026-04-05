from .main_base import MainBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON
import time


class ParserDBEntity(MainBase):
    __tablename__ = "parsers"

    id: Mapped[int] = mapped_column(primary_key=True)
    system_name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    module: Mapped[str] = mapped_column(String(64), nullable=False)
    kwargs_json: Mapped[str | None] = mapped_column(JSON, nullable=True)
    source: Mapped["SourceDBEntity"] = relationship(back_populates="parser")
    created_at: Mapped[int] = mapped_column(
        nullable=False, default=lambda: int(time.time())
    )

    def __repr__(self):
        return f"Parser #{self.id}: {self.system_name}"
