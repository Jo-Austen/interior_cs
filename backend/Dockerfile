FROM python:3.11-slim

# Python 运行时优化
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 工作目录设为“项目根”
WORKDIR /app

# 系统依赖（cffi / cryptography 等需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
  && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件（利用 Docker cache）
COPY backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 再复制代码（包括 backend 包）
COPY backend /app/backend

# 容器内部统一端口
EXPOSE 8000

# 健康检查（⚠️ 使用你真实存在的 /healthz）
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
  CMD curl -fsS http://localhost:8000/healthz || exit 1

# 启动 FastAPI（⚠️ 真实入口）
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
