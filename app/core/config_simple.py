import os
from typing import Optional


class SimpleSettings:
    """简化的应用配置类"""
    
    def __init__(self):
        # 数据库配置
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/financial.db")
        
        # Redis配置
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Gemini API配置
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        
        # 日志配置
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.getenv("LOG_FILE", "./logs/app.log")
        
        # 应用配置
        self.DEBUG = os.getenv("DEBUG", "True").lower() == "true"
        self.SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        
        # 爬虫配置
        self.CRAWLER_DELAY = int(os.getenv("CRAWLER_DELAY", "1"))
        self.CRAWLER_TIMEOUT = int(os.getenv("CRAWLER_TIMEOUT", "30"))
        self.USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # 任务配置
        self.CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
        self.CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
        
        # 数据源配置
        self.EASTMONEY_BASE_URL = os.getenv("EASTMONEY_BASE_URL", "http://f10.eastmoney.com")
        self.THS_BASE_URL = os.getenv("THS_BASE_URL", "http://basic.10jqka.com.cn")
        self.STATS_BASE_URL = os.getenv("STATS_BASE_URL", "http://www.stats.gov.cn")
        
        # 行业配置
        self.TARGET_INDUSTRIES = ["医药", "新能源", "半导体", "芯片"]


# 创建全局配置实例
simple_settings = SimpleSettings() 