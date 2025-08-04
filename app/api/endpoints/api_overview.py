#!/usr/bin/env python3
"""
API概览页面
提供所有API的快速导航和说明
"""

from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/overview", tags=["API概览"])

@router.get("/", summary="📋 API概览页面", operation_id="api_overview")
def get_api_overview():
    """
    API概览页面
    
    提供所有API端点的快速导航和说明
    """
    return {
        "title": "金融分析系统API概览",
        "version": "1.0.0",
        "description": "智能金融分析系统，支持实时数据获取、历史数据分析、行业筛选等功能",
        "base_url": "http://localhost:8000/api/v1",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "api_groups": {
            "实时数据": {
                "description": "获取实时市场数据，支持AKShare数据源",
                "endpoints": {
                    "获取个股实时数据": {
                        "url": "/realtime/stock/{symbol}",
                        "method": "GET",
                        "description": "获取个股实时价格、成交量等数据",
                        "parameters": {
                            "symbol": "股票代码，如：000001",
                            "force_refresh": "强制刷新，默认false"
                        },
                        "example": "/realtime/stock/000001?force_refresh=true"
                    },
                    "获取行业公司列表": {
                        "url": "/realtime/companies/{industry}",
                        "method": "GET",
                        "description": "获取指定行业的实时公司列表",
                        "parameters": {
                            "industry": "行业名称，如：医药、新能源",
                            "force_refresh": "强制刷新，默认false"
                        },
                        "example": "/realtime/companies/医药?force_refresh=true"
                    },
                    "测试AKShare连接": {
                        "url": "/realtime/test/akshare",
                        "method": "GET",
                        "description": "测试AKShare数据源连接状态",
                        "example": "/realtime/test/akshare"
                    },
                    "获取缓存信息": {
                        "url": "/realtime/cache/info",
                        "method": "GET",
                        "description": "查看缓存状态和统计信息",
                        "example": "/realtime/cache/info"
                    }
                }
            },
            "历史数据": {
                "description": "获取历史数据，支持智能增量更新",
                "endpoints": {
                    "获取股票历史数据": {
                        "url": "/historical/stock/{symbol}",
                        "method": "GET",
                        "description": "获取股票历史数据，支持增量更新",
                        "parameters": {
                            "symbol": "股票代码，如：000001",
                            "start_date": "开始日期，格式：YYYY-MM-DD",
                            "end_date": "结束日期，格式：YYYY-MM-DD",
                            "period": "数据周期：daily/weekly/monthly",
                            "force_refresh": "强制刷新，默认false"
                        },
                        "example": "/historical/stock/000001?start_date=2023-01-01&end_date=2023-12-31&period=daily"
                    },
                    "获取数据统计": {
                        "url": "/historical/stock/{symbol}/statistics",
                        "method": "GET",
                        "description": "获取股票数据统计信息",
                        "parameters": {
                            "symbol": "股票代码，如：000001"
                        },
                        "example": "/historical/stock/000001/statistics"
                    },
                    "演示增量逻辑": {
                        "url": "/historical/incremental/demo",
                        "method": "GET",
                        "description": "演示增量更新逻辑和优势",
                        "example": "/historical/incremental/demo"
                    },
                    "查看缓存状态": {
                        "url": "/historical/cache/status",
                        "method": "GET",
                        "description": "查看历史数据缓存状态",
                        "example": "/historical/cache/status"
                    }
                }
            },
            "公司管理": {
                "description": "公司信息管理，支持本地存储",
                "endpoints": {
                    "获取公司列表": {
                        "url": "/companies/",
                        "method": "GET",
                        "description": "获取公司列表，支持行业筛选和分页",
                        "parameters": {
                            "industry": "行业筛选，如：医药、新能源",
                            "skip": "跳过记录数，用于分页",
                            "limit": "返回记录数限制，最大1000"
                        },
                        "example": "/companies/?industry=医药&skip=0&limit=50"
                    },
                    "获取公司详情": {
                        "url": "/companies/{company_code}",
                        "method": "GET",
                        "description": "获取指定公司的详细信息",
                        "parameters": {
                            "company_code": "公司代码，如：000001"
                        },
                        "example": "/companies/000001"
                    },
                    "获取公司财务数据": {
                        "url": "/companies/{company_code}/financial-data",
                        "method": "GET",
                        "description": "获取公司财务数据",
                        "parameters": {
                            "company_code": "公司代码，如：000001",
                            "data_type": "数据类型筛选",
                            "start_date": "开始日期",
                            "end_date": "结束日期"
                        },
                        "example": "/companies/000001/financial-data"
                    }
                }
            },
            "行业管理": {
                "description": "行业信息管理，支持智能匹配",
                "endpoints": {
                    "获取行业列表": {
                        "url": "/industries/",
                        "method": "GET",
                        "description": "获取所有支持的行业列表",
                        "example": "/industries/"
                    },
                    "获取行业建议": {
                        "url": "/industries/suggest/{query}",
                        "method": "GET",
                        "description": "获取行业建议，支持智能匹配",
                        "parameters": {
                            "query": "查询关键词，如：医药、medical"
                        },
                        "example": "/industries/suggest/医药"
                    },
                    "获取行业数据": {
                        "url": "/industries/{industry_name}/data",
                        "method": "GET",
                        "description": "获取指定行业的数据",
                        "parameters": {
                            "industry_name": "行业名称，如：医药",
                            "data_type": "数据类型筛选",
                            "start_date": "开始日期",
                            "end_date": "结束日期"
                        },
                        "example": "/industries/医药/data"
                    }
                }
            },
            "任务管理": {
                "description": "后台任务管理，支持任务创建和监控",
                "endpoints": {
                    "获取任务列表": {
                        "url": "/tasks/",
                        "method": "GET",
                        "description": "获取任务列表，支持状态筛选",
                        "parameters": {
                            "status": "任务状态筛选",
                            "task_type": "任务类型筛选",
                            "skip": "跳过记录数",
                            "limit": "返回记录数限制"
                        },
                        "example": "/tasks/?status=running&limit=10"
                    },
                    "创建任务": {
                        "url": "/tasks/",
                        "method": "POST",
                        "description": "创建新的后台任务",
                        "example": "POST /tasks/ (需要请求体)"
                    },
                    "获取任务详情": {
                        "url": "/tasks/{task_id}",
                        "method": "GET",
                        "description": "获取指定任务的详细信息",
                        "parameters": {
                            "task_id": "任务ID"
                        },
                        "example": "/tasks/12345"
                    }
                }
            }
        },
        "数据源": {
            "AKShare": "中国金融市场数据",
            "Yahoo Finance": "全球金融市场数据",
            "本地存储": "JSON/CSV文件存储"
        },
        "特性": [
            "实时数据获取",
            "智能增量更新",
            "行业智能匹配",
            "本地缓存机制",
            "多数据源支持",
            "RESTful API设计"
        ],
        "快速开始": {
            "1": "启动服务器：python run.py",
            "2": "访问文档：http://localhost:8000/docs",
            "3": "测试连接：GET /health",
            "4": "获取实时数据：GET /api/v1/realtime/stock/000001",
            "5": "获取历史数据：GET /api/v1/historical/stock/000001"
        }
    } 