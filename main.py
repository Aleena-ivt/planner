from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

# --- Импорты для NoSQL (MongoDB) ---
from database.connection_mongo import initialize_nosql_database
from routes.events_mongo import event_nosql_router
from routes.users_mongo import user_nosql_router

app = FastAPI()

# Подключаем маршруты NoSQL
app.include_router(user_nosql_router, prefix="/user")
app.include_router(event_nosql_router, prefix="/event")

@app.on_event("startup")
async def on_startup():
    # Инициализация MongoDB
    await initialize_nosql_database()

@app.get("/")
async def home():
    return RedirectResponse(url="/docs")

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)