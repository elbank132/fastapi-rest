from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

from .routers import users, pets
from .logger import logger

app = FastAPI(
    title="User & Pet Management API",
    version="1.0.0",
    description="A REST API for managing users and their associated pets."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

@app.middleware("http")
async def global_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    
    except Exception as e:
        
        logger.error(
            f"Unexpected server crash on {request.method} {request.url.path}: {str(e)}", 
            exc_info=True
        )
        
        return JSONResponse(
            status_code=510,
            content={"detail": "Internal Server Error. Please contact support."},
            headers={"Access-Control-Allow-Origin": "*"} 
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Payload validation failed on {request.method} {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Invalid request payload", 
            "errors": exc.errors()
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP {exc.status_code} returned on {request.method} {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

app.include_router(users.router)
app.include_router(pets.router)