from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine
from models import models
from routes import authentication, caretakers, owners, administrator


app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict the origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

models.Base.metadata.create_all(engine)

app.include_router(administrator.router, tags=["admin"], prefix="/api/v1/admin")
app.include_router(
    authentication.router, tags=["authentication"], prefix="/api/v1/authentication"
)
app.include_router(caretakers.router, tags=["caretaker"], prefix="/api/v1/caretaker")
app.include_router(owners.router, tags=["owner"], prefix="/api/v1/owner")
