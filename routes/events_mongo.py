from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from database.connection_mongo import DatabaseNoSQL
from models.events_mongo import EventNoSQL, EventUpdateNoSQL
from typing import List

# Вот здесь создается роутер с нужным именем
event_nosql_router = APIRouter(tags=["Events (MongoDB)"])
event_db = DatabaseNoSQL(EventNoSQL)

@event_nosql_router.get("/", response_model=List[EventNoSQL])
async def get_all_events():
    return await event_db.get_all()

@event_nosql_router.post("/new")
async def create_event(body: EventNoSQL):
    await event_db.save(body)
    return {"message": "Event created in MongoDB successfully"}

@event_nosql_router.get("/{id}", response_model=EventNoSQL)
async def get_event(id: PydanticObjectId):
    event = await event_db.get(id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@event_nosql_router.put("/edit/{id}", response_model=EventNoSQL)
async def update_event(id: PydanticObjectId, body: EventUpdateNoSQL):
    event = await event_db.update(id, body)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@event_nosql_router.delete("/delete/{id}")
async def delete_event(id: PydanticObjectId):
    deleted = await event_db.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted from MongoDB successfully"}