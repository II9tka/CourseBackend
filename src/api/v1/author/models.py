from pydantic import Field, BaseModel


class CreateUpdateAuthorSchema(BaseModel):
    user_id: int
    full_name: str = Field(max_length=128)


class AuthorSchema(CreateUpdateAuthorSchema):
    id: int
