from .main_base import MainBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
import time


class ParserDBEntity(MainBase):
    __tablename__ = "parsers"

    id: Mapped[int] = mapped_column(primary_key=True)
    system_name: Mapped[str] = mapped_column(String(64), nullable=False)
    module: Mapped[str] = mapped_column(String(64), nullable=False)
    kwargs_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[int] = mapped_column(
        nullable=False, default=lambda: int(time.time())
    )
