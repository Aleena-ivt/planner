from pydantic import BaseModel
from typing import List

class Event(BaseModel):
    id: int
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Тестовое мероприятие",
                "image": "https://example.com/image.png",
                "description": "Описание тестового события для проверки работы приложения.",
                "tags": ["тест", "событие", "api"],
                "location": "Онлайн"
            }
        }