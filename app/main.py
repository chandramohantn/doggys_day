from fastapi import FastAPI
from database.db import engine
from models import models
from routes import authentication, caretakers, owners


app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(
    authentication.router, tags=["authentication"], prefix="/api/v1/authentication"
)
app.include_router(caretakers.router, tags=["caretaker"], prefix="/api/v1/caretaker")
app.include_router(owners.router, tags=["owner"], prefix="/api/v1/owner")
