from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.routes import auth, transactions, summary, health, goals

app = FastAPI(
    title="FinFresh API",
    description="Personal Finance Management API",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(summary.router)
app.include_router(health.router)
app.include_router(goals.router)

@app.get("/")
async def root():
    return {
        "message": "FinFresh API is running",
        "status": "success",
        "version": "2.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }