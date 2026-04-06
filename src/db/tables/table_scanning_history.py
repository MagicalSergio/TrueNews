from .main_base import MainBase
from sqlalchemy.orm import Mapped, mapped_column
import time


class ScanningHistoryDBEntity(MainBase):
    __tablename__ = "scanning_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[int] = mapped_column(
        nullable=False,
        default=lambda: int(time.time()),
    )
