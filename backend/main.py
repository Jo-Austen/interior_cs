from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from backend.api.router import api_router


load_dotenv()
# ✅ 1) 覆盖默认值：把 5173 改成 Nuxt 的 3000，并顺带加上 127.0.0.1 变体
_default_origins = "http://localhost:3000,http://127.0.0.1:3000"
origins = [
    o.strip() for o in os.getenv("CORS_ALLOW_ORIGINS", _default_origins).split(",") if o.strip()
]

app = FastAPI(title="Company API", version="1.0")

# ✅ 2) CORS 放在 include_router 之前
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,          # 若前端将来需要带 cookie，这行要开；不需要可设 False
    allow_methods=["*"],             # 含 OPTIONS
    allow_headers=["*"],             # 含 Content-Type 等
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# 统一挂载
app.include_router(api_router)
