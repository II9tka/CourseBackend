from pydantic import Field, BaseModel


class CreateUpdateAuthorSchema(BaseModel):
    full_name: str = Field(max_length=128)
    user_id: int | None = None


class AuthorSchema(CreateUpdateAuthorSchema):
    id: int
