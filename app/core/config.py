import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./data/financial.db"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379"
    
    # Gemini API配置
    GEMINI_API_KEY: Optional[str] = None
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # 应用配置
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # 爬虫配置
    CRAWLER_DELAY: int = 1
    CRAWLER_TIMEOUT: int = 30
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # 任务配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # 数据源配置
    EASTMONEY_BASE_URL: str = "http://f10.eastmoney.com"
    THS_BASE_URL: str = "http://basic.10jqka.com.cn"
    STATS_BASE_URL: str = "http://www.stats.gov.cn"
    
    # 行业配置
    TARGET_INDUSTRIES = [
        "医药", "新能源", "半导体", "芯片"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings() 