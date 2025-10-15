from typing import TypeVar

from pydantic import BaseModel

from src.database import Base

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data_from_db):
        return cls.schema.model_validate(data_from_db, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data_from_schema, exclude_unset_and_none: bool = False):
        return cls.db_model(**data_from_schema.model_dump(exclude_unset=exclude_unset_and_none,
                                                          exclude_none=exclude_unset_and_none))
