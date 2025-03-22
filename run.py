#!/usr/bin/env python3
import os
import uvicorn
from app.core.config import APP_HOST, APP_PORT

if __name__ == "__main__":
    os.system("clear" if os.name == "posix" else "cls")
    print("="*50)
    print("启动 LLM RAG 演示应用")
    print("="*50)
    print(f"应用将在 http://{APP_HOST}:{APP_PORT} 上运行")
    print("API文档访问地址: http://127.0.0.1:8000/docs")
    print("="*50)
    print("按 Ctrl+C 停止服务")
    print("="*50)
    
    uvicorn.run("app.main:app", host=APP_HOST, port=APP_PORT, reload=True) 