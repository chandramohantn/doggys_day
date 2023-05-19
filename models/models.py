import uuid
from database.db import Base
from sqlalchemy import Column, String, Integer, DateTime, TEXT, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


owner_booking = Table(
    "owner_booking_association",
    Base.metadata,
    Column("owner_id", ForeignKey("owners.id")),
    Column("booking_id", ForeignKey("bookings.id")),
)


caretaker_booking = Table(
    "caretaker_booking_association",
    Base.metadata,
    Column("caretaker_id", ForeignKey("caretakers.id")),
    Column("booking_id", ForeignKey("bookings.id")),
)


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
    pet_obj = relationship("Pet", back_populates="owner_obj")
    booking_obj = relationship(
        "Booking", secondary=owner_booking, back_populates="owner_obj"
    )


class Pet(Base):
    __tablename__ = "pets"

    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    breed = Column(String)
    gender = Column(String)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("owners.id"))
    owner_obj = relationship("Owner", back_populates="pet_obj")


class Caretaker(Base):
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
    booking_obj = relationship(
        "Booking", secondary=caretaker_booking, back_populates="caretaker_obj"
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    caretaker_id = Column(UUID(as_uuid=True), ForeignKey("caretakers.id"))
    author_id = Column(UUID(as_uuid=True), ForeignKey("owners.id"))
    date_of_booking = Column(DateTime, nullable=False)
    instruction = Column(TEXT, nullable=True)
    owner_obj = relationship(
        "Owner", secondary=owner_booking, back_populates="booking_obj"
    )
    caretaker_obj = relationship(
        "Caretaker", secondary=caretaker_booking, back_populates="booking_obj"
    )
    review_obj = relationship("Review", back_populates="booking_obj")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"))
    rating = Column(Integer, nullable=False)
    date_of_review = Column(DateTime, nullable=False)
    comment = Column(TEXT, nullable=True)
    booking_obj = relationship("Booking", back_populates="review_obj")
