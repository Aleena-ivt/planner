from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events_mongo import EventNoSQL

class UserNoSQL(Document):
    email: EmailStr
    password: str
    events: Optional[List[Link[EventNoSQL]]] = []

    class Settings:
        name = "users"

class UserSignInNoSQL(BaseModel):
    email: EmailStr
    password: str