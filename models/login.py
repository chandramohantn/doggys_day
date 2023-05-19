import uuid
from ..database.db import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Integer, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from data_types import IntEnum, BreedTypes, GenderTypes


class Owner(Base):
    __tablename__ = "owners"

    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    lat = Column(Integer, nullable=False)
    lon = Column(Integer, nullable=False)


class Dog(Base):
    __tablename__ = "dogs"

    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("owners.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    breed = Column(IntEnum(BreedTypes), nullable=False)
    gender = Column(IntEnum(GenderTypes), nullable=False)
    owner = relationship("Owner")


class CareTaker(Base):
    __tablename__ = "caretakers"

    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    lat = Column(Integer, nullable=False)
    lon = Column(Integer, nullable=False)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("owners.id", ondelete="CASCADE"), nullable=False
    )
    caretaker_id = Column(
        UUID(as_uuid=True),
        ForeignKey("caretakers.id", ondelete="CASCADE"),
        nullable=False,
    )
    rating = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    comment = Column(text, nullable=True)
    owner = relationship("Owner")
    caretaker = relationship("CareTaker")


class Boooking(Base):
    __tablename__ = "bookings"

    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("owners.id", ondelete="CASCADE"), nullable=False
    )
    caretaker_id = Column(
        UUID(as_uuid=True),
        ForeignKey("caretakers.id", ondelete="CASCADE"),
        nullable=False,
    )
    dog_id = Column(
        UUID(as_uuid=True), ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False
    )
    date_of_booking = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    start_time = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    end_time = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    instructions = Column(text, nullable=True)
