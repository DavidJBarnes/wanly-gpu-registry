import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.heartbeat_monitor import heartbeat_monitor
from app.routes.workers import router as workers_router

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(heartbeat_monitor())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="wanly-gpu-registry", lifespan=lifespan)
app.include_router(workers_router)
