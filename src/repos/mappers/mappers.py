from src.models.bookings_model import BookingsOrm
from src.models.facilities_model import FacilitiesOrm, RoomsFacilitiesOrm
from src.models.hotels_model import HotelsOrm
from src.models.rooms_model import RoomsOrm
from src.models.users_model import UsersOrm
from src.repos.mappers.base_mapper import DataMapper
from src.schemas.bookings_schemas import Booking
from src.schemas.facilities_schemas import Facility, RoomFacility
from src.schemas.hotels_schemas import Hotel
from src.schemas.rooms_schemas import Room
from src.schemas.users_schemas import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility


class RoomFacilitiesDataMapper(DataMapper):
    model = RoomsFacilitiesOrm
    schema = RoomFacility


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User
