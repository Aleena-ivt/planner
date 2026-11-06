from beanie import Document
from pydantic import BaseModel
from typing import Optional, List

class EventNoSQL(Document):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str
    user_email: Optional[str] = None

    class Settings:
        name = "events"

class EventUpdateNoSQL(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None