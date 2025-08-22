from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime, timezone
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, select
import os


#настройка БД

DB_HOST = "db"
DB_PORT = "5432"
DB_NAME = "feedback"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


Base = declarative_base()


class FeedbackCreate(BaseModel):
    username: str
    message: str

#модель таблицы



class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    message = Column(Text)


#инициализация фаст апи
app = FastAPI()

#разадём папку public for HTML/CSS/JS
app.mount("/static", StaticFiles(directory="public"), name="static")

#маршруты

@app.get("/")
async def get_form():
    return FileResponse("public/index.html")

@app.post("/feedback")
async def create_feedback(data: FeedbackCreate, session: AsyncSession = Depends(async_session)):
    feedback = Feedback(username=data.username, message=data.message)
    session.add(feedback)
    await session.commit()
    return {"status": "ok"}

@app.get("/feedback")
async def get_feedback(session: AsyncSession = Depends(async_session)):
    result = await session.execute(select(Feedback))
    feedback_list = result.scalars().all()
    return feedback_list

#создание таблиц при старте

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
