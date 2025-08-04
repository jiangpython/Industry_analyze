import akshare as ak
from typing import Dict, Any, List, Optional
from app.services.collectors.base_collector import BaseCollector
import logging
from datetime import datetime, timedelta
import pandas as pd # Added missing import for pandas

logger = logging.getLogger(__name__)

class AKShareCollector(BaseCollector):
    """AKShare数据采集器，专注于中国市场数据"""
    
    def __init__(self):
        super().__init__()
        
    def collect(self, **kwargs) -> Dict[str, Any]:
        """实现基类的数据采集方法"""
        collection_type = kwargs.get('type', 'stock')
        symbol = kwargs.get('symbol')
        
        if not symbol:
            logger.error("未提供股票代码")
            return {"error": "未提供股票代码"}
        
        try:
            if collection_type == 'stock':
                return self.get_stock_data(symbol, **kwargs)
            elif collection_type == 'fund':
                return self.get_fund_data(symbol, **kwargs)
            elif collection_type == 'index':
                return self.get_index_data(symbol, **kwargs)
            elif collection_type == 'bond':
                return self.get_bond_data(symbol, **kwargs)
            else:
                logger.error(f"不支持的数据类型: {collection_type}")
                return {"error": f"不支持的数据类型: {collection_type}"}
        except Exception as e:
            logger.error(f"获取AKShare数据失败: {e}")
            return {"error": f"获取数据失败: {str(e)}"}
    
    def get_stock_data(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """获取股票数据"""
        try:
            # 处理日期参数
            end_date = kwargs.get('end_date', datetime.now().strftime('%Y%m%d'))
            start_date = kwargs.get('start_date')
            if not start_date:
                # 默认获取一年的数据
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            
            # 获取股票历史数据
            stock_zh_a_hist_df = ak.stock_zh_a_hist(
                symbol=symbol, 
                period="daily", 
                start_date=start_date, 
                end_date=end_date,
                adjust=kwargs.get('adjust', '')
            )
            
            # 获取股票基本信息
            try:
                stock_info_df = ak.stock_individual_info_em(symbol=symbol)
                stock_info = {}
                if not stock_info_df.empty:
                    for _, row in stock_info_df.iterrows():
                        stock_info[row['item']] = row['value']
            except Exception as e:
                logger.warning(f"获取股票信息失败: {e}")
                stock_info = {}
            
            # 获取公司财务数据 - 修复API调用
            try:
                # 使用正确的API调用方式获取财务摘要数据
                financial_abstract_df = ak.stock_financial_abstract(symbol=symbol)
                
                financial_data = {}
                if not financial_abstract_df.empty:
                    # 处理财务摘要数据
                    financial_data = self._process_financial_abstract(financial_abstract_df)
                else:
                    logger.warning(f"股票 {symbol} 无财务摘要数据")
                    
            except Exception as e:
                logger.warning(f"获取财务报表失败: {e}")
                financial_data = {}
            
            # 处理历史数据
            historical_data = []
            if not stock_zh_a_hist_df.empty:
                for _, row in stock_zh_a_hist_df.iterrows():
                    historical_data.append({
                        'date': row.get('日期'),
                        'open': float(row.get('开盘')),
                        'high': float(row.get('最高')),
                        'low': float(row.get('最低')),
                        'close': float(row.get('收盘')),
                        'volume': float(row.get('成交量')),
                        'amount': float(row.get('成交额')) if '成交额' in row else None,
                        'change_pct': float(row.get('涨跌幅')) if '涨跌幅' in row else None,
                        'turnover': float(row.get('换手率')) if '换手率' in row else None
                    })
            
            # 获取行业信息
            try:
                stock_sector = ""
                stock_industry_info_df = ak.stock_sector_detail(sector="申万一级")
                if not stock_industry_info_df.empty:
                    for _, row in stock_industry_info_df.iterrows():
                        # 修复数据类型转换问题
                        stock_code = str(row.get('代码', '')).strip()
                        if stock_code == symbol:
                            stock_sector = row.get('行业', '')
                            break
            except Exception as e:
                logger.warning(f"获取行业信息失败: {e}")
                stock_sector = ""
            
            # 构建结果
            result = {
                'symbol': symbol,
                'company_name': stock_info.get('股票简称', ''),
                'industry': stock_sector,
                'market': '上证' if symbol.startswith('6') else '深证' if symbol.startswith(('0', '3')) else '未知',
                'historical_data': historical_data,
                'financial_data': financial_data,
                'company_info': stock_info
            }
            
            return result
            
        except Exception as e:
            logger.error(f"获取股票数据失败: {e}")
            raise
    
    def _process_financial_abstract(self, df) -> Dict[str, Any]:
        """处理财务摘要数据"""
        try:
            financial_data = {
                'balance_sheet': {},
                'income_statement': {},
                'cash_flow': {},
                'key_indicators': {}
            }
            
            if df.empty:
                return financial_data
            
            # 获取所有可用的日期列（除了'选项'和'指标'）
            date_columns = [col for col in df.columns if col not in ['选项', '指标']]
            if not date_columns:
                return financial_data
            
            # 按时间排序，从新到旧
            date_columns.sort(reverse=True)
            
            # 获取最新的数据（保持向后兼容）
            latest_date = date_columns[0]
            
            # 提取关键财务指标
            for _, row in df.iterrows():
                indicator = row.get('指标', '')
                value = row.get(latest_date, None)
                
                if pd.isna(value) or value == '':
                    continue
                
                # 分类处理不同的财务指标
                if '资产' in indicator and '总资产' in indicator:
                    financial_data['balance_sheet']['total_assets'] = self._convert_to_float(value)
                elif '负债' in indicator and '总负债' in indicator:
                    financial_data['balance_sheet']['total_liabilities'] = self._convert_to_float(value)
                elif '营业收入' in indicator:
                    financial_data['income_statement']['revenue'] = self._convert_to_float(value)
                elif '净利润' in indicator:
                    financial_data['income_statement']['net_profit'] = self._convert_to_float(value)
                elif '经营活动现金流量净额' in indicator:
                    financial_data['cash_flow']['operating_cash_flow'] = self._convert_to_float(value)
                elif '净资产收益率' in indicator:
                    financial_data['key_indicators']['roe'] = self._convert_to_float(value)
                elif '总资产收益率' in indicator:
                    financial_data['key_indicators']['roa'] = self._convert_to_float(value)
                elif '资产负债率' in indicator:
                    financial_data['key_indicators']['debt_ratio'] = self._convert_to_float(value)
            
            # 计算财务比率
            self._calculate_financial_ratios(financial_data)
            
            return financial_data
            
        except Exception as e:
            logger.error(f"处理财务摘要数据失败: {e}")
            return {}
    
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
    
    def _calculate_financial_ratios(self, financial_data):
        """计算财务比率"""
        try:
            # 从资产负债表获取数据
            total_assets = financial_data['balance_sheet'].get('total_assets')
            total_liabilities = financial_data['balance_sheet'].get('total_liabilities')
            
            # 从利润表获取数据
            revenue = financial_data['income_statement'].get('revenue')
            net_profit = financial_data['income_statement'].get('net_profit')
            
            # 从现金流量表获取数据
            operating_cash_flow = financial_data['cash_flow'].get('operating_cash_flow')
            
            # 计算ROE（净资产收益率）
            if net_profit and total_assets and total_liabilities:
                equity = total_assets - total_liabilities
                if equity > 0:
                    financial_data['key_indicators']['roe_calculated'] = (net_profit / equity) * 100
            
            # 计算ROA（总资产收益率）
            if net_profit and total_assets:
                financial_data['key_indicators']['roa_calculated'] = (net_profit / total_assets) * 100
            
            # 计算资产负债率
            if total_liabilities and total_assets:
                financial_data['key_indicators']['debt_ratio_calculated'] = (total_liabilities / total_assets) * 100
            
            # 计算流动比率（简化计算）
            if total_assets and total_liabilities:
                current_assets = total_assets * 0.6  # 假设60%为流动资产
                current_liabilities = total_liabilities * 0.8  # 假设80%为流动负债
                if current_liabilities > 0:
                    financial_data['key_indicators']['current_ratio'] = current_assets / current_liabilities
                    
        except Exception as e:
            logger.error(f"计算财务比率失败: {e}")
    
    def get_fund_data(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """获取基金数据"""
        try:
            # 处理日期参数
            end_date = kwargs.get('end_date', datetime.now().strftime('%Y%m%d'))
            start_date = kwargs.get('start_date')
            if not start_date:
                # 默认获取一年的数据
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            
            # 获取基金净值数据
            fund_em_info_df = ak.fund_em_open_fund_info(fund=symbol, indicator="单位净值走势")
            
            # 获取基金基本信息
            try:
                fund_info_df = ak.fund_em_fund_info(fund=symbol)
                fund_info = {}
                if not fund_info_df.empty:
                    for _, row in fund_info_df.iterrows():
                        fund_info[row['明细']] = row['数据']
            except Exception as e:
                logger.warning(f"获取基金信息失败: {e}")
                fund_info = {}
            
            # 处理历史数据
            historical_data = []
            if not fund_em_info_df.empty:
                for _, row in fund_em_info_df.iterrows():
                    if start_date <= row.get('净值日期').replace('-', '') <= end_date:
                        historical_data.append({
                            'date': row.get('净值日期'),
                            'nav': float(row.get('单位净值')),
                            'accumulative_nav': float(row.get('累计净值')) if '累计净值' in row else None,
                            'change_pct': float(row.get('日增长率')) if '日增长率' in row else None
                        })
            
            # 构建结果
            result = {
                'symbol': symbol,
                'fund_name': fund_info.get('基金简称', ''),
                'fund_type': fund_info.get('基金类型', ''),
                'historical_data': historical_data,
                'fund_info': fund_info
            }
            
            return result
            
        except Exception as e:
            logger.error(f"获取基金数据失败: {e}")
            raise
    
    def get_index_data(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """获取指数数据"""
        try:
            # 处理日期参数
            end_date = kwargs.get('end_date', datetime.now().strftime('%Y%m%d'))
            start_date = kwargs.get('start_date')
            if not start_date:
                # 默认获取一年的数据
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            
            # 获取指数历史数据
            index_zh_a_hist_df = ak.index_zh_a_hist(
                symbol=symbol, 
                period="daily", 
                start_date=start_date, 
                end_date=end_date
            )
            
            # 处理历史数据
            historical_data = []
            if not index_zh_a_hist_df.empty:
                for _, row in index_zh_a_hist_df.iterrows():
                    historical_data.append({
                        'date': row.get('日期'),
                        'open': float(row.get('开盘')),
                        'high': float(row.get('最高')),
                        'low': float(row.get('最低')),
                        'close': float(row.get('收盘')),
                        'volume': float(row.get('成交量')),
                        'amount': float(row.get('成交额')) if '成交额' in row else None,
                        'change_pct': float(row.get('涨跌幅')) if '涨跌幅' in row else None
                    })
            
            # 获取指数成分股
            try:
                if symbol.startswith('0'):  # 上证指数
                    index_stock_cons_df = ak.index_stock_cons(symbol=f"sh{symbol}")
                elif symbol.startswith('3'):  # 深证指数
                    index_stock_cons_df = ak.index_stock_cons(symbol=f"sz{symbol}")
                else:
                    index_stock_cons_df = None
                
                constituent_stocks = []
                if index_stock_cons_df is not None and not index_stock_cons_df.empty:
                    for _, row in index_stock_cons_df.iterrows():
                        constituent_stocks.append({
                            'symbol': row.get('品种代码'),
                            'name': row.get('品种名称')
                        })
            except Exception as e:
                logger.warning(f"获取指数成分股失败: {e}")
                constituent_stocks = []
            
            # 构建结果
            result = {
                'symbol': symbol,
                'index_name': kwargs.get('index_name', ''),
                'historical_data': historical_data,
                'constituent_stocks': constituent_stocks
            }
            
            return result
            
        except Exception as e:
            logger.error(f"获取指数数据失败: {e}")
            raise
    
    def get_bond_data(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """获取债券数据"""
        try:
            # 处理日期参数
            end_date = kwargs.get('end_date', datetime.now().strftime('%Y%m%d'))
            start_date = kwargs.get('start_date')
            if not start_date:
                # 默认获取一年的数据
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            
            # 获取债券历史数据
            bond_zh_hs_cov_daily_df = ak.bond_zh_hs_cov_daily(
                symbol=symbol
            )
            
            # 处理历史数据
            historical_data = []
            if not bond_zh_hs_cov_daily_df.empty:
                for _, row in bond_zh_hs_cov_daily_df.iterrows():
                    date_str = row.get('日期')
                    if start_date <= date_str.replace('-', '') <= end_date:
                        historical_data.append({
                            'date': date_str,
                            'open': float(row.get('开盘')),
                            'high': float(row.get('最高')),
                            'low': float(row.get('最低')),
                            'close': float(row.get('收盘')),
                            'volume': float(row.get('成交量')),
                            'amount': float(row.get('成交额')) if '成交额' in row else None,
                            'change_pct': float(row.get('涨跌幅')) if '涨跌幅' in row else None
                        })
            
            # 获取债券基本信息
            try:
                bond_info_df = ak.bond_zh_cov_info(symbol=symbol)
                bond_info = {}
                if not bond_info_df.empty:
                    for _, row in bond_info_df.iterrows():
                        bond_info[row['item']] = row['value']
            except Exception as e:
                logger.warning(f"获取债券信息失败: {e}")
                bond_info = {}
            
            # 构建结果
            result = {
                'symbol': symbol,
                'bond_name': bond_info.get('债券名称', ''),
                'bond_type': '可转债',  # 默认为可转债
                'historical_data': historical_data,
                'bond_info': bond_info
            }
            
            return result
            
        except Exception as e:
            logger.error(f"获取债券数据失败: {e}")
            raise
    
    def get_industry_list(self) -> List[Dict[str, Any]]:
        """获取行业列表"""
        try:
            # 获取申万一级行业列表
            industry_list_df = ak.stock_sector_spot(indicator="申万一级")
            
            result = []
            if not industry_list_df.empty:
                for _, row in industry_list_df.iterrows():
                    result.append({
                        'name': row.get('板块名称'),
                        'change_pct': float(row.get('涨跌幅')),
                        'price': float(row.get('最新价')),
                        'volume': float(row.get('总成交量')),
                        'amount': float(row.get('总成交额'))
                    })
            
            return result
        except Exception as e:
            logger.error(f"获取行业列表失败: {e}")
            return []
    
    def get_industry_stocks(self, industry: str) -> List[Dict[str, Any]]:
        """获取行业成分股"""
        try:
            # 获取行业成分股
            stocks_df = ak.stock_sector_detail(sector=industry)
            
            result = []
            if not stocks_df.empty:
                for _, row in stocks_df.iterrows():
                    result.append({
                        'symbol': row.get('代码'),
                        'name': row.get('名称'),
                        'price': float(row.get('最新价')),
                        'change_pct': float(row.get('涨跌幅')),
                        'industry': industry
                    })
            
            return result
        except Exception as e:
            logger.error(f"获取行业成分股失败: {e}")
            return []
    
    def get_stock_news(self, symbol: str = None, count: int = 10) -> List[Dict[str, Any]]:
        """获取股票相关新闻"""
        try:
            if symbol:
                # 获取个股新闻
                news_df = ak.stock_news_em(symbol=symbol)
            else:
                # 获取财经新闻
                news_df = ak.news_economic()
            
            result = []
            if not news_df.empty:
                for _, row in news_df.iterrows():
                    if len(result) >= count:
                        break
                    
                    news_item = {}
                    if symbol:
                        news_item = {
                            'title': row.get('新闻标题'),
                            'date': row.get('发布时间'),
                            'content': row.get('新闻内容') if '新闻内容' in row else '',
                            'url': row.get('新闻链接') if '新闻链接' in row else ''
                        }
                    else:
                        news_item = {
                            'title': row.get('新闻标题'),
                            'date': row.get('发布日期'),
                            'content': row.get('新闻内容') if '新闻内容' in row else '',
                            'url': row.get('新闻链接') if '新闻链接' in row else ''
                        }
                    
                    result.append(news_item)
            
            return result
        except Exception as e:
            logger.error(f"获取新闻失败: {e}")
            return []
    
    def get_market_overview(self) -> Dict[str, Any]:
        """获取市场概览数据"""
        try:
            # 获取A股市场概览
            stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
            
            # 获取指数行情
            index_data = {}
            try:
                # 上证指数
                index_sh_df = ak.stock_zh_index_spot()
                for _, row in index_sh_df.iterrows():
                    code = row.get('代码')
                    if code in ['000001', '399001', '399006']:  # 上证指数、深证成指、创业板指
                        index_data[code] = {
                            'name': row.get('名称'),
                            'price': float(row.get('最新价')),
                            'change': float(row.get('涨跌额')),
                            'change_pct': float(row.get('涨跌幅')),
                            'volume': float(row.get('成交量')),
                            'amount': float(row.get('成交额'))
                        }
            except Exception as e:
                logger.warning(f"获取指数行情失败: {e}")
            
            # 统计市场数据
            up_count = 0
            down_count = 0
            limit_up_count = 0
            limit_down_count = 0
            total_amount = 0
            
            if not stock_zh_a_spot_em_df.empty:
                for _, row in stock_zh_a_spot_em_df.iterrows():
                    change_pct = row.get('涨跌幅')
                    if change_pct > 0:
                        up_count += 1
                    elif change_pct < 0:
                        down_count += 1
                    
                    if change_pct >= 9.5:  # 涨停
                        limit_up_count += 1
                    elif change_pct <= -9.5:  # 跌停
                        limit_down_count += 1
                    
                    total_amount += float(row.get('成交额', 0))
            
            # 构建结果
            result = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'indices': index_data,
                'market_stats': {
                    'total_stocks': len(stock_zh_a_spot_em_df) if not stock_zh_a_spot_em_df.empty else 0,
                    'up_count': up_count,
                    'down_count': down_count,
                    'limit_up_count': limit_up_count,
                    'limit_down_count': limit_down_count,
                    'total_amount': total_amount / 100000000  # 转换为亿元
                }
            }
            
            return result
        except Exception as e:
            logger.error(f"获取市场概览失败: {e}")
            return {"error": str(e)}