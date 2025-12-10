from fastapi import FastAPI, Depends
from sqlmodel import SQLModel

from .database import engine, get_session
from .api.routes.evals import router as evals_router


app = FastAPI(title="Vanguard AI Eval Platform", version="0.1.0")


@app.on_event("startup")
async def on_startup() -> None:
    # Create tables on startup for MVP; in production use migrations instead.
    SQLModel.metadata.create_all(bind=engine)


@app.get("/health", tags=["system"])
async def healthcheck():
    return {"status": "ok"}


app.include_router(evals_router, prefix="/v1/evals", tags=["evals"])
