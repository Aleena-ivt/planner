from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Any, List
from pydantic_settings import BaseSettings
from models.users_mongo import UserNoSQL
from models.events_mongo import EventNoSQL

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    class Config:
        env_file = ".env"

settings = Settings()

async def initialize_nosql_database():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(),
        document_models=[EventNoSQL, UserNoSQL]
    )

class DatabaseNoSQL:
    def __init__(self, model):
        self.model = model
    async def save(self, document) -> None:
        await document.create()
    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        return doc if doc else False
    async def get_all(self) -> List[Any]:
        return await self.model.find_all().to_list()
    async def update(self, id: PydanticObjectId, body) -> Any:
        des_body = body.model_dump(exclude_unset=True)
        update_query = {"$set": {k: v for k, v in des_body.items() if v is not None}}
        doc = await self.get(id)
        if not doc: return False
        await doc.update(update_query)
        return doc
    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc: return False
        await doc.delete()
        return True