import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api import *

try:
    import uvicorn
except Exception:  # pragma: no cover - fallback if uvicorn missing at import time
    uvicorn = None

app = FastAPI()
app.include_router(qq_email)
app.include_router(liepin)
app.include_router(zhilian_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def _run() -> None:
    if uvicorn is None:
        raise RuntimeError("uvicorn is required to run the API server")

    # 检查是否启用重载模式
    debug_mode = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

    if debug_mode:
        print("🚀 启动开发模式（带自动重载）...")
        # 使用导入字符串方式启动，支持重载
        uvicorn.run(
            "main:app",  # 注意这里是字符串格式 "模块名:应用名"
            host="127.0.0.1",
            port=8000,
            reload=True,
            reload_dirs=["./api", "./search_manage"],
            reload_excludes=["*.pyc", "__pycache__", ".git"]
        )
    else:
        print("🚀 启动生产模式...")
        # 生产模式下直接运行应用实例
        uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    _run()
