from sqlalchemy import (
    create_engine,
    text,
    String,
    ForeignKey,
)
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from icecream import ic
from typing import List


class BaseMappedClass(DeclarativeBase):
    pass


class UserEntity(BaseMappedClass):
    __tablename__ = "user_entities"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    addresses: Mapped[List["UserAddressEntity"]] = relationship(
        back_populates="addresses"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, last_name={self.last_name})"


class UserAddressEntity(BaseMappedClass):
    __tablename__ = "user_address_entities"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user_entities.id"))
    email_address: Mapped[str] = mapped_column(String(50), nullable=False)
    user: Mapped[UserEntity] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"UserAddress(id={self.id}, user_id={self.user_id}, email_address={self.email_address})"


class DBConn:
    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

        BaseMappedClass.metadata.create_all(self.engine)

        with Session(self.engine) as session:
            result = session.execute(
                text('select name from sqlite_master where type="table" order by name')
            )

            items = result.all()
            ic(items)
