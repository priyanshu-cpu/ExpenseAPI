from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserSchema(BaseModel):
    username: str
    email: EmailStr | None = Field(default=None)
    password: str


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class UserCreateResponse(BaseModel):
    message: str
    data: UserOutSchema


class UserLoginSchema(BaseModel):
    username:str
    password: str