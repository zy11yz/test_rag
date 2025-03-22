from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import router as api_router
import os
from pathlib import Path

# 创建应用
app = FastAPI(
    title="LLM RAG 演示应用",
    description="一个基于大语言模型和检索增强生成的简单演示应用",
    version="0.1.0",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api")

# 挂载静态文件
static_dir = Path(__file__).resolve().parent / "static"
if not static_dir.exists():
    static_dir.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

@app.get("/")
async def root():
    return {"message": "欢迎使用LLM RAG演示应用，请访问/docs查看API文档"}

if __name__ == "__main__":
    import uvicorn
    from app.core.config import APP_HOST, APP_PORT
    
    uvicorn.run("app.main:app", host=APP_HOST, port=APP_PORT, reload=True)
