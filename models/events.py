from typing import Optional, List
from sqlmodel import JSON, SQLModel, Field, Column, Relationship


class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str

    # Внешний ключ, ссылающийся на таблицу user (на поле email)
    user_email: Optional[str] = Field(default=None, foreign_key="user.email")

    # Обратная связь
    owner: Optional["User"] = Relationship(back_populates="events")

    class Config:
        arbitrary_types_allowed = True


class EventUpdate(SQLModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None