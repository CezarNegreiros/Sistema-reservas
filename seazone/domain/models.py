from datetime import date, datetime

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Property:
    __tablename__ = 'properties'

    id: Mapped[int] = mapped_column(
        Integer,
        init=False,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    address_street: Mapped[str] = mapped_column(String(50), nullable=False)
    address_number: Mapped[str] = mapped_column(String(5), nullable=False)
    address_neighborhood: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    address_city: Mapped[str] = mapped_column(String(50), nullable=False)
    address_state: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    rooms: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_night: Mapped[float] = mapped_column(Float, nullable=False)

    reservations = relationship(
        'Reservation', back_populates='property', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class Reservation:
    __tablename__ = 'reservation'

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    property_id: Mapped[int] = mapped_column(ForeignKey('properties.id'))
    client_name: Mapped[str] = mapped_column(String(50), nullable=False)
    client_email: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    guests_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)

    property = relationship('Property', back_populates='reservations')


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True, index=True
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[date] = mapped_column(Date, default=datetime.now())
