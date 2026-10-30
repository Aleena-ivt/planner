from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from database.connection import conn, engine_url
from routes.users import user_router
from routes.events import event_router
import uvicorn
import os

# Импорт моделей для админки
from models.events import Event
from models.users import User

# Импорт для админ-панели
from sqladmin import Admin, ModelView

app = FastAPI()

# Регистрация маршрутов
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

# --- Настройка Админ-панели ---
admin = Admin(app, engine_url, base_url="/admin")

# 1. Отображение для Событий (Events)
class EventAdmin(ModelView, model=Event):
    # Добавили Event.user_email в отображаемые колонки
    column_list = [Event.id, Event.title, Event.location, Event.user_email]
    column_searchable_list = [Event.title, Event.user_email]
    can_export = True

# 2. Отображение для Пользователей (Users)
class UserAdmin(ModelView, model=User):
    column_list = [User.email]  # Используем email, так как id нет
    column_details_exclude_list = [User.password]  # Скрываем пароль в карточке

admin.add_view(EventAdmin)
admin.add_view(UserAdmin)
# --------------------------------

@app.on_event("startup")
def on_startup():
    # Удаляем старую БД, чтобы применилась новая структура (поле user_email)
    if os.path.exists("planner.db"):
        os.remove("planner.db")
    conn()

@app.get("/")
async def home():
    return RedirectResponse(url="/event/")

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)