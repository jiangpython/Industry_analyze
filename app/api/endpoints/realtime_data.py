#!/usr/bin/env python3
"""
实时数据API端点
支持混合模式：本地缓存 + 实时获取
"""

from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from app.services.realtime_data_service import realtime_service
from app.utils.industry_mapper import IndustryMapper

router = APIRouter(prefix="/realtime", tags=["realtime"])

# Pydantic模型
class StockDataResponse(BaseModel):
    code: str
    name: str
    current_price: Optional[float] = None
    change_percent: Optional[float] = None
    volume: Optional[float] = None
    turnover: Optional[float] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    industry: Optional[str] = None
    market: Optional[str] = None
    source: str
    update_time: str

class CompanyResponse(BaseModel):
    code: str
    name: str
    industry: str
    market: str
    current_price: Optional[float] = None
    change_percent: Optional[float] = None
    volume: Optional[float] = None
    turnover: Optional[float] = None
    market_cap: Optional[float] = None
    source: str
    update_time: str

class CacheInfoResponse(BaseModel):
    cache_key: str
    timestamp: str
    data_type: str

@router.get("/stock/{symbol}", response_model=StockDataResponse)
def get_stock_realtime_data(
    symbol: str = Path(..., description="股票代码，例如：000001（平安银行）、000002（万科A）、300750（宁德时代）"),
    force_refresh: bool = Query(False, description="强制刷新数据，忽略缓存。默认False，建议仅在需要最新数据时使用")
):
    """
    获取个股实时数据
    
    **输入参数说明：**
    - **symbol**: 股票代码（必填）
      - 格式：6位数字代码
      - 示例：000001、000002、300750
      - 支持A股所有股票代码
    
    - **force_refresh**: 强制刷新（可选）
      - 默认值：False
      - 说明：True=强制从网络获取最新数据，False=优先使用缓存
    
    **返回数据：**
    - 股票基本信息（代码、名称）
    - 实时价格数据（当前价、涨跌幅等）
    - 交易数据（成交量、成交额等）
    - 财务指标（市盈率、市净率等）
    - 数据来源和时间戳
    
    **使用示例：**
    ```
    GET /api/v1/realtime/stock/000001
    GET /api/v1/realtime/stock/000001?force_refresh=true
    ```
    """
    try:
        data = realtime_service.get_stock_realtime_data(symbol, force_refresh)
        
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
        
        return StockDataResponse(**data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票数据失败: {str(e)}")

@router.get("/companies/{industry}", response_model=List[CompanyResponse])
def get_companies_realtime(
    industry: str = Path(..., description="行业名称，支持中文和英文。例如：医药、新能源、半导体、medical、new_energy、semiconductor"),
    force_refresh: bool = Query(False, description="强制刷新数据，忽略缓存。默认False，建议仅在需要最新数据时使用")
):
    """
    获取指定行业的公司列表（实时）
    
    **输入参数说明：**
    - **industry**: 行业名称（必填）
      - 支持中文：医药、新能源、半导体、芯片、电子、计算机、通信、金融、房地产、汽车、化工、钢铁、有色金属、建筑材料、农林牧渔、食品饮料、纺织服装、轻工制造、医药生物、公用事业、交通运输、商业贸易、休闲服务、综合
      - 支持英文：medical、new_energy、semiconductor、chip、electronics、computer、communication、finance、real_estate、auto、chemical、steel、nonferrous_metals、building_materials、agriculture、food_beverage、textile_clothing、light_industry、pharmaceutical、utilities、transportation、commercial_trade、leisure_service、comprehensive
      - 支持模糊匹配和别名识别
    
    - **force_refresh**: 强制刷新（可选）
      - 默认值：False
      - 说明：True=强制从网络获取最新数据，False=优先使用缓存
    
    **返回数据：**
    - 行业公司列表（代码、名称、行业、市场）
    - 实时价格数据（当前价、涨跌幅等）
    - 交易数据（成交量、成交额等）
    - 数据来源和时间戳
    
    **使用示例：**
    ```
    GET /api/v1/realtime/companies/医药
    GET /api/v1/realtime/companies/新能源?force_refresh=true
    GET /api/v1/realtime/companies/semiconductor
    ```
    """
    try:
        # 使用行业映射器
        mapped_industry = IndustryMapper.map_industry(industry)
        if not mapped_industry:
            suggestions = IndustryMapper.get_suggestions(industry)
            raise HTTPException(
                status_code=400, 
                detail=f"未找到行业 '{industry}'，建议: {suggestions}"
            )
        
        companies = realtime_service.get_companies_by_industry_realtime(
            mapped_industry, force_refresh
        )
        
        return [CompanyResponse(**company) for company in companies]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行业数据失败: {str(e)}")

@router.get("/cache/info", response_model=Dict[str, CacheInfoResponse])
def get_cache_info():
    """获取缓存信息"""
    try:
        from app.utils.data_manager import data_manager
        cache_info = data_manager.get_cache_info()
        
        # 转换为响应格式
        response = {}
        for key, info in cache_info.items():
            response[key] = CacheInfoResponse(
                cache_key=key,
                timestamp=info.get("timestamp", ""),
                data_type=info.get("data_type", "")
            )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取缓存信息失败: {str(e)}")

@router.delete("/cache")
def clear_cache(cache_key: Optional[str] = Query(None, description="指定缓存键，为空则清除所有缓存")):
    """清除缓存"""
    try:
        from app.utils.data_manager import data_manager
        success = data_manager.clear_cache(cache_key)
        
        if success:
            return {"message": f"缓存清除成功: {cache_key or '所有缓存'}"}
        else:
            raise HTTPException(status_code=500, detail="缓存清除失败")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清除缓存失败: {str(e)}")

@router.get("/test/akshare")
def test_akshare_connection():
    """测试AKShare连接"""
    try:
        import akshare as ak
        
        # 尝试获取A股股票列表
        df = ak.stock_zh_a_spot_em()
        
        return {
            "status": "success",
            "message": "AKShare连接正常",
            "data_count": len(df),
            "sample_data": df.head(3).to_dict('records') if not df.empty else []
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"AKShare连接失败: {str(e)}",
            "data_count": 0,
            "sample_data": []
        }

@router.get("/summary")
def get_realtime_summary():
    """获取实时数据摘要"""
    try:
        from app.utils.data_manager import data_manager
        
        # 获取缓存信息
        cache_info = data_manager.get_cache_info()
        
        # 获取数据摘要
        data_summary = data_manager.get_data_summary()
        
        return {
            "cache_count": len(cache_info),
            "cache_keys": list(cache_info.keys()),
            "data_summary": data_summary,
            "akshare_status": test_akshare_connection(),
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取摘要失败: {str(e)}") 