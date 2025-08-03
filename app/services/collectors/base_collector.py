import requests
import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class BaseCollector(ABC):
    """基础数据采集器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': settings.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def get(self, url: str, **kwargs) -> Optional[requests.Response]:
        """发送GET请求"""
        try:
            response = self.session.get(url, timeout=settings.CRAWLER_TIMEOUT, **kwargs)
            response.raise_for_status()
            time.sleep(settings.CRAWLER_DELAY)  # 请求间隔
            return response
        except requests.RequestException as e:
            logger.error(f"请求失败: {url}, 错误: {e}")
            return None
    
    def post(self, url: str, data: Dict[str, Any] = None, **kwargs) -> Optional[requests.Response]:
        """发送POST请求"""
        try:
            response = self.session.post(url, data=data, timeout=settings.CRAWLER_TIMEOUT, **kwargs)
            response.raise_for_status()
            time.sleep(settings.CRAWLER_DELAY)  # 请求间隔
            return response
        except requests.RequestException as e:
            logger.error(f"请求失败: {url}, 错误: {e}")
            return None
    
    @abstractmethod
    def collect(self, **kwargs) -> Dict[str, Any]:
        """数据采集方法，子类必须实现"""
        pass
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """验证数据有效性"""
        if not data:
            return False
        return True
    
    def save_data(self, data: Dict[str, Any]) -> bool:
        """保存数据，子类可以重写"""
        # 默认实现，子类可以重写
        return True 