from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime, timezone
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()


class Feedback(BaseModel):
    username: str
    message: str


feedbacks = []


@app.post("/feedback")
def receive_feedback(feedback: Feedback):
    entry = {
        "username": feedback.username,
        "message": feedback.message,
        "timestamp": datetime.now(datetime.UTC)
    }
    feedbacks.append(entry)
    return {"status": "received", "entry": entry}


@app.get("/feedback")
def get_feedback():
    return feedbacks

app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/")
def get_form():
    return FileResponse("public/index.html")