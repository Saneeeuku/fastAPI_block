from src.models.facilities_model import FacilitiesOrm
from src.repos.base_repo import BaseRepository
from src.schemas.facilities_schemas import Facility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility
