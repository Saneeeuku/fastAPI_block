from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime

from src.database import Base


class BookingsORM(Base):
	__tablename__ = "bookings"

	id: Mapped[int] = mapped_column(primary_key=True)
	room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	date_from: Mapped[datetime] = mapped_column(DateTime(timezone=True))
	date_to: Mapped[datetime] = mapped_column(DateTime(timezone=True))
	price: Mapped[int]

	# @hybrid_property
	# def total_cost(self):
	# 	return self.price * (self.date_to - self.date_from).days
