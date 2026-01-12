from pydantic import (
    BaseModel,
    model_validator,
    EmailStr,
    Field,
)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    superuser: bool
    first_name: str
    last_name: str
    patronymic: str

    model_config = {
        "from_attributes": True,
    }


class UserCreate(BaseModel):
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    patronymic: str = Field(max_length=255)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=4, max_length=255)
    password2: str = Field(max_length=255)

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.password2:
            raise ValueError("Passwords do not match")
        return self


class UserUpdate(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None

    model_config = {
        "from_attributes": True,
    }


class UserLoginSchema(BaseModel):
    email: str
    password: str


class JWTToken(BaseModel):
    token: str
    token_type: str


class OAuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
