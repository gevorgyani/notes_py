from fastapi import FastAPI, Query
from app.api.v1.notes import router as notes_router  #импортируем роутер со всеми маршрутами
from app.core.init_db import init_db

app = FastAPI()


@app.on_event('startup')
async def on_startup():
    await init_db()


app.include_router(notes_router, prefix="/api/v1/notes", tags=["notes"])
