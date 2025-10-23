from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, func
from datetime import date, datetime

from src.database import Base


class BookingsOrm(Base):
	__tablename__ = "bookings"

	id: Mapped[int] = mapped_column(primary_key=True)
	room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	date_from: Mapped[date]
	date_to: Mapped[date]
	price: Mapped[int]
	created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
