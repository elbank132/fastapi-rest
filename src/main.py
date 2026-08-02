from fastapi import FastAPI

from . import models
from .database import engine

from .routers import users, pets

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pets & Users API",
    description="A complete REST API built with FastAPI, SQLAlchemy, and Pydantic",
    version="1.0.0"
)


app.include_router(users.router)
app.include_router(pets.router)

#fix: if not necessery remove
@app.get("/")
def root():
    return {"message": "Server is running! Navigate to /docs for the interactive API documentation."}