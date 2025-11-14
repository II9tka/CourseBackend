from typing import Any, Union
from pydantic import BaseModel as _BaseModel

from .models import Pagination


class BaseModel(_BaseModel):
    @classmethod
    def paginate(cls, pagination: Pagination, db: dict[int, Any], **kwargs) -> list[Union[dict, "BaseModel"]]:
        length = len(db)

        if pagination.offset >= length:
            return []

        objects = list(db.values())
        objects = cls.apply_filters(objects, **kwargs)

        paginated_objects: list[BaseModel] = objects[pagination.offset:pagination.offset + pagination.limit]
        return [paginated_object.model_dump(mode='json') for paginated_object in paginated_objects]

    @staticmethod
    def apply_filters(objects, **kwargs):
        return objects
