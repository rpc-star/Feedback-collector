from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime, timezone

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
