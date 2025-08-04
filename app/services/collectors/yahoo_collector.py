import yfinance as yf
from typing import Dict, Any, List, Optional
from app.services.collectors.base_collector import BaseCollector
import logging

logger = logging.getLogger(__name__)

class YahooFinanceCollector(BaseCollector):
    """Yahoo Finance数据采集器"""
    
    def __init__(self):
        super().__init__()
        
    def collect(self, **kwargs) -> Dict[str, Any]:
        """实现基类的数据采集方法"""
        ticker_symbol = kwargs.get('ticker')
        period = kwargs.get('period', '1y')
        interval = kwargs.get('interval', '1d')
        
        if not ticker_symbol:
            logger.error("未提供股票代码")
            return {"error": "未提供股票代码"}
        
        try:
            data = self.get_stock_data(ticker_symbol, period, interval)
            return data
        except Exception as e:
            logger.error(f"获取Yahoo数据失败: {e}")
            return {"error": f"获取数据失败: {str(e)}"}
    
    def get_stock_data(self, ticker: str, period: str = '1y', interval: str = '1d') -> Dict[str, Any]:
        """获取股票数据"""
        try:
            # 创建Ticker对象
            stock = yf.Ticker(ticker)
            
            # 获取历史数据
            hist = stock.history(period=period, interval=interval)
            
            # 获取公司信息
            info = stock.info
            
            # 获取财务数据
            financials = {}
            balance_sheet = {}
            cash_flow = {}
            
            try:
                financials = stock.financials.to_dict() if hasattr(stock, 'financials') and not stock.financials.empty else {}
            except Exception as e:
                logger.warning(f"获取财务数据失败: {e}")
                
            try:
                balance_sheet = stock.balance_sheet.to_dict() if hasattr(stock, 'balance_sheet') and not stock.balance_sheet.empty else {}
            except Exception as e:
                logger.warning(f"获取资产负债表失败: {e}")
                
            try:
                cash_flow = stock.cashflow.to_dict() if hasattr(stock, 'cashflow') and not stock.cashflow.empty else {}
            except Exception as e:
                logger.warning(f"获取现金流量表失败: {e}")
            
            # 处理历史数据
            historical_data = []
            if not hist.empty:
                for date, row in hist.iterrows():
                    historical_data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'open': float(row.get('Open', 0)),
                        'high': float(row.get('High', 0)),
                        'low': float(row.get('Low', 0)),
                        'close': float(row.get('Close', 0)),
                        'volume': int(row.get('Volume', 0))
                    })
            
            # 构建结果
            result = {
                'symbol': ticker,
                'company_name': info.get('shortName', ''),
                'industry': info.get('industry', ''),
                'sector': info.get('sector', ''),
                'market_cap': info.get('marketCap'),
                'historical_data': historical_data,
                'financials': {
                    'income_statement': financials,
                    'balance_sheet': balance_sheet,
                    'cash_flow': cash_flow
                },
                'info': info
            }
            
            return result
            
        except Exception as e:
            logger.error(f"获取股票数据失败: {e}")
            raise
    
    def get_multiple_stocks(self, tickers: List[str], period: str = '1y', interval: str = '1d') -> Dict[str, Dict[str, Any]]:
        """获取多个股票的数据"""
        results = {}
        for ticker in tickers:
            try:
                results[ticker] = self.get_stock_data(ticker, period, interval)
            except Exception as e:
                logger.error(f"获取股票 {ticker} 数据失败: {e}")
                results[ticker] = {"error": str(e)}
        
        return results
    
    def search_stocks(self, query: str) -> List[Dict[str, Any]]:
        """搜索股票"""
        try:
            # 使用yfinance的Search功能
            search_result = yf.Ticker(query)  # 简单搜索方式
            
            # 如果是有效股票，返回其信息
            if hasattr(search_result, 'info'):
                info = search_result.info
                return [{
                    'symbol': info.get('symbol', query),
                    'name': info.get('shortName', ''),
                    'exchange': info.get('exchange', ''),
                    'type': info.get('quoteType', '')
                }]
            return []
        except Exception as e:
            logger.error(f"搜索股票失败: {e}")
            return []
    
    def get_market_data(self, market: str) -> Dict[str, Any]:
        """获取市场数据"""
        try:
            # 使用yfinance获取市场指数
            if market.lower() == 'us':
                indices = ['^GSPC', '^DJI', '^IXIC']  # S&P 500, 道琼斯, 纳斯达克
            elif market.lower() == 'china':
                indices = ['^SSEC', '^SZSC', '^HSI']  # 上证指数, 深证成指, 恒生指数
            else:
                indices = [market]
                
            market_data = {}
            for index in indices:
                try:
                    ticker = yf.Ticker(index)
                    hist = ticker.history(period='1d')
                    if not hist.empty:
                        latest = hist.iloc[-1]
                        market_data[index] = {
                            'name': ticker.info.get('shortName', index),
                            'last_price': float(latest.get('Close', 0)),
                            'change': float(latest.get('Close', 0) - hist.iloc[-2].get('Close', 0)) if len(hist) > 1 else 0,
                            'change_percent': float((latest.get('Close', 0) / hist.iloc[-2].get('Close', 0) - 1) * 100) if len(hist) > 1 else 0,
                            'volume': int(latest.get('Volume', 0))
                        }
                except Exception as e:
                    logger.error(f"获取指数 {index} 数据失败: {e}")
            
            return {
                'market': market,
                'indices': market_data
            }
        except Exception as e:
            logger.error(f"获取市场数据失败: {e}")
            return {"error": str(e)}