#!/usr/bin/env python3
"""
历史数据API端点
支持增量数据获取
"""

from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from app.services.incremental_data_service import incremental_service

router = APIRouter(prefix="/historical", tags=["historical"])

# Pydantic模型
class HistoricalDataResponse(BaseModel):
    symbol: str
    period: str
    total_records: int
    date_range: Dict[str, str]
    data: List[Dict[str, Any]]
    source: str
    last_updated: str

class DataStatisticsResponse(BaseModel):
    symbol: str
    total_records: int
    date_range: Dict[str, str]
    price_stats: Dict[str, float]
    volume_stats: Dict[str, float]
    last_updated: str

@router.get("/stock/{symbol}", response_model=HistoricalDataResponse)
def get_stock_historical_data(
    symbol: str = Path(..., description="股票代码，6位数字。例如：000001（平安银行）、000002（万科A）、300750（宁德时代）"),
    start_date: Optional[str] = Query(None, description="开始日期，格式：YYYY-MM-DD。例如：2023-01-01。默认：1年前"),
    end_date: Optional[str] = Query(None, description="结束日期，格式：YYYY-MM-DD。例如：2023-12-31。默认：今天"),
    period: str = Query("daily", description="数据周期：daily（日线）、weekly（周线）、monthly（月线）。默认：daily"),
    force_refresh: bool = Query(False, description="强制刷新数据，忽略缓存。默认False，建议仅在需要最新数据时使用")
):
    """
    获取股票历史数据（支持智能增量更新）
    
    **输入参数说明：**
    - **symbol**: 股票代码（必填）
      - 格式：6位数字代码
      - 示例：000001、000002、300750
      - 支持A股所有股票代码
    
    - **start_date**: 开始日期（可选）
      - 格式：YYYY-MM-DD
      - 示例：2023-01-01、2023-06-01
      - 默认：1年前
    
    - **end_date**: 结束日期（可选）
      - 格式：YYYY-MM-DD
      - 示例：2023-12-31、2024-01-01
      - 默认：今天
    
    - **period**: 数据周期（可选）
      - daily：日线数据（默认）
      - weekly：周线数据
      - monthly：月线数据
    
    - **force_refresh**: 强制刷新（可选）
      - 默认值：False
      - 说明：True=强制全量获取，False=智能增量更新
    
    **智能增量更新特性：**
    - 自动检查本地缓存
    - 只获取缺失的数据
    - 智能合并新旧数据
    - 节省网络请求和响应时间
    
    **返回数据：**
    - 股票基本信息（代码、周期）
    - 历史价格数据（开盘、最高、最低、收盘）
    - 交易数据（成交量、成交额、换手率）
    - 涨跌数据（涨跌幅、涨跌额、振幅）
    - 数据统计（总记录数、日期范围）
    - 数据来源和时间戳
    
    **使用示例：**
    ```
    # 获取最近1年日线数据（智能增量）
    GET /api/v1/historical/stock/000001
    
    # 获取指定日期范围
    GET /api/v1/historical/stock/000001?start_date=2023-01-01&end_date=2023-12-31
    
    # 获取周线数据
    GET /api/v1/historical/stock/000001?period=weekly
    
    # 强制刷新获取最新数据
    GET /api/v1/historical/stock/000001?force_refresh=true
    ```
    """
    try:
        data = incremental_service.get_stock_historical_data(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            period=period,
            force_refresh=force_refresh
        )
        
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
        
        return HistoricalDataResponse(**data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史数据失败: {str(e)}")

@router.get("/stock/{symbol}/statistics", response_model=DataStatisticsResponse)
def get_stock_data_statistics(
    symbol: str = Path(..., description="股票代码，6位数字。例如：000001（平安银行）、000002（万科A）、300750（宁德时代）")
):
    """
    获取股票数据统计信息
    
    **输入参数说明：**
    - **symbol**: 股票代码（必填）
      - 格式：6位数字代码
      - 示例：000001、000002、300750
      - 支持A股所有股票代码
    
    **返回数据：**
    - 数据概览（总记录数、日期范围）
    - 价格统计（最低价、最高价、平均价）
    - 成交量统计（总成交量、平均成交量）
    - 更新时间
    
    **统计说明：**
    - 基于缓存的历史数据计算
    - 包含完整的交易日期范围
    - 提供价格和成交量的关键指标
    
    **使用示例：**
    ```
    GET /api/v1/historical/stock/000001/statistics
    GET /api/v1/historical/stock/300750/statistics
    ```
    """
    try:
        stats = incremental_service.get_data_statistics(symbol)
        
        if "error" in stats:
            raise HTTPException(status_code=404, detail=stats["error"])
        
        if "message" in stats:
            raise HTTPException(status_code=404, detail=stats["message"])
        
        return DataStatisticsResponse(**stats)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")

@router.get("/incremental/demo")
def demonstrate_incremental_logic():
    """
    演示增量更新逻辑
    """
    demo_scenarios = {
        "scenario_1": {
            "description": "用户请求1年数据，本地有300天缓存",
            "request": "获取000001最近365天数据",
            "cache_status": "本地有300天数据 (2023-01-01 到 2023-10-28)",
            "incremental_action": "只获取最近65天数据 (2023-10-29 到 2024-01-01)",
            "efficiency_gain": "节省82%的网络请求 (300/365)"
        },
        "scenario_2": {
            "description": "用户请求特定日期范围",
            "request": "获取000001 2023-06-01 到 2023-12-31 数据",
            "cache_status": "本地有完整数据",
            "incremental_action": "直接返回缓存数据，无需网络请求",
            "efficiency_gain": "100%使用缓存，零网络请求"
        },
        "scenario_3": {
            "description": "缓存过期，需要更新",
            "request": "获取000001最近30天数据",
            "cache_status": "本地有数据但已过期",
            "incremental_action": "检查数据完整性，补充缺失日期",
            "efficiency_gain": "只获取缺失数据，避免重复获取"
        }
    }
    
    return {
        "message": "增量更新逻辑演示",
        "scenarios": demo_scenarios,
        "benefits": [
            "减少网络请求次数",
            "提高响应速度",
            "节省带宽和计算资源",
            "智能数据合并和去重"
        ],
        "cache_strategy": {
            "daily_data": "缓存1天",
            "minute_data": "缓存5分钟",
            "storage": "./data/cache.json"
        }
    }

@router.get("/cache/status")
def get_cache_status():
    """
    获取缓存状态信息
    """
    try:
        from app.utils.data_manager import data_manager
        
        cache_info = data_manager.get_cache_info()
        historical_caches = {}
        
        # 筛选历史数据缓存
        for key, info in cache_info.items():
            if key.startswith("historical_"):
                historical_caches[key] = info
        
        return {
            "total_cache_count": len(cache_info),
            "historical_cache_count": len(historical_caches),
            "historical_caches": historical_caches,
            "cache_keys": list(cache_info.keys())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取缓存状态失败: {str(e)}")

@router.delete("/cache/{symbol}")
def clear_symbol_cache(
    symbol: str,
    period: Optional[str] = Query(None, description="数据周期，为空则清除所有周期")
):
    """
    清除指定股票的缓存
    """
    try:
        from app.utils.data_manager import data_manager
        
        if period:
            cache_key = f"historical_{symbol}_{period}"
            success = data_manager.clear_cache(cache_key)
        else:
            # 清除该股票的所有周期缓存
            cache_info = data_manager.get_cache_info()
            cleared_count = 0
            for key in cache_info.keys():
                if key.startswith(f"historical_{symbol}_"):
                    if data_manager.clear_cache(key):
                        cleared_count += 1
            success = cleared_count > 0
        
        if success:
            return {"message": f"清除 {symbol} 缓存成功"}
        else:
            raise HTTPException(status_code=404, detail="未找到相关缓存")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清除缓存失败: {str(e)}")

@router.get("/test/incremental")
def test_incremental_functionality():
    """
    测试增量功能
    """
    test_results = {
        "test_1": {
            "description": "测试获取000001历史数据",
            "symbol": "000001",
            "period": "daily",
            "date_range": "最近30天"
        },
        "test_2": {
            "description": "测试强制刷新",
            "symbol": "000001",
            "force_refresh": True
        },
        "test_3": {
            "description": "测试数据统计",
            "symbol": "000001"
        }
    }
    
    return {
        "message": "增量功能测试",
        "tests": test_results,
        "usage_examples": [
            "GET /api/v1/historical/stock/000001",
            "GET /api/v1/historical/stock/000001?start_date=2023-01-01&end_date=2023-12-31",
            "GET /api/v1/historical/stock/000001?force_refresh=true",
            "GET /api/v1/historical/stock/000001/statistics"
        ]
    } 