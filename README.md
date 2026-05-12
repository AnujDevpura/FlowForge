# FlowForge

FlowForge is a distributed DAG-based workflow orchestration platform inspired by systems like Apache Airflow, Temporal, Prefect, and Dagster.

It schedules dependency-aware tasks, executes them through distributed workers, and exposes runtime state in a web dashboard.

## What It Demonstrates

- Distributed systems coordination
- Async execution pipelines
- Queue-based architecture
- DAG orchestration semantics
- Worker heartbeat and lease recovery
- Retry/backoff lifecycle management
- Execution observability and history

## Core Architecture

```text
PostgreSQL (durable state)
    -> Scheduler
    -> Redis Queue
    -> Workers
    -> Executors
    -> PostgreSQL (status, logs, history, metrics)
```

## Why PostgreSQL + Redis

### PostgreSQL

Used as the durable source of truth for:

- Jobs
- Tasks
- Task dependencies
- Retry counters
- Execution history
- Worker state
- Logs and errors
- Aggregated metrics inputs

### Redis

Used as the execution queue for:

- Fast enqueue/dequeue
- Task dispatch to workers
- Scheduler/worker decoupling
- Queue semantics for distributed execution

## Implemented Features

### DAG Workflow Orchestration

- Arbitrary DAG support
- Dependency-aware task scheduling
- Parallel execution where dependencies allow
- Fan-out/fan-in workflow support
- Recursive blocked-state propagation

### Distributed Worker Architecture

- Multi-worker execution model
- Redis-backed task consumption
- Heartbeat monitoring
- Lease-based task ownership
- Worker recovery path
- Concurrent async execution

### Retry and Failure Handling

- Retry support with backoff
- Failure isolation per task attempt
- Dead worker detection and recovery
- Lease-expiry based task recovery
- Immutable execution attempt records

### Observability

- Jobs list and status visibility
- DAG visualization for each job
- Per-attempt execution logs
- Retry attempt history
- Worker health view
- Status propagation visibility

## System Design Workflow

### End-to-End Lifecycle

```text
Submit DAG
    -> Validate DAG
    -> Persist job/tasks/dependencies in PostgreSQL
    -> Scheduler scans runnable tasks
    -> Runnable tasks pushed to Redis queue
    -> Workers consume and execute tasks
    -> Executor outputs persisted
    -> Downstream tasks become runnable
    -> Job converges to SUCCESS/FAILED
```

### Scheduler Workflow

The scheduler loop continuously:

1. Scans for runnable tasks.
2. Validates dependency completion.
3. Atomically claims tasks for queueing.
4. Pushes claimed tasks to Redis.

Runnable logic (conceptual):

```python
if all_dependencies_successful:
    enqueue_task()
```

### Worker Workflow

Workers:

- Consume tasks from Redis
- Execute tasks concurrently
- Maintain periodic heartbeats
- Renew in-flight task leases
- Persist execution results/logs/errors
- Handle retries and failure transitions
- Participate in recovery semantics

### Concurrency Model

FlowForge uses bounded asyncio concurrency:

```text
Total concurrency = number of workers * max concurrent tasks per worker
```

Example:

```text
4 workers * 3 tasks each = 12 concurrent task executions
```

### Lease and Heartbeat Recovery

Workers periodically update `last_heartbeat_at`.

This supports worker status transitions (for example ACTIVE vs DEAD) and enables recovery of leased RUNNING tasks when a worker disappears.

If a worker dies:

1. Lease expires.
2. Recovery logic marks task re-runnable (or failed by policy).
3. Scheduler can safely re-dispatch.

### Retry Backoff

Conceptual retry schedule:

```text
attempt 1 -> 2s
attempt 2 -> 4s
attempt 3 -> 8s
```

Each retry creates a new immutable execution record.

### Execution History Model

Every task attempt is stored independently with:

- Attempt number
- Worker ID
- Status
- Logs
- Error message
- Start/completion timestamps

This gives auditability and easier production debugging.

### Task Context Propagation

Downstream tasks can consume upstream outputs via task execution context.

Example:

```text
fetch_data
    -> process_data
```

## Frontend Architecture

### Jobs Page

- Workflow list
- Status/search filtering
- Summary metrics cards
- Live-ish refresh behavior

### Job Details Page

- DAG graph visualization
- Task state cards
- Retry and execution history
- Logs/error details
- Dependency and blocked-state visibility

### DAG Visualization

Built with React Flow + Dagre.

Supports:

- Automatic graph layout
- Dependency edges
- Status-driven node styling
- Blocked propagation visibility
- Runtime state rendering

## Current Executors

### HTTP Executor

- Async HTTP requests
- API ingestion workflows
- External integration steps

### Print Executor

- Workflow debugging
- Context propagation testing
- Execution simulation

## Tech Stack

### Backend

- Python 3.11+
- FastAPI
- SQLAlchemy Async ORM
- PostgreSQL
- Redis
- asyncio
- Alembic
- httpx

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- React Flow
- Dagre
- Axios
- Lucide React

### Infrastructure

- Docker
- Docker Compose

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker + Docker Compose
- `uv` (recommended Python package runner)

## Local Setup

1. Clone and enter the repo.
2. Configure `.env`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/flowforge
SYNC_DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/flowforge
REDIS_URL=redis://localhost:6379
```

3. Start infrastructure:

```bash
docker-compose up -d
```

4. Install backend dependencies:

```bash
uv sync
```

5. Apply migrations:

```bash
uv run alembic upgrade head
```

6. Install frontend dependencies:

```bash
cd frontend
npm install
```

## Running the System

Run each service in a separate terminal from repository root.

### API

```bash
uv run uvicorn main:app --reload
```

API URLs:

- `http://localhost:8000/`
- `http://localhost:8000/docs`
- `http://localhost:8000/health`
- `http://localhost:8000/health/db`

### Scheduler

```bash
uv run python -m scripts.run_scheduler
```

### Worker

```bash
uv run python -m scripts.run_worker
```

### Frontend

```bash
cd frontend
npm run dev
```

Frontend URL:

- `http://localhost:5173`

## API Surface (Current)

- `POST /jobs/` create workflow job
- `GET /jobs/` list jobs
- `GET /jobs/{job_id}` get full job graph/state
- `GET /workers/` list workers and heartbeats
- `GET /metrics/` queue and worker metrics

## Repository Structure

```text
FlowForge/
+-- api/           # FastAPI routes
+-- db/            # models, session, DB helpers
+-- executors/     # task executor implementations
+-- frontend/      # React dashboard
+-- queueing/      # Redis queue layer
+-- scheduler/     # runnable scanning and dispatch
+-- schemas/       # request/response models
+-- scripts/       # process entry points
+-- services/      # execution and state services
+-- utils/         # shared logic (for example DAG validation)
+-- worker/        # worker loop and processing
```

## Key Engineering Concepts Implemented

- DAG orchestration with dependency semantics
- Distributed worker coordination
- Queue-based execution dispatch
- Async parallel task execution
- Lease-based recovery for in-flight tasks
- Worker heartbeat based liveness detection
- Retry/backoff control flow
- Immutable execution attempt history
- Task context propagation
- UI-level execution observability

## Troubleshooting

- `DB connection errors`: verify Postgres container and `.env` URLs.
- `Redis errors`: verify Redis container is running on `localhost:6379`.
- `CORS issues`: frontend should run on `http://localhost:5173`.
- `Empty UI state`: confirm API, scheduler, and at least one worker are all running.

## Notes

- `pyproject.toml` currently includes a `flowforge-api` script entry pointing to `scripts.run_api:main`, but `scripts/run_api.py` is not present.
- Running API via `uv run uvicorn main:app --reload` is the current valid path.
