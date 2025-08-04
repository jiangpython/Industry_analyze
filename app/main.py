from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import companies_simple, industries_simple, tasks_simple, yahoo_data, data_source, realtime_data, historical_data, api_overview
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
app.include_router(companies_simple.router, prefix="/api/v1")
app.include_router(industries_simple.router, prefix="/api/v1")
app.include_router(tasks_simple.router, prefix="/api/v1")
app.include_router(yahoo_data.router, prefix="/api/v1")
app.include_router(data_source.router, prefix="/api/v1")
app.include_router(realtime_data.router, prefix="/api/v1")
app.include_router(historical_data.router, prefix="/api/v1")
app.include_router(api_overview.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    # 确保数据目录存在
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    logging.info("应用启动完成")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "金融分析系统API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "storage": "本地文件存储 (JSON/CSV)"
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
        "storage_type": "本地文件存储",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "api_overview": "/api/v1/overview"
        },
        "endpoints": {
            "实时数据": "/api/v1/realtime",
            "历史数据": "/api/v1/historical", 
            "公司管理": "/api/v1/companies",
            "行业管理": "/api/v1/industries",
            "任务管理": "/api/v1/tasks",
            "数据源": "/api/v1/data",
            "API概览": "/api/v1/overview"
        },
        "quick_start": {
            "健康检查": "GET /health",
            "获取实时数据": "GET /api/v1/realtime/stock/000001",
            "获取历史数据": "GET /api/v1/historical/stock/000001",
            "获取行业公司": "GET /api/v1/realtime/companies/医药"
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