from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from backend.routers_posts import router as posts_router

load_dotenv()
origins = [o.strip() for o in os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:5173").split(",")]

app = FastAPI(title="Company API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_methods=["*"], allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

app.include_router(posts_router)
