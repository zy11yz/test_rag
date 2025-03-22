import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 基本路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# API配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY 环境变量未设置")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
if not OPENAI_API_BASE:
    raise ValueError("OPENAI_API_BASE 环境变量未设置")

# 应用设置
APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

# 向量数据库设置
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", os.path.join(BASE_DIR, "chroma_db"))

# LLM设置
DEFAULT_MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-ada-002"

# 文档处理设置
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200 