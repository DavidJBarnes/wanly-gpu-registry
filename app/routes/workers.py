import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Worker
from app.schemas import WorkerHeartbeat, WorkerRegister, WorkerResponse, WorkerStatusUpdate

router = APIRouter()


@router.post("/workers", response_model=WorkerResponse, status_code=201)
async def register_worker(body: WorkerRegister, db: AsyncSession = Depends(get_db)):
    # Upsert: if friendly_name already exists, reclaim that row
    result = await db.execute(
        select(Worker).where(Worker.friendly_name == body.friendly_name)
    )
    worker = result.scalar_one_or_none()
    if worker:
        worker.hostname = body.hostname
        worker.ip_address = body.ip_address
        worker.comfyui_running = body.comfyui_running
        worker.status = "online-idle"
        worker.last_heartbeat = datetime.now(timezone.utc)
    else:
        worker = Worker(
            friendly_name=body.friendly_name,
            hostname=body.hostname,
            ip_address=body.ip_address,
            comfyui_running=body.comfyui_running,
        )
        db.add(worker)
    await db.commit()
    await db.refresh(worker)
    return worker


@router.delete("/workers/{worker_id}", status_code=204)
async def deregister_worker(
    worker_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    worker = await db.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    await db.delete(worker)
    await db.commit()


@router.post("/workers/{worker_id}/drain", response_model=WorkerResponse)
async def drain_worker(
    worker_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    worker = await db.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    if worker.status == "offline":
        raise HTTPException(status_code=400, detail="Cannot drain an offline worker")
    worker.status = "draining"
    await db.commit()
    await db.refresh(worker)
    return worker


@router.post("/workers/{worker_id}/heartbeat", response_model=WorkerResponse)
async def heartbeat(
    worker_id: uuid.UUID,
    body: WorkerHeartbeat,
    db: AsyncSession = Depends(get_db),
):
    worker = await db.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    worker.last_heartbeat = datetime.now(timezone.utc)
    worker.comfyui_running = body.comfyui_running
    if worker.status == "offline":
        worker.status = "online-idle"
    # Don't reset "draining" status — daemon needs to see it
    await db.commit()
    await db.refresh(worker)
    return worker


@router.patch("/workers/{worker_id}/status", response_model=WorkerResponse)
async def update_status(
    worker_id: uuid.UUID,
    body: WorkerStatusUpdate,
    db: AsyncSession = Depends(get_db),
):
    allowed = {"online-idle", "online-busy"}
    if body.status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Status must be one of: {', '.join(sorted(allowed))}",
        )
    worker = await db.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    worker.status = body.status
    await db.commit()
    await db.refresh(worker)
    return worker


@router.get("/workers", response_model=list[WorkerResponse])
async def list_workers(
    status: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Worker)
    if status:
        stmt = stmt.where(Worker.status == status)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/workers/{worker_id}", response_model=WorkerResponse)
async def get_worker(
    worker_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    worker = await db.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker
