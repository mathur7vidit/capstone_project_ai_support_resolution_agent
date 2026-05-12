from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.agent import run_agent
from app.logger import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Backend startup complete")
    yield
    logging.info("Backend shutdown complete")


app = FastAPI(
    title="AI Support Resolution Agent API",
    version="1.0.0",
    lifespan=lifespan
)


class UserRequest(BaseModel):
    query: str


@app.get("/")
def home():

    return {
        "message": "AI Support Resolution Agent Running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "backend"
    }


@app.get("/ready")
def ready():

    return {
        "status": "ready"
    }


@app.post("/chat")
def chat(request: UserRequest):

    response = run_agent(request.query)

    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):

    logging.exception("Unhandled API error")

    return JSONResponse(
        status_code=500,
        content={
            "response": "The service is temporarily unavailable. Please try again shortly."
        }
    )
