from pydantic import BaseModel, EmailStr, SecretStr, model_validator

from .crypto import context


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str
    biography: str | None = None

    def set_password(self):
        self.password = context.hash(self.password)

    @model_validator(mode='after')
    def check_password(self) -> "CreateUserSchema":
        self.set_password()
        return self


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    biography: str | None = None
