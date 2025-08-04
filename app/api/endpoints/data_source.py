from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from app.services.collectors.data_source_selector import DataSourceSelector
from app.services.processors.yahoo_processor import YahooDataProcessor
from app.services.processors.akshare_processor import AKShareDataProcessor
from app.utils.local_storage import local_storage
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/data", tags=["data"])

# Pydantic模型
class DataSourceResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    source: str

class StockSearchResult(BaseModel):
    symbol: str
    name: Optional[str] = None
    exchange: Optional[str] = None
    price: Optional[float] = None
    change_pct: Optional[float] = None

# 创建数据源选择器实例
data_selector = DataSourceSelector()

@router.get("/stock/{symbol}", response_model=DataSourceResponse)
def get_stock_data(
    symbol: str,
    source: str = Query("auto", description="数据源: auto, yahoo, akshare"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: str = Query("1y", description="数据周期，如1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max"),
    interval: str = Query("1d", description="数据间隔，如1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo"),
    adjust: str = Query("", description="价格复权类型: '', qfq(前复权), hfq(后复权)"),
    save: bool = Query(False, description="是否保存数据到本地存储")
):
    """获取股票数据，可以灵活选择数据源"""
    try:
        # 获取数据
        data = data_selector.get_stock_data(
            symbol=symbol,
            source=source,
            start_date=start_date,
            end_date=end_date,
            period=period,
            interval=interval,
            adjust=adjust
        )
        
        if "error" in data:
            return DataSourceResponse(success=False, message=data["error"], source=source)
        
        # 确定实际使用的数据源
        actual_source = source
        if source == "auto":
            if symbol.startswith(('0', '3', '6')):
                actual_source = "akshare"
            else:
                actual_source = "yahoo"
        
        # 如果需要保存数据
        if save:
            if actual_source == "yahoo":
                processor = YahooDataProcessor()
            else:
                processor = AKShareDataProcessor()
            
            # 处理并保存公司数据
            company_data = processor.process_company_data(data)
            if "error" not in company_data:
                local_storage.save_company(company_data)
            
            # 处理并保存财务数据
            financial_data_list = processor.process_financial_data(data)
            for financial_data in financial_data_list:
                if "error" not in financial_data:
                    local_storage.save_financial_data(symbol, financial_data)
        
        return DataSourceResponse(success=True, message="数据获取成功", data=data, source=actual_source)
    
    except Exception as e:
        return DataSourceResponse(success=False, message=f"获取数据失败: {str(e)}", source=source)

@router.get("/market/{market}", response_model=DataSourceResponse)
def get_market_data(
    market: str,
    source: str = Query("auto", description="数据源: auto, yahoo, akshare")
):
    """获取市场数据，可以灵活选择数据源"""
    try:
        # 获取数据
        data = data_selector.get_market_data(market=market, source=source)
        
        if "error" in data:
            return DataSourceResponse(success=False, message=data["error"], source=source)
        
        # 确定实际使用的数据源
        actual_source = source
        if source == "auto":
            if market.lower() in ['china', 'cn', 'a股', '沪深', '沪深300']:
                actual_source = "akshare"
            else:
                actual_source = "yahoo"
        
        return DataSourceResponse(success=True, message="市场数据获取成功", data=data, source=actual_source)
    
    except Exception as e:
        return DataSourceResponse(success=False, message=f"获取市场数据失败: {str(e)}", source=source)

@router.get("/industry/{industry}", response_model=DataSourceResponse)
def get_industry_data(
    industry: str,
    source: str = Query("akshare", description="数据源: akshare"),
    save: bool = Query(False, description="是否保存行业数据到本地存储")
):
    """获取行业数据，目前主要支持AKShare"""
    try:
        # 获取数据
        data = data_selector.get_industry_data(industry=industry, source=source)
        
        if "error" in data:
            return DataSourceResponse(success=False, message=data["error"], source=source)
        
        # 如果需要保存数据
        if save:
            processor = AKShareDataProcessor()
            
            # 处理并保存行业数据
            industry_data = processor.process_industry_data(data)
            if "error" not in industry_data:
                local_storage.save_industry_data(industry, industry_data)
        
        return DataSourceResponse(success=True, message=f"获取{industry}行业数据成功", data=data, source=source)
    
    except Exception as e:
        return DataSourceResponse(success=False, message=f"获取行业数据失败: {str(e)}", source=source)

@router.get("/search", response_model=List[StockSearchResult])
def search_stocks(
    query: str,
    source: str = Query("auto", description="数据源: auto, yahoo, akshare")
):
    """搜索股票，可以灵活选择数据源"""
    try:
        # 搜索股票
        results = data_selector.search_stocks(query=query, source=source)
        
        # 转换为响应模型
        response = []
        for item in results:
            response.append(StockSearchResult(
                symbol=item.get("symbol", ""),
                name=item.get("name", ""),
                exchange=item.get("exchange", ""),
                price=item.get("price"),
                change_pct=item.get("change_pct")
            ))
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索股票失败: {str(e)}")