from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db.deps import get_db

from api.routes.jobs import router as jobs_router
from api.routes.workers import (
    router as workers_router,
)
from api.routes.metrics import (
    router as metrics_router,
)

app = FastAPI(
    title= "FlowForge",
    version= "0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs_router)

app.include_router(workers_router)

app.include_router(metrics_router)

@app.get("/")
async def root():
    return {
        "message" : "FlowForge API is running"
    }
    
@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }
    
@app.get("/health/db")
async def db_health_check(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        text("SELECT 1")
    )

    return {
        "database": "connected",
        "result": result.scalar(),
    }