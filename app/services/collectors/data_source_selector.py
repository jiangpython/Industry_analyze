from typing import Dict, Any, List, Optional
import logging
from app.services.collectors.yahoo_collector import YahooFinanceCollector
from app.services.collectors.akshare_collector import AKShareCollector

logger = logging.getLogger(__name__)

class DataSourceSelector:
    """数据源选择器，用于灵活选择不同的数据源"""
    
    def __init__(self):
        self.yahoo_collector = YahooFinanceCollector()
        self.akshare_collector = AKShareCollector()
    
    def get_stock_data(self, symbol: str, source: str = "auto", **kwargs) -> Dict[str, Any]:
        """
        获取股票数据，可以选择数据源
        
        Args:
            symbol: 股票代码
            source: 数据源，可选值：'yahoo', 'akshare', 'auto'
            **kwargs: 其他参数
        
        Returns:
            股票数据字典
        """
        try:
            # 自动选择数据源
            if source == "auto":
                # 根据股票代码前缀判断市场
                if symbol.startswith(('0', '3', '6')):  # 中国A股
                    source = "akshare"
                elif symbol.endswith(('.HK', '.SS', '.SZ')):  # 港股或A股（雅虎格式）
                    source = "yahoo"
                else:  # 默认使用雅虎
                    source = "yahoo"
            
            # 根据选择的数据源获取数据
            if source == "yahoo":
                return self.yahoo_collector.get_stock_data(symbol, **kwargs)
            elif source == "akshare":
                return self.akshare_collector.get_stock_data(symbol, **kwargs)
            else:
                logger.error(f"不支持的数据源: {source}")
                return {"error": f"不支持的数据源: {source}"}
        
        except Exception as e:
            logger.error(f"获取股票数据失败: {e}")
            return {"error": f"获取数据失败: {str(e)}"}
    
    def get_market_data(self, market: str, source: str = "auto") -> Dict[str, Any]:
        """
        获取市场数据，可以选择数据源
        
        Args:
            market: 市场代码
            source: 数据源，可选值：'yahoo', 'akshare', 'auto'
        
        Returns:
            市场数据字典
        """
        try:
            # 自动选择数据源
            if source == "auto":
                if market.lower() in ['china', 'cn', 'a股', '沪深', '沪深300']:
                    source = "akshare"
                else:
                    source = "yahoo"
            
            # 根据选择的数据源获取数据
            if source == "yahoo":
                return self.yahoo_collector.get_market_data(market)
            elif source == "akshare":
                return self.akshare_collector.get_market_overview()
            else:
                logger.error(f"不支持的数据源: {source}")
                return {"error": f"不支持的数据源: {source}"}
        
        except Exception as e:
            logger.error(f"获取市场数据失败: {e}")
            return {"error": f"获取数据失败: {str(e)}"}
    
    def get_industry_data(self, industry: str, source: str = "akshare") -> Dict[str, Any]:
        """
        获取行业数据，目前主要支持AKShare
        
        Args:
            industry: 行业名称
            source: 数据源，目前主要支持'akshare'
        
        Returns:
            行业数据字典
        """
        try:
            if source == "akshare":
                stocks = self.akshare_collector.get_industry_stocks(industry)
                return {"industry": industry, "stocks": stocks}
            else:
                logger.error(f"不支持的数据源: {source}")
                return {"error": f"不支持的数据源: {source}"}
        
        except Exception as e:
            logger.error(f"获取行业数据失败: {e}")
            return {"error": f"获取数据失败: {str(e)}"}
    
    def search_stocks(self, query: str, source: str = "auto") -> List[Dict[str, Any]]:
        """
        搜索股票，可以选择数据源
        
        Args:
            query: 搜索关键词
            source: 数据源，可选值：'yahoo', 'akshare', 'auto'
        
        Returns:
            股票列表
        """
        try:
            # 自动选择数据源或使用两个源并合并结果
            if source == "auto":
                # 尝试从两个源获取数据
                yahoo_results = self.yahoo_collector.search_stocks(query)
                
                # 对于中文查询，优先使用AKShare
                if any('\u4e00' <= char <= '\u9fff' for char in query):
                    # 这里需要实现AKShare的搜索功能
                    # 目前AKShare没有直接的股票搜索API，可以考虑从行业成分股中筛选
                    akshare_results = []
                    return akshare_results if akshare_results else yahoo_results
                else:
                    return yahoo_results
            
            elif source == "yahoo":
                return self.yahoo_collector.search_stocks(query)
            
            elif source == "akshare":
                # 这里需要实现AKShare的搜索功能
                # 目前暂无直接实现
                return []
            
            else:
                logger.error(f"不支持的数据源: {source}")
                return []
        
        except Exception as e:
            logger.error(f"搜索股票失败: {e}")
            return []