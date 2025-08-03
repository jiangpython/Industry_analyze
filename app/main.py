from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api.endpoints import companies, industries, tasks
import logging
import os

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)

# 创建日志目录
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)

# 创建FastAPI应用
app = FastAPI(
    title="金融分析系统",
    description="智能金融分析系统，专注于医药、新能源、半导体、芯片等行业的数据采集、处理和分析",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(companies.router, prefix="/api/v1")
app.include_router(industries.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    # 初始化数据库
    init_db()
    logging.info("应用启动完成")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "金融分析系统API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}


@app.get("/api/v1/")
async def api_root():
    """API根路径"""
    return {
        "message": "金融分析系统API v1",
        "endpoints": {
            "companies": "/api/v1/companies",
            "industries": "/api/v1/industries",
            "tasks": "/api/v1/tasks"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 