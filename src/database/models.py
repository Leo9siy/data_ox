from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Auto(Base):
    __tablename__ = "autos"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    url: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[str] = mapped_column(String)
    price_usd: Mapped[int]
    odometer: Mapped[int] = mapped_column(Integer) #(число, потрібно перевести 95 тис. у 95000 і записати як число)

    username: Mapped[str] = mapped_column(String)
    phone_number: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str] = mapped_column(String)
    images_count: Mapped[int] = mapped_column(Integer)

    car_number: Mapped[str] = mapped_column(String)
    car_vin: Mapped[str] = mapped_column(String)
    datetime_found: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
