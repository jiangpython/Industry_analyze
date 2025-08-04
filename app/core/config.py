import os
from typing import Optional, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""
    
    # 数据存储路径
    DATA_DIR: str = "./data"
    LOG_DIR: str = "./logs"
    
    # 数据文件路径
    COMPANIES_FILE: str = "./data/companies.json"
    FINANCIAL_DATA_FILE: str = "./data/financial_data.json"
    INDUSTRY_DATA_FILE: str = "./data/industry_data.json"
    ANALYSIS_RESULTS_FILE: str = "./data/analysis_results.json"
    
    # CSV文件路径（可选）
    COMPANIES_CSV: str = "./data/companies.csv"
    FINANCIAL_DATA_CSV: str = "./data/financial_data.csv"
    
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
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./data/financial.db"
    
    # 数据源配置
    EASTMONEY_BASE_URL: str = "http://f10.eastmoney.com"
    THS_BASE_URL: str = "http://basic.10jqka.com.cn"
    STATS_BASE_URL: str = "http://www.stats.gov.cn"
    
    # 行业配置
    TARGET_INDUSTRIES: str = "医药,新能源,半导体,芯片"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 确保目录存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.LOG_DIR, exist_ok=True)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings() 