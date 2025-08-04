from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from app.services.collectors.yahoo_collector import YahooFinanceCollector
from app.services.processors.yahoo_processor import YahooDataProcessor
from app.utils.local_storage import local_storage
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/yahoo", tags=["Yahoo数据"])

# Pydantic模型
class StockSearchResult(BaseModel):
    symbol: str
    name: Optional[str] = None
    exchange: Optional[str] = None
    type: Optional[str] = None

class YahooDataResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

@router.get("/search", response_model=List[StockSearchResult], summary="🔍 搜索股票", operation_id="yahoo_search")
def search_stocks(query: str):
    """搜索股票"""
    collector = YahooFinanceCollector()
    results = collector.search_stocks(query)
    return results

@router.get("/stock/{ticker}", response_model=YahooDataResponse, summary="📊 获取股票数据", operation_id="yahoo_stock_data")
def get_stock_data(
    ticker: str,
    period: str = Query("1y", description="数据周期，如1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max"),
    interval: str = Query("1d", description="数据间隔，如1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo"),
    save: bool = Query(False, description="是否保存数据到本地存储")
):
    """获取股票数据"""
    try:
        # 收集数据
        collector = YahooFinanceCollector()
        data = collector.get_stock_data(ticker, period, interval)
        
        if "error" in data:
            return YahooDataResponse(success=False, message=data["error"])
        
        # 如果需要保存数据
        if save:
            processor = YahooDataProcessor()
            
            # 处理并保存公司数据
            company_data = processor.process_company_data(data)
            if "error" not in company_data:
                local_storage.save_company(company_data)
            
            # 处理并保存财务数据
            financial_data_list = processor.process_financial_data(data)
            for financial_data in financial_data_list:
                if "error" not in financial_data:
                    local_storage.save_financial_data(ticker, financial_data)
            
            # 处理并保存行业数据
            industry_data = processor.extract_industry_data(data)
            if "error" not in industry_data and industry_data.get("industry"):
                local_storage.save_industry_data(industry_data.get("industry"), industry_data)
        
        return YahooDataResponse(success=True, message="数据获取成功", data=data)
    
    except Exception as e:
        return YahooDataResponse(success=False, message=f"获取数据失败: {str(e)}")

@router.get("/market/{market}", response_model=YahooDataResponse, summary="🌍 获取市场数据", operation_id="yahoo_market_data")
def get_market_data(market: str):
    """获取市场数据"""
    try:
        collector = YahooFinanceCollector()
        data = collector.get_market_data(market)
        
        if "error" in data:
            return YahooDataResponse(success=False, message=data["error"])
        
        return YahooDataResponse(success=True, message="市场数据获取成功", data=data)
    
    except Exception as e:
        return YahooDataResponse(success=False, message=f"获取市场数据失败: {str(e)}")

@router.get("/industry/{industry_name}", response_model=YahooDataResponse, summary="🏭 获取行业股票", operation_id="yahoo_industry_stocks")
def get_industry_stocks(
    industry_name: str,
    limit: int = Query(10, description="返回的股票数量限制")
):
    """获取行业相关股票"""
    try:
        # 这里可以实现一个简单的行业股票查询
        # 实际应用中可能需要更复杂的实现
        collector = YahooFinanceCollector()
        
        # 使用行业名称作为搜索关键词
        stocks = collector.search_stocks(industry_name)
        
        # 限制返回数量
        stocks = stocks[:limit] if stocks else []
        
        return YahooDataResponse(
            success=True, 
            message=f"获取{industry_name}行业股票成功", 
            data={"industry": industry_name, "stocks": stocks}
        )
    
    except Exception as e:
        return YahooDataResponse(success=False, message=f"获取行业股票失败: {str(e)}")

@router.get("/batch", response_model=YahooDataResponse, summary="📦 批量获取股票数据", operation_id="yahoo_batch_data")
def batch_get_stocks(
    tickers: str = Query(..., description="股票代码列表，用逗号分隔"),
    period: str = Query("1mo", description="数据周期"),
    interval: str = Query("1d", description="数据间隔")
):
    """批量获取股票数据"""
    try:
        ticker_list = [t.strip() for t in tickers.split(",")]
        
        if not ticker_list:
            return YahooDataResponse(success=False, message="未提供有效的股票代码")
        
        collector = YahooFinanceCollector()
        data = collector.get_multiple_stocks(ticker_list, period, interval)
        
        return YahooDataResponse(success=True, message="批量获取数据成功", data=data)
    
    except Exception as e:
        return YahooDataResponse(success=False, message=f"批量获取数据失败: {str(e)}")