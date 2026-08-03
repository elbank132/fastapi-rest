from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, pets
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pets & Users API",
    description="A complete REST API built with FastAPI, SQLAlchemy, and Pydantic",
    version="1.0.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    
    is_json_error = any(error.get("type") == "json_invalid" for error in errors)
    
    if is_json_error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Malformed JSON payload. Please check for missing brackets, quotes, or trailing commas.",
                "details": errors
            }
        )
        
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors}
    )


app.include_router(users.router)
app.include_router(pets.router)

#fix: if not necessery remove
@app.get("/")
def root():
    return {"message": "Server is running! Navigate to /docs for the interactive API documentation."}