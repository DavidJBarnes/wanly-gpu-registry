import uuid
from datetime import datetime

from pydantic import BaseModel


class WorkerRegister(BaseModel):
    friendly_name: str
    hostname: str
    ip_address: str
    comfyui_running: bool = False


class WorkerHeartbeat(BaseModel):
    comfyui_running: bool


class WorkerRename(BaseModel):
    friendly_name: str


class WorkerStatusUpdate(BaseModel):
    status: str


class WorkerResponse(BaseModel):
    id: uuid.UUID
    friendly_name: str
    hostname: str
    ip_address: str
    status: str
    comfyui_running: bool
    last_heartbeat: datetime
    registered_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
