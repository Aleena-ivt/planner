from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, BaseModel


class User(SQLModel, table=True):
    email: EmailStr = Field(primary_key=True)
    password: str

    # Связь с событиями (один ко многим)
    events: List["Event"] = Relationship(back_populates="owner")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@Aleena.com",
                "password": "password123",
                "events": []
            }
        }


# Класс для регистрации (без базы данных)
class NewUser(BaseModel):
    email: EmailStr
    password: str


# Класс для входа (без базы данных)
class UserSignIn(BaseModel):
    email: EmailStr
    password: str