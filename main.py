from fastapi import FastAPI

from config import settings
from database.MessagesDB import MessagesDB
from database.utils import Message

app = FastAPI()
db = MessagesDB(settings.database_url)
@app.get("/")
def index():
    return {"message": settings.greeting}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/messages")
def list_messages():
    return db.get_all_messages()


@app.post("/messages")
def add_message(message: Message):
    db.add_message(message)

    return {"ok": True}
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)