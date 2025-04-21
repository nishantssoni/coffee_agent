from fastapi import FastAPI
import models
from database import engine
from routers import users, auth, chats
from agents import AgentProtocol
import os


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(chats.router)

# routes
@app.get("/")
async def root():
    return {"message": "hey there"}

