from datetime import datetime

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from src.repos.base_repo import BaseRepository
from src.models.bookings_model import BookingsORM
from src.schemas.bookings_schemas import Booking, BookingAdd


class BookingsRepository(BaseRepository):
	model = BookingsORM
	schema = Booking
