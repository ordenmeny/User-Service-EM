from pydantic import (
    BaseModel,
    model_validator,
    EmailStr,
    Field,
)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool = True
    first_name: str
    last_name: str

    model_config = {
        'from_attributes': True,
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


class UserLoginSchema(BaseModel):
    email: str
    password: str


# user = UserCreate(
#     first_name="Test name",
#     last_name="Test surname",
#     patronymic="Test patronymic",
#     email="test@example.com",
#     password="securepassword123",
#     password2="securepassword1234",
# )
#
#
# user_dict = user.model_dump()  # to python-dict.
# print(user_dict)
# model_user = UserCreate(**dict(user_dict))  # to pydantic model.
