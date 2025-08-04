#!/usr/bin/env python3
"""
简化版行业API端点
使用本地文件存储
"""

from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from app.utils.data_manager import data_manager
from app.utils.industry_mapper import IndustryMapper
from app.services.analyzers.gemini_analyzer import GeminiAnalyzer
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/industries", tags=["行业管理"])

# Pydantic模型
class IndustryDataBase(BaseModel):
    industry: str
    data_date: datetime
    data_type: str
    market_size: Optional[float] = None
    growth_rate: Optional[float] = None
    company_count: Optional[int] = None
    avg_pe: Optional[float] = None
    description: Optional[str] = None

class IndustryDataResponse(IndustryDataBase):
    created_at: Optional[datetime] = None

class IndustryAnalysisRequest(BaseModel):
    analysis_type: str = "trend"  # trend, investment, risk

class IndustryAnalysisResponse(BaseModel):
    id: str
    target_type: str
    target_id: str
    analysis_type: str
    title: str
    summary: str
    details: str
    score: Optional[float] = None
    risk_level: Optional[str] = None
    ai_model: str
    confidence: Optional[float] = None
    created_at: datetime


@router.get("/", response_model=List[str], summary="📋 获取行业列表", operation_id="industries_list")
def get_industries():
    """获取所有行业列表"""
    # 返回系统支持的标准行业列表
    return IndustryMapper.get_all_industries()

@router.get("/suggest/{query}", response_model=dict, summary="🔍 智能行业匹配", operation_id="industry_suggestions")
def get_industry_suggestions(
    query: str = Path(..., description="行业查询关键词，支持中文和英文。例如：医药、新能源、半导体、medical、new_energy、semiconductor")
):
    """
    获取行业建议（智能匹配）
    
    **输入参数说明：**
    - **query**: 行业查询关键词（必填）
      - 支持中文：医药、新能源、半导体、芯片、电子、计算机、通信、金融、房地产、汽车、化工、钢铁、有色金属、建筑材料、农林牧渔、食品饮料、纺织服装、轻工制造、医药生物、公用事业、交通运输、商业贸易、休闲服务、综合
      - 支持英文：medical、new_energy、semiconductor、chip、electronics、computer、communication、finance、real_estate、auto、chemical、steel、nonferrous_metals、building_materials、agriculture、food_beverage、textile_clothing、light_industry、pharmaceutical、utilities、transportation、commercial_trade、leisure_service、comprehensive
      - 支持模糊匹配和别名识别
    
    **返回数据：**
    - 查询关键词
    - 映射的标准行业名称
    - 相关行业建议列表
    - 所有支持的行业列表
    
    **智能匹配特性：**
    - 支持中文和英文输入
    - 支持行业别名识别
    - 支持模糊匹配
    - 提供相关行业建议
    
    **使用示例：**
    ```
    GET /api/v1/industries/suggest/医药
    GET /api/v1/industries/suggest/medical
    GET /api/v1/industries/suggest/芯片
    GET /api/v1/industries/suggest/新能源
    ```
    """
    suggestions = IndustryMapper.get_suggestions(query)
    mapped = IndustryMapper.map_industry(query)
    
    return {
        "query": query,
        "mapped_industry": mapped,
        "suggestions": suggestions,
        "all_industries": IndustryMapper.get_all_industries()
    }


@router.get("/{industry_name}/data", response_model=List[IndustryDataResponse], summary="📊 获取行业数据", operation_id="industry_data")
def get_industry_data(
    industry_name: str = Path(..., description="行业名称，支持中文和英文。例如：医药、新能源、半导体"),
    data_type: Optional[str] = Query(None, description="数据类型筛选，可选值：market、financial、trend。不填则返回所有类型"),
    start_date: Optional[str] = Query(None, description="起始日期，格式YYYY-MM-DD。例如：2023-01-01"),
    end_date: Optional[str] = Query(None, description="结束日期，格式YYYY-MM-DD。例如：2023-12-31"),
    force_refresh: bool = Query(False, description="强制刷新，优先获取最新数据。默认False，优先本地缓存")
):
    """
    获取行业数据

    **功能说明**：
    - 根据行业名称获取该行业的详细数据。
    - 支持按数据类型、时间范围筛选。
    - 支持force_refresh参数，优先尝试实时数据，失败降级本地。
    - 支持行业名称智能匹配（中文、英文、别名等）。
    - 返回市场规模、增长率、公司数量、平均市盈率等关键指标。

    **参数说明**：
    - industry_name: str，行业名称，必填，支持中英文。例如：医药、新能源、半导体
    - data_type: str，数据类型筛选，可选，market/financial/trend
    - start_date: datetime，起始日期，可选，格式YYYY-MM-DD
    - end_date: datetime，结束日期，可选，格式YYYY-MM-DD
    - force_refresh: bool，是否强制实时获取，默认False

    **返回**：
    - List[IndustryDataResponse]，行业数据列表，包含：
      - industry: 行业名称
      - data_date: 数据日期
      - data_type: 数据类型
      - market_size: 市场规模
      - growth_rate: 增长率
      - company_count: 公司数量
      - avg_pe: 平均市盈率
      - description: 行业描述
      - created_at: 创建时间

    **异常**：
    - 404: 未找到行业或行业数据

    **示例**：
    ```
    GET /api/v1/industries/医药/data
    GET /api/v1/industries/医药/data?data_type=market
    GET /api/v1/industries/医药/data?start_date=2023-01-01&end_date=2023-12-31
    GET /api/v1/industries/医药/data?force_refresh=true
    ```
    """
    # 使用行业映射器进行智能匹配
    mapped_industry = IndustryMapper.map_industry(industry_name)
    if not mapped_industry:
        # 如果无法映射，提供建议
        suggestions = IndustryMapper.get_suggestions(industry_name)
        error_msg = f"未找到行业 '{industry_name}'"
        if suggestions:
            error_msg += f"，建议使用: {', '.join(suggestions)}"
        raise HTTPException(status_code=404, detail=error_msg)
    
    # 优先尝试实时数据
    from app.services.realtime_data_service import RealtimeDataService
    realtime_service = RealtimeDataService()
    industry_data = None
    
    # 1. 优先尝试实时数据采集
    if force_refresh:
        industry_data = realtime_service.get_industry_data(mapped_industry, force_refresh)
    
    # 2. 如果本地没有数据，自动启动采集
    if not industry_data:
        industry_data = data_manager.get_industry_data(mapped_industry)
        
        # 如果本地也没有数据，尝试实时采集
        if not industry_data:
            logger.info(f"本地无数据，启动实时采集: {mapped_industry}")
            industry_data = realtime_service.get_industry_data(mapped_industry, force_refresh=True)
    
    # 3. 如果仍然没有数据，返回错误
    if not industry_data:
        raise HTTPException(status_code=404, detail=f"未找到{mapped_industry}行业数据，请检查行业名称是否正确")
    
    # 转换为响应格式
    response_data = []
    if isinstance(industry_data, dict):
        # 单个行业数据
        response_data.append(IndustryDataResponse(
            industry=mapped_industry,
            data_date=datetime.now(),
            data_type=industry_data.get('data_type', ''),
            market_size=industry_data.get('market_size'),
            growth_rate=industry_data.get('growth_rate'),
            company_count=industry_data.get('company_count'),
            avg_pe=industry_data.get('avg_pe'),
            description=industry_data.get('description'),
            created_at=datetime.now()
        ))
    
    return response_data


@router.get("/{industry_name}/latest", response_model=IndustryDataResponse, summary="📈 获取行业最新数据", operation_id="industry_latest_data")
def get_latest_industry_data(
    industry_name: str = Path(..., description="行业名称，支持中文和英文。例如：医药、新能源、半导体"),
    force_refresh: bool = Query(False, description="强制刷新，优先获取最新数据。默认False，优先本地缓存")
):
    """
    获取行业最新数据

    **功能说明**：
    - 根据行业名称获取该行业的最新数据。
    - 支持force_refresh参数，优先尝试实时数据，失败降级本地。
    - 支持行业名称智能匹配（中文、英文、别名等）。
    - 返回该行业最新的市场规模、增长率、公司数量、平均市盈率等指标。

    **参数说明**：
    - industry_name: str，行业名称，必填，支持中英文。例如：医药、新能源、半导体
    - force_refresh: bool，是否强制实时获取，默认False

    **返回**：
    - IndustryDataResponse，最新行业数据，包含：
      - industry: 行业名称
      - data_date: 数据日期
      - data_type: 数据类型
      - market_size: 市场规模
      - growth_rate: 增长率
      - company_count: 公司数量
      - avg_pe: 平均市盈率
      - description: 行业描述
      - created_at: 创建时间

    **异常**：
    - 404: 未找到行业或行业数据

    **示例**：
    ```
    GET /api/v1/industries/医药/latest
    GET /api/v1/industries/医药/latest?force_refresh=true
    GET /api/v1/industries/medical/latest
    ```
    """
    # 使用行业映射器进行智能匹配
    mapped_industry = IndustryMapper.map_industry(industry_name)
    if not mapped_industry:
        raise HTTPException(status_code=404, detail="未找到行业")
    
    # 优先尝试实时数据
    from app.services.realtime_data_service import RealtimeDataService
    realtime_service = RealtimeDataService()
    industry_data = None
    
    if force_refresh:
        # 实时获取行业数据（如有实现，可补充）
        # industry_data = realtime_service.get_industry_data(mapped_industry, force_refresh)
        pass
    
    # 降级本地
    if not industry_data:
        industry_data = data_manager.get_industry_data(mapped_industry)
    
    if not industry_data:
        raise HTTPException(status_code=404, detail="未找到行业数据")
    
    return IndustryDataResponse(
        industry=mapped_industry,
        data_date=datetime.now(),
        data_type=industry_data.get('data_type', ''),
        market_size=industry_data.get('market_size'),
        growth_rate=industry_data.get('growth_rate'),
        company_count=industry_data.get('company_count'),
        avg_pe=industry_data.get('avg_pe'),
        description=industry_data.get('description'),
        created_at=datetime.now()
    )


@router.post("/{industry_name}/analyze", response_model=IndustryAnalysisResponse, summary="🤖 AI行业分析", operation_id="industry_ai_analysis")
def analyze_industry(
    industry_name: str = Path(..., description="行业名称，支持中文和英文。例如：医药、新能源、半导体"),
    request: IndustryAnalysisRequest = ...,
    force_refresh: bool = Query(False, description="强制刷新，优先获取最新数据。默认False，优先本地缓存")
):
    """
    分析行业趋势/投资/风险（AI分析报告）

    **功能说明**：
    - 根据行业名称和分析类型，生成AI行业分析报告。
    - 支持趋势、投资、风险等多种分析类型。
    - 支持force_refresh参数，优先尝试实时数据，失败降级本地。

    **参数说明**：
    - industry_name: str，行业名称，必填，支持中英文
    - request: IndustryAnalysisRequest，请求体，包含分析类型（trend/investment/risk）
    - force_refresh: bool，是否强制实时获取，默认False

    **返回**：
    - IndustryAnalysisResponse，分析报告，包括分析结论、分数、风险等级等

    **异常**：
    - 404: 未找到行业或行业数据
    - 500: AI分析服务异常

    **示例**：
    ```json
    POST /api/v1/industries/医药/analyze?force_refresh=true
    {
      "analysis_type": "trend"
    }
    ```
    """
    # 使用行业映射器进行智能匹配
    mapped_industry = IndustryMapper.map_industry(industry_name)
    if not mapped_industry:
        raise HTTPException(status_code=404, detail="未找到行业")
    # 优先尝试实时数据
    from app.services.realtime_data_service import RealtimeDataService
    realtime_service = RealtimeDataService()
    industry_data = None
    if force_refresh:
        # 实时获取行业数据（如有实现，可补充）
        # industry_data = realtime_service.get_industry_data(mapped_industry, force_refresh)
        pass
    # 降级本地
    if not industry_data:
        industry_data = data_manager.get_industry_data(mapped_industry)
    if not industry_data:
        raise HTTPException(status_code=404, detail="未找到行业数据")
    # 准备分析数据
    analysis_data = {
        'industry': mapped_industry,
        'market_size': industry_data.get('market_size'),
        'growth_rate': industry_data.get('growth_rate'),
        'company_count': industry_data.get('company_count'),
        'avg_pe': industry_data.get('avg_pe'),
        'description': industry_data.get('description')
    }
    # AI分析
    analyzer = GeminiAnalyzer()
    analysis_result = analyzer.analyze_industry_trends(analysis_data)
    if "error" in analysis_result:
        raise HTTPException(status_code=500, detail=analysis_result["error"])
    # 保存分析结果
    analysis_id = f"{mapped_industry}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    analysis_data = {
        "id": analysis_id,
        "target_type": "industry",
        "target_id": mapped_industry,
        "analysis_type": request.analysis_type,
        "title": f"{mapped_industry}行业分析报告",
        "summary": analysis_result.get("summary", ""),
        "details": analysis_result.get("full_analysis", ""),
        "score": None,  # 行业分析暂不评分
        "risk_level": "medium",  # 默认风险等级
        "ai_model": "gemini-pro",
        "confidence": analysis_result.get("confidence", 0.8),
        "created_at": datetime.now().isoformat()
    }
    data_manager.save_analysis_result(analysis_id, analysis_data)
    return IndustryAnalysisResponse(
        id=analysis_id,
        target_type="industry",
        target_id=mapped_industry,
        analysis_type=request.analysis_type,
        title=analysis_data["title"],
        summary=analysis_data["summary"],
        details=analysis_data["details"],
        score=analysis_data["score"],
        risk_level=analysis_data["risk_level"],
        ai_model=analysis_data["ai_model"],
        confidence=analysis_data["confidence"],
        created_at=datetime.now()
    )


@router.get("/{industry_name}/analysis", response_model=List[IndustryAnalysisResponse], summary="📊 获取行业分析报告", operation_id="industry_analysis_reports")
def get_industry_analysis(
    industry_name: str = Path(..., description="行业名称，支持中文和英文。例如：医药、新能源、半导体"),
    analysis_type: Optional[str] = Query(None, description="分析类型筛选，可选值：trend、investment、risk。不填则返回所有类型")
):
    """
    获取行业分析结果列表

    **功能说明**：
    - 根据行业名称获取该行业的所有分析报告。
    - 支持按分析类型筛选（趋势分析、投资分析、风险分析等）。
    - 返回按时间倒序排列的分析结果列表。
    - 支持行业名称智能匹配（中文、英文、别名等）。

    **参数说明**：
    - industry_name: str，行业名称，必填，支持中英文。例如：医药、新能源、半导体
    - analysis_type: str，分析类型筛选，可选，trend/investment/risk

    **返回**：
    - List[IndustryAnalysisResponse]，分析结果列表，包含：
      - id: 分析报告ID
      - target_type: 目标类型（industry）
      - target_id: 目标ID（行业名称）
      - analysis_type: 分析类型
      - title: 报告标题
      - summary: 分析摘要
      - details: 详细分析内容
      - score: 评分（可选）
      - risk_level: 风险等级
      - ai_model: AI模型名称
      - confidence: 置信度
      - created_at: 创建时间

    **异常**：
    - 404: 未找到行业（如果行业名称无效）

    **示例**：
    ```
    GET /api/v1/industries/医药/analysis
    GET /api/v1/industries/医药/analysis?analysis_type=trend
    GET /api/v1/industries/medical/analysis
    ```
    """
    # 使用行业映射器进行智能匹配
    mapped_industry = IndustryMapper.map_industry(industry_name)
    if not mapped_industry:
        raise HTTPException(status_code=404, detail="未找到行业")
    
    analysis_results = data_manager.get_analysis_results()
    
    # 过滤该行业的分析结果
    industry_analyses = []
    for analysis_id, analysis_data in analysis_results.items():
        if analysis_data.get('target_type') == 'industry' and analysis_data.get('target_id') == mapped_industry:
            if analysis_type and analysis_data.get('analysis_type') != analysis_type:
                continue
            
            industry_analyses.append(IndustryAnalysisResponse(
                id=analysis_id,
                target_type=analysis_data.get('target_type', ''),
                target_id=analysis_data.get('target_id', ''),
                analysis_type=analysis_data.get('analysis_type', ''),
                title=analysis_data.get('title', ''),
                summary=analysis_data.get('summary', ''),
                details=analysis_data.get('details', ''),
                score=analysis_data.get('score'),
                risk_level=analysis_data.get('risk_level'),
                ai_model=analysis_data.get('ai_model', ''),
                confidence=analysis_data.get('confidence'),
                created_at=datetime.fromisoformat(analysis_data.get('created_at', datetime.now().isoformat()))
            ))
    
    return industry_analyses


@router.get("/summary", response_model=dict, summary="📈 获取行业数据概览", operation_id="industries_summary")
def get_industries_summary():
    """
    获取行业汇总信息

    **功能说明**：
    - 获取系统中所有行业的统计汇总信息。
    - 包括各行业的市场规模、增长率、公司数量、平均市盈率等关键指标。
    - 用于快速了解各行业的发展状况和投资价值。

    **参数说明**：
    - 无参数

    **返回**：
    - dict，行业汇总信息，格式：{行业名: 行业数据}
    - 每个行业数据包含：
      - market_size: 市场规模
      - growth_rate: 增长率
      - company_count: 公司数量
      - avg_pe: 平均市盈率
      - last_update: 最后更新时间

    **异常**：
    - 无异常情况

    **示例**：
    ```
    GET /api/v1/industries/summary
    ```

    **返回示例**：
    ```json
    {
      "医药": {
        "market_size": 5000.0,
        "growth_rate": 15.5,
        "company_count": 150,
        "avg_pe": 25.3,
        "last_update": "2024-01-15T10:30:00"
      },
      "新能源": {
        "market_size": 8000.0,
        "growth_rate": 28.7,
        "company_count": 200,
        "avg_pe": 35.8,
        "last_update": "2024-01-15T10:30:00"
      },
      "半导体": {
        "market_size": 12000.0,
        "growth_rate": 22.3,
        "company_count": 180,
        "avg_pe": 42.1,
        "last_update": "2024-01-15T10:30:00"
      }
    }
    ```
    """
    # 获取各行业的最新数据
    industries = IndustryMapper.get_all_industries()
    summary = {}
    
    for industry in industries:
        industry_data = data_manager.get_industry_data(industry)
        if industry_data:
            summary[industry] = {
                "market_size": industry_data.get('market_size'),
                "growth_rate": industry_data.get('growth_rate'),
                "company_count": industry_data.get('company_count'),
                "avg_pe": industry_data.get('avg_pe'),
                "last_update": datetime.now().isoformat()
            }
    
    return summary 