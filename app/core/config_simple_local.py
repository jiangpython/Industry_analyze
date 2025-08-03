import os
from typing import Optional


class LocalSettings:
    """本地存储配置"""
    
    def __init__(self):
        # 数据存储路径
        self.DATA_DIR = os.getenv("DATA_DIR", "./data")
        self.LOG_DIR = os.getenv("LOG_DIR", "./logs")
        
        # 数据文件路径
        self.COMPANIES_FILE = os.path.join(self.DATA_DIR, "companies.json")
        self.FINANCIAL_DATA_FILE = os.path.join(self.DATA_DIR, "financial_data.json")
        self.INDUSTRY_DATA_FILE = os.path.join(self.DATA_DIR, "industry_data.json")
        self.ANALYSIS_RESULTS_FILE = os.path.join(self.DATA_DIR, "analysis_results.json")
        
        # CSV文件路径（可选）
        self.COMPANIES_CSV = os.path.join(self.DATA_DIR, "companies.csv")
        self.FINANCIAL_DATA_CSV = os.path.join(self.DATA_DIR, "financial_data.csv")
        
        # Gemini API配置
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        
        # 日志配置
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.path.join(self.LOG_DIR, "app.log")
        
        # 应用配置
        self.DEBUG = os.getenv("DEBUG", "True").lower() == "true"
        
        # 爬虫配置
        self.CRAWLER_DELAY = int(os.getenv("CRAWLER_DELAY", "1"))
        self.CRAWLER_TIMEOUT = int(os.getenv("CRAWLER_TIMEOUT", "30"))
        self.USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # 数据源配置
        self.EASTMONEY_BASE_URL = os.getenv("EASTMONEY_BASE_URL", "http://f10.eastmoney.com")
        self.THS_BASE_URL = os.getenv("THS_BASE_URL", "http://basic.10jqka.com.cn")
        
        # 行业配置
        self.TARGET_INDUSTRIES = ["医药", "新能源", "半导体", "芯片"]
        
        # 确保目录存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.LOG_DIR, exist_ok=True)


# 创建全局配置实例
local_settings = LocalSettings() 