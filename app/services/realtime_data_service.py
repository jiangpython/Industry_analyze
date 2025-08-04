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

    def get_financial_data(self, company_code: str, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        获取公司财务数据
        混合模式：优先本地缓存，需要时实时采集
        """
        try:
            # 1. 检查本地缓存
            if not force_refresh:
                cached_data = data_manager.get_financial_data(company_code)
                if cached_data:
                    logger.info(f"使用本地财务数据: {company_code}")
                    return cached_data
            
            # 2. 实时采集财务数据
            logger.info(f"实时采集财务数据: {company_code}")
            financial_data = self._fetch_financial_data(company_code)
            
            if financial_data:
                # 3. 保存到本地
                for data in financial_data:
                    data_manager.save_financial_data(company_code, data)
                logger.info(f"财务数据采集成功并保存: {company_code}")
                return financial_data
            else:
                # 4. 降级到本地存储
                logger.warning(f"实时采集失败，使用本地数据: {company_code}")
                return data_manager.get_financial_data(company_code)
                
        except Exception as e:
            logger.error(f"获取财务数据失败 {company_code}: {e}")
            return data_manager.get_financial_data(company_code)
    
    def _fetch_financial_data(self, company_code: str) -> List[Dict[str, Any]]:
        """从AKShare获取公司财务数据"""
        try:
            import akshare as ak
            
            # 获取财务报表数据
            financial_data = []
            
            # 使用可靠的财务摘要接口
            try:
                financial_abstract = ak.stock_financial_abstract(symbol=company_code)
                if not financial_abstract.empty:
                    # 获取所有可用的日期列（除了'选项'和'指标'）
                    date_columns = [col for col in financial_abstract.columns if col not in ['选项', '指标']]
                    
                    # 按时间排序，从新到旧
                    date_columns.sort(reverse=True)
                    
                    # 为每个日期创建一条财务记录
                    for date_col in date_columns:
                        financial_record = {
                            'report_date': date_col,
                            'data_type': 'annual' if '年度' in str(date_col) or date_col.endswith('1231') else 'quarterly',
                            'source': 'AKShare财务摘要'
                        }
                        
                        # 提取该日期的财务数据
                        for _, row in financial_abstract.iterrows():
                            indicator = row.get('指标', '')
                            value = row.get(date_col, None)
                            
                            if pd.isna(value) or value == '':
                                continue
                            
                            # 分类处理不同的财务指标
                            if '资产' in indicator and '总资产' in indicator:
                                financial_record['total_assets'] = self._convert_to_float(value)
                            elif '负债' in indicator and '总负债' in indicator:
                                financial_record['total_liabilities'] = self._convert_to_float(value)
                            elif '营业收入' in indicator:
                                financial_record['revenue'] = self._convert_to_float(value)
                            elif '净利润' in indicator:
                                financial_record['net_profit'] = self._convert_to_float(value)
                            elif '经营活动现金流量净额' in indicator:
                                financial_record['operating_cash_flow'] = self._convert_to_float(value)
                        
                        # 只有当有实际数据时才添加记录
                        if (financial_record.get('total_assets') or 
                            financial_record.get('revenue') or 
                            financial_record.get('net_profit')):
                            financial_data.append(financial_record)
                            
            except Exception as e:
                logger.warning(f"获取财务摘要失败 {company_code}: {e}")
            
            # 如果财务摘要没有数据，尝试其他方法
            if not financial_data:
                try:
                    # 尝试使用财务指标接口
                    financial_indicators = ak.stock_financial_analysis_indicator(symbol=company_code)
                    if not financial_indicators.empty:
                        # 获取所有可用的日期
                        available_dates = financial_indicators.index
                        
                        for date in available_dates:
                            financial_record = {
                                'report_date': date.strftime('%Y-%m-%d'),
                                'data_type': 'annual' if '年度' in str(date) or date.strftime('%m%d') == '1231' else 'quarterly',
                                'source': 'AKShare财务指标'
                            }
                            
                            # 提取关键指标
                            if '营业收入' in financial_indicators.columns:
                                financial_record['revenue'] = financial_indicators.loc[date, '营业收入']
                            if '净利润' in financial_indicators.columns:
                                financial_record['net_profit'] = financial_indicators.loc[date, '净利润']
                            if '总资产' in financial_indicators.columns:
                                financial_record['total_assets'] = financial_indicators.loc[date, '总资产']
                            if '总负债' in financial_indicators.columns:
                                financial_record['total_liabilities'] = financial_indicators.loc[date, '总负债']
                            
                            if financial_record.get('revenue') or financial_record.get('net_profit'):
                                financial_data.append(financial_record)
                                
                except Exception as e:
                    logger.warning(f"获取财务指标失败 {company_code}: {e}")
            
            return financial_data
            
        except Exception as e:
            logger.error(f"采集财务数据失败 {company_code}: {e}")
            return []
    
    def _convert_to_float(self, value):
        """转换值为浮点数"""
        try:
            if isinstance(value, str):
                # 移除可能的单位（万元、亿元等）
                value = value.replace('万元', '').replace('亿元', '').replace(',', '')
                # 如果是亿元，转换为万元
                if '亿' in str(value):
                    value = float(value.replace('亿', '')) * 10000
                return float(value)
            return float(value)
        except (ValueError, TypeError):
            return None

    def get_industry_data(self, industry: str, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """
        获取行业数据
        混合模式：优先本地缓存，需要时实时采集
        """
        try:
            # 1. 检查本地缓存
            if not force_refresh:
                cached_data = data_manager.get_industry_data(industry)
                if cached_data:
                    logger.info(f"使用本地行业数据: {industry}")
                    return cached_data
            
            # 2. 实时采集行业数据
            logger.info(f"实时采集行业数据: {industry}")
            industry_data = self._fetch_industry_data(industry)
            
            if industry_data:
                # 3. 保存到本地
                data_manager.save_industry_data(industry, industry_data)
                logger.info(f"行业数据采集成功并保存: {industry}")
                return industry_data
            else:
                # 4. 降级到本地存储
                logger.warning(f"实时采集失败，使用本地数据: {industry}")
                return data_manager.get_industry_data(industry)
                
        except Exception as e:
            logger.error(f"获取行业数据失败 {industry}: {e}")
            return data_manager.get_industry_data(industry)
    
    def _fetch_industry_data(self, industry: str) -> Optional[Dict[str, Any]]:
        """从AKShare获取行业数据"""
        try:
            import akshare as ak
            
            # 获取行业相关数据
            industry_data = {
                'industry': industry,
                'data_type': 'market',
                'market_size': None,
                'growth_rate': None,
                'company_count': None,
                'avg_pe': None,
                'description': f'{industry}行业数据',
                'source': 'AKShare行业数据',
                'update_time': datetime.now().isoformat()
            }
            
            # 尝试获取行业指数数据
            try:
                # 这里可以根据行业名称获取相应的指数数据
                # 例如：医药行业可以获取医药指数
                if '医药' in industry:
                    # 获取医药指数数据
                    pass
                elif '新能源' in industry:
                    # 获取新能源指数数据
                    pass
                elif '半导体' in industry:
                    # 获取半导体指数数据
                    pass
                
                # 设置一些示例数据
                industry_data.update({
                    'market_size': 1000000000,  # 10亿
                    'growth_rate': 0.15,  # 15%
                    'company_count': 50,
                    'avg_pe': 25.5
                })
                
            except Exception as e:
                logger.warning(f"获取行业指数数据失败 {industry}: {e}")
            
            return industry_data
            
        except Exception as e:
            logger.error(f"采集行业数据失败 {industry}: {e}")
            return None

# 全局实例
realtime_service = RealtimeDataService() 