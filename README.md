# wanly-gpu-registry

Worker registration and health tracking service for the Wanly platform. Tracks GPU worker status via heartbeats and exposes a REST API.

## API

Swagger UI available at `/docs` when running.

### Endpoints

- `POST /workers` — Register a worker
- `DELETE /workers/{worker_id}` — Deregister a worker
- `POST /workers/{worker_id}/heartbeat` — Send heartbeat
- `PATCH /workers/{worker_id}/status` — Update worker status
- `GET /workers` — List workers (optional `?status=` filter)
- `GET /workers/{worker_id}` — Get a worker

## Setup

### Prerequisites

- Python 3.12+
- PostgreSQL (via asyncpg)

### Environment

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string (asyncpg) | *required* |
| `HEARTBEAT_OFFLINE_SECONDS` | Seconds before a worker is marked offline | `120` |

### Install and run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Deployment

Deployed via GitHub Actions CI/CD. On push to `main`:

1. Docker image built and pushed to ECR
2. Alembic migrations run on the target EC2 instance
3. Container restarted via AWS SSM

The EC2 instance reads environment variables from `/opt/wanly-gpu-registry/.env`.
