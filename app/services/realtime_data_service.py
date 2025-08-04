#!/usr/bin/env python3
"""
实时数据服务
支持混合模式：本地缓存 + 实时获取
"""

import akshare as ak
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from app.utils.data_manager import data_manager

logger = logging.getLogger(__name__)

class RealtimeDataService:
    """实时数据服务"""
    
    def __init__(self):
        self.cache_duration = timedelta(minutes=5)  # 缓存5分钟
        self.last_update = {}
        self._all_stocks_cache = None  # 全局A股数据缓存
        self._all_stocks_cache_time = None  # 缓存时间
    
    def get_stock_realtime_data(self, symbol: str, force_refresh: bool = False) -> Dict[str, Any]:
        """
        获取个股实时数据
        混合模式：优先本地缓存，需要时实时获取
        """
        try:
            # 1. 检查本地缓存
            if not force_refresh:
                cached_data = self._get_cached_stock_data(symbol)
                if cached_data and self._is_cache_valid(symbol):
                    logger.info(f"使用缓存数据: {symbol}")
                    return cached_data
            
            # 2. 实时获取数据
            logger.info(f"实时获取数据: {symbol}")
            realtime_data = self._fetch_stock_realtime(symbol)
            
            if realtime_data and "error" not in realtime_data:
                # 3. 更新缓存
                self._update_stock_cache(symbol, realtime_data)
                return realtime_data
            else:
                # 4. 降级到本地存储
                logger.warning(f"实时获取失败，使用本地数据: {symbol}")
                return self._get_local_stock_data(symbol)
                
        except Exception as e:
            logger.error(f"获取股票数据失败 {symbol}: {e}")
            return self._get_local_stock_data(symbol)
    
    def get_companies_by_industry_realtime(self, industry: str, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        获取指定行业的公司列表（实时）
        """
        try:
            # 1. 检查本地缓存
            if not force_refresh:
                cached_companies = self._get_cached_industry_companies(industry)
                if cached_companies and self._is_cache_valid(industry):
                    logger.info(f"使用缓存数据: {industry} 行业")
                    return cached_companies
            
            # 2. 实时获取数据
            logger.info(f"实时获取行业数据: {industry}")
            realtime_companies = self._fetch_industry_companies(industry)
            
            if realtime_companies:
                # 3. 更新缓存
                self._update_industry_cache(industry, realtime_companies)
                return realtime_companies
            else:
                # 4. 降级到本地存储
                logger.warning(f"实时获取失败，使用本地数据: {industry}")
                return self._get_local_industry_companies(industry)
                
        except Exception as e:
            logger.error(f"获取行业数据失败 {industry}: {e}")
            return self._get_local_industry_companies(industry)
    
    def _fetch_stock_realtime(self, symbol: str) -> Optional[Dict[str, Any]]:
        """从AKShare获取个股实时数据"""
        try:
            # 首先尝试从缓存获取A股数据
            stock_quote = self._get_all_stocks_cache()
            
            # 如果缓存不存在或已过期，重新获取
            if stock_quote is None:
                logger.info("获取所有A股实时数据（将缓存5分钟）")
                stock_quote = ak.stock_zh_a_spot_em()
                self._update_all_stocks_cache(stock_quote)
            else:
                logger.info("使用缓存的A股数据")
            
            # 从数据中筛选目标股票
            stock_data = stock_quote[stock_quote['代码'] == symbol]
            
            if not stock_data.empty:
                row = stock_data.iloc[0]
                return {
                    "code": symbol,
                    "name": row.get('名称', ''),
                    "current_price": row.get('最新价', 0),
                    "change_percent": row.get('涨跌幅', 0),
                    "volume": row.get('成交量', 0),
                    "turnover": row.get('成交额', 0),
                    "market_cap": row.get('总市值', 0),
                    "pe_ratio": row.get('市盈率', 0),
                    "pb_ratio": row.get('市净率', 0),
                    "source": "AKShare实时获取",
                    "update_time": datetime.now().isoformat()
                }
            else:
                logger.warning(f"未找到股票 {symbol} 的实时数据")
                return None
                
        except Exception as e:
            logger.error(f"AKShare获取失败 {symbol}: {e}")
            return None
    
    def _fetch_industry_companies(self, industry: str) -> List[Dict[str, Any]]:
        """从AKShare获取行业公司列表"""
        try:
            # 首先尝试从缓存获取A股数据
            stocks_df = self._get_all_stocks_cache()
            
            # 如果缓存不存在或已过期，重新获取
            if stocks_df is None:
                logger.info("获取所有A股实时数据（将缓存5分钟）")
                stocks_df = ak.stock_zh_a_spot_em()
                self._update_all_stocks_cache(stocks_df)
            else:
                logger.info("使用缓存的A股数据")
            
            # 获取行业信息（简化版本，实际可能需要更复杂的行业映射）
            # 这里使用关键词匹配
            industry_keywords = {
                "医药": ["医药", "生物", "制药", "医疗"],
                "新能源": ["新能源", "光伏", "风电", "储能"],
                "半导体": ["半导体", "芯片", "集成电路", "电子"]
            }
            
            keywords = industry_keywords.get(industry, [industry])
            
            # 筛选包含关键词的公司
            companies = []
            for _, row in stocks_df.iterrows():
                name = row.get('名称', '')
                if any(keyword in name for keyword in keywords):
                    company = {
                        "code": row.get('代码', ''),
                        "name": name,
                        "industry": industry,
                        "market": "A股",
                        "current_price": row.get('最新价', 0),
                        "change_percent": row.get('涨跌幅', 0),
                        "volume": row.get('成交量', 0),
                        "turnover": row.get('成交额', 0),
                        "market_cap": row.get('总市值', 0),
                        "source": "AKShare实时获取",
                        "update_time": datetime.now().isoformat()
                    }
                    companies.append(company)
            
            return companies
            
        except Exception as e:
            logger.error(f"AKShare获取行业数据失败 {industry}: {e}")
            return []
    
    def _get_cached_stock_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取缓存的股票数据"""
        try:
            # 从data_manager获取缓存数据
            cache_key = f"stock_cache_{symbol}"
            return data_manager.get_cache_data(cache_key)
        except Exception as e:
            logger.error(f"获取缓存数据失败 {symbol}: {e}")
            return None
    
    def _get_cached_industry_companies(self, industry: str) -> List[Dict[str, Any]]:
        """获取缓存的行业公司数据"""
        try:
            cache_key = f"industry_cache_{industry}"
            return data_manager.get_cache_data(cache_key) or []
        except Exception as e:
            logger.error(f"获取行业缓存数据失败 {industry}: {e}")
            return []
    
    def _update_stock_cache(self, symbol: str, data: Dict[str, Any]):
        """更新股票缓存"""
        try:
            cache_key = f"stock_cache_{symbol}"
            data_manager.save_cache_data(cache_key, data)
            self.last_update[symbol] = datetime.now()
        except Exception as e:
            logger.error(f"更新股票缓存失败 {symbol}: {e}")
    
    def _update_industry_cache(self, industry: str, companies: List[Dict[str, Any]]):
        """更新行业缓存"""
        try:
            cache_key = f"industry_cache_{industry}"
            data_manager.save_cache_data(cache_key, companies)
            self.last_update[industry] = datetime.now()
        except Exception as e:
            logger.error(f"更新行业缓存失败 {industry}: {e}")
    
    def _is_cache_valid(self, key: str) -> bool:
        """检查缓存是否有效"""
        if key not in self.last_update:
            return False
        return datetime.now() - self.last_update[key] < self.cache_duration
    
    def _get_local_stock_data(self, symbol: str) -> Dict[str, Any]:
        """获取本地存储的股票数据"""
        try:
            company_data = data_manager.get_company(symbol)
            if company_data:
                return {
                    "code": symbol,
                    "name": company_data.get('name', ''),
                    "industry": company_data.get('industry', ''),
                    "market": company_data.get('market', ''),
                    "source": "本地存储",
                    "update_time": datetime.now().isoformat()
                }
            else:
                return {"code": symbol, "error": "未找到本地数据"}
        except Exception as e:
            logger.error(f"获取本地数据失败 {symbol}: {e}")
            return {"code": symbol, "error": str(e)}
    
    def _get_local_industry_companies(self, industry: str) -> List[Dict[str, Any]]:
        """获取本地存储的行业公司数据"""
        try:
            companies = data_manager.get_all_companies()
            industry_companies = []
            
            for company_id, company_data in companies.items():
                if company_data.get('industry') == industry:
                    industry_companies.append({
                        "code": company_id,
                        "name": company_data.get('name', ''),
                        "industry": company_data.get('industry', ''),
                        "market": company_data.get('market', 'A股'),
                        "source": "本地存储",
                        "update_time": datetime.now().isoformat()
                    })
            
            return industry_companies
        except Exception as e:
            logger.error(f"获取本地行业数据失败 {industry}: {e}")
            return []

    def _get_all_stocks_cache(self) -> Optional[pd.DataFrame]:
        """获取缓存的A股数据"""
        if (self._all_stocks_cache is not None and 
            self._all_stocks_cache_time is not None and
            datetime.now() - self._all_stocks_cache_time < self.cache_duration):
            return self._all_stocks_cache
        return None
    
    def _update_all_stocks_cache(self, data: pd.DataFrame):
        """更新A股数据缓存"""
        self._all_stocks_cache = data
        self._all_stocks_cache_time = datetime.now()

# 全局实例
realtime_service = RealtimeDataService() 