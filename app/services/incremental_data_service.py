#!/usr/bin/env python3
"""
增量数据服务
智能处理历史数据的增量更新
"""

import akshare as ak
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
from app.utils.data_manager import data_manager

logger = logging.getLogger(__name__)

class IncrementalDataService:
    """增量数据服务"""
    
    def __init__(self):
        self.cache_duration = timedelta(days=1)  # 日线数据缓存1天
        self.minute_cache_duration = timedelta(minutes=5)  # 分钟数据缓存5分钟
    
    def get_stock_historical_data(
        self, 
        symbol: str, 
        start_date: str = None,
        end_date: str = None,
        period: str = "daily",
        force_refresh: bool = False
    ) -> Dict[str, Any]:
        """
        获取股票历史数据（增量更新）
        
        Args:
            symbol: 股票代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            period: 数据周期 (daily, weekly, monthly)
            force_refresh: 是否强制刷新
        """
        try:
            # 1. 确定日期范围
            end_date = end_date or datetime.now().strftime('%Y-%m-%d')
            if start_date:
                # 用户指定了开始日期
                date_range = (start_date, end_date)
            else:
                # 默认获取1年数据
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
                date_range = (start_date, end_date)
            
            # 2. 检查本地缓存
            cached_data = self._get_cached_historical_data(symbol, period)
            
            if not force_refresh and cached_data:
                # 3. 智能增量更新
                updated_data = self._incremental_update(
                    symbol, cached_data, date_range, period
                )
                return updated_data
            else:
                # 4. 全量获取
                logger.info(f"全量获取 {symbol} 历史数据")
                return self._fetch_full_historical_data(symbol, date_range, period)
                
        except Exception as e:
            logger.error(f"获取历史数据失败 {symbol}: {e}")
            return {"error": str(e)}
    
    def _get_cached_historical_data(self, symbol: str, period: str) -> Optional[Dict[str, Any]]:
        """获取缓存的历史数据"""
        try:
            cache_key = f"historical_{symbol}_{period}"
            cached_data = data_manager.get_cache_data(cache_key)
            
            if cached_data and self._is_cache_valid(cache_key):
                return cached_data
            return None
        except Exception as e:
            logger.error(f"获取缓存历史数据失败 {symbol}: {e}")
            return None
    
    def _incremental_update(
        self, 
        symbol: str, 
        cached_data: Dict[str, Any], 
        date_range: Tuple[str, str],
        period: str
    ) -> Dict[str, Any]:
        """
        增量更新历史数据
        
        逻辑：
        1. 分析缓存数据的日期范围
        2. 确定需要补充的日期范围
        3. 只获取缺失的数据
        4. 合并新旧数据
        """
        try:
            start_date, end_date = date_range
            request_start = datetime.strptime(start_date, '%Y-%m-%d')
            request_end = datetime.strptime(end_date, '%Y-%m-%d')
            
            # 获取缓存数据的日期范围
            cached_dates = set()
            if 'data' in cached_data and cached_data['data']:
                for record in cached_data['data']:
                    if 'date' in record:
                        cached_dates.add(record['date'])
            
            # 确定需要获取的日期范围
            missing_dates = []
            current_date = request_start
            while current_date <= request_end:
                date_str = current_date.strftime('%Y-%m-%d')
                if date_str not in cached_dates:
                    missing_dates.append(date_str)
                current_date += timedelta(days=1)
            
            if not missing_dates:
                logger.info(f"{symbol} 缓存数据完整，无需更新")
                return cached_data
            
            # 获取缺失的数据
            logger.info(f"{symbol} 需要补充 {len(missing_dates)} 天的数据")
            missing_data = self._fetch_missing_data(symbol, missing_dates, period)
            
            if missing_data:
                # 合并数据
                updated_data = self._merge_historical_data(cached_data, missing_data)
                
                # 更新缓存
                cache_key = f"historical_{symbol}_{period}"
                data_manager.save_cache_data(cache_key, updated_data)
                
                return updated_data
            else:
                return cached_data
                
        except Exception as e:
            logger.error(f"增量更新失败 {symbol}: {e}")
            return cached_data
    
    def _fetch_missing_data(
        self, 
        symbol: str, 
        missing_dates: List[str], 
        period: str
    ) -> List[Dict[str, Any]]:
        """获取缺失的数据"""
        try:
            if period == "daily":
                # 获取日线数据
                df = ak.stock_zh_a_hist(symbol=symbol, period="daily", 
                                       start_date=missing_dates[0], 
                                       end_date=missing_dates[-1])
            else:
                # 其他周期的数据获取逻辑
                df = ak.stock_zh_a_hist(symbol=symbol, period=period)
            
            if df.empty:
                return []
            
            # 转换为标准格式
            data = []
            for _, row in df.iterrows():
                record = {
                    "date": row.get('日期', ''),
                    "open": row.get('开盘', 0),
                    "high": row.get('最高', 0),
                    "low": row.get('最低', 0),
                    "close": row.get('收盘', 0),
                    "volume": row.get('成交量', 0),
                    "turnover": row.get('成交额', 0),
                    "amplitude": row.get('振幅', 0),
                    "change_percent": row.get('涨跌幅', 0),
                    "change_amount": row.get('涨跌额', 0),
                    "turnover_rate": row.get('换手率', 0)
                }
                data.append(record)
            
            return data
            
        except Exception as e:
            logger.error(f"获取缺失数据失败 {symbol}: {e}")
            return []
    
    def _merge_historical_data(
        self, 
        cached_data: Dict[str, Any], 
        new_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """合并历史数据"""
        try:
            # 合并数据
            all_data = cached_data.get('data', []) + new_data
            
            # 按日期排序
            all_data.sort(key=lambda x: x.get('date', ''))
            
            # 去重（按日期）
            seen_dates = set()
            unique_data = []
            for record in all_data:
                date = record.get('date', '')
                if date and date not in seen_dates:
                    seen_dates.add(date)
                    unique_data.append(record)
            
            return {
                "symbol": cached_data.get('symbol', ''),
                "period": cached_data.get('period', ''),
                "data": unique_data,
                "total_records": len(unique_data),
                "date_range": {
                    "start": unique_data[0].get('date') if unique_data else '',
                    "end": unique_data[-1].get('date') if unique_data else ''
                },
                "last_updated": datetime.now().isoformat(),
                "source": "增量更新"
            }
            
        except Exception as e:
            logger.error(f"合并历史数据失败: {e}")
            return cached_data
    
    def _fetch_full_historical_data(
        self, 
        symbol: str, 
        date_range: Tuple[str, str], 
        period: str
    ) -> Dict[str, Any]:
        """全量获取历史数据"""
        try:
            start_date, end_date = date_range
            
            # 获取历史数据
            df = ak.stock_zh_a_hist(symbol=symbol, period=period, 
                                   start_date=start_date, end_date=end_date)
            
            if df.empty:
                return {"error": "未获取到数据"}
            
            # 转换为标准格式
            data = []
            for _, row in df.iterrows():
                record = {
                    "date": row.get('日期', ''),
                    "open": row.get('开盘', 0),
                    "high": row.get('最高', 0),
                    "low": row.get('最低', 0),
                    "close": row.get('收盘', 0),
                    "volume": row.get('成交量', 0),
                    "turnover": row.get('成交额', 0),
                    "amplitude": row.get('振幅', 0),
                    "change_percent": row.get('涨跌幅', 0),
                    "change_amount": row.get('涨跌额', 0),
                    "turnover_rate": row.get('换手率', 0)
                }
                data.append(record)
            
            result = {
                "symbol": symbol,
                "period": period,
                "data": data,
                "total_records": len(data),
                "date_range": {
                    "start": start_date,
                    "end": end_date
                },
                "last_updated": datetime.now().isoformat(),
                "source": "全量获取"
            }
            
            # 保存到缓存
            cache_key = f"historical_{symbol}_{period}"
            data_manager.save_cache_data(cache_key, result)
            
            return result
            
        except Exception as e:
            logger.error(f"全量获取历史数据失败 {symbol}: {e}")
            return {"error": str(e)}
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """检查缓存是否有效"""
        try:
            cache_data = data_manager.get_cache_data(cache_key)
            if not cache_data:
                return False
            
            last_updated = cache_data.get('last_updated')
            if not last_updated:
                return False
            
            last_update_time = datetime.fromisoformat(last_updated)
            return datetime.now() - last_update_time < self.cache_duration
            
        except Exception as e:
            logger.error(f"检查缓存有效性失败: {e}")
            return False
    
    def get_data_statistics(self, symbol: str) -> Dict[str, Any]:
        """获取数据统计信息"""
        try:
            cached_data = self._get_cached_historical_data(symbol, "daily")
            
            if not cached_data:
                return {"message": "无缓存数据"}
            
            data = cached_data.get('data', [])
            
            if not data:
                return {"message": "数据为空"}
            
            # 计算统计信息
            prices = [record.get('close', 0) for record in data if record.get('close')]
            volumes = [record.get('volume', 0) for record in data if record.get('volume')]
            
            return {
                "symbol": symbol,
                "total_records": len(data),
                "date_range": cached_data.get('date_range', {}),
                "price_stats": {
                    "min": min(prices) if prices else 0,
                    "max": max(prices) if prices else 0,
                    "avg": sum(prices) / len(prices) if prices else 0
                },
                "volume_stats": {
                    "total": sum(volumes) if volumes else 0,
                    "avg": sum(volumes) / len(volumes) if volumes else 0
                },
                "last_updated": cached_data.get('last_updated', '')
            }
            
        except Exception as e:
            logger.error(f"获取数据统计失败 {symbol}: {e}")
            return {"error": str(e)}

# 全局实例
incremental_service = IncrementalDataService() 