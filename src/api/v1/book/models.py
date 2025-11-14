from enum import Enum

from api.pydantic.mixins import BaseModel


class Genre(Enum):
    Horror = "horror"
    Porn = "porn"


class ListBook(BaseModel):
    id: int | None = None
    title: str
    author: str

    @staticmethod
    def apply_filters(objects, **kwargs):
        genre = kwargs.pop("genre", None)

        if not genre:
            return objects

        filtered_objects = []

        for object_ in objects:
            if object_.genre == genre:
                filtered_objects.append(object_)

        return filtered_objects

class Book(ListBook):
    genre: Genre
    year: int
    price: int
