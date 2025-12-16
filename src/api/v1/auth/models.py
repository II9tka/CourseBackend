from pydantic import BaseModel, model_validator

from api.v1.user.crypto import context


class UserLoginSchema(BaseModel):
    username: str
    password: str

    def set_password(self):
        self.password = context.hash(self.password)

    @model_validator(mode='after')
    def check_password(self) -> "UserLoginSchema":
        self.set_password()
        return self


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    access_token_expires_in: int
    refresh_token_expires_in: int
