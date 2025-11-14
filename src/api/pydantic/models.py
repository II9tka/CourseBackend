from typing import Annotated

from pydantic import BaseModel, AfterValidator, Field


def ensure_gte_zero(value: int) -> int:
    if value < 0:
        return 0
    return value


class Pagination(BaseModel):
    limit: int = Field(10, le=4)
    offset: int = Field(0, ge=0)

    # limit: Annotated[int, AfterValidator(ensure_gte_zero)] = Field(10, le=4)
    # offset: Annotated[int, AfterValidator(ensure_gte_zero)] = 0
