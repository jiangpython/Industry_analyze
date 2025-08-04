#!/usr/bin/env python3
"""
简化版公司API端点
使用本地文件存储
"""

from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from app.utils.data_manager import data_manager
from app.services.analyzers.gemini_analyzer import GeminiAnalyzer
from app.services.realtime_data_service import RealtimeDataService
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/companies", tags=["公司管理"])

# Pydantic模型
class CompanyBase(BaseModel):
    code: str
    name: str
    industry: str
    market: str = "A股"

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class FinancialDataBase(BaseModel):
    report_date: datetime
    data_type: str
    revenue: Optional[float] = None
    net_profit: Optional[float] = None
    total_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    operating_cash_flow: Optional[float] = None

class FinancialDataResponse(FinancialDataBase):
    created_at: Optional[datetime] = None

class AnalysisRequest(BaseModel):
    analysis_type: str = "financial"  # financial, industry

class AnalysisResponse(BaseModel):
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


@router.get("/", response_model=List[CompanyResponse], summary="📋 获取公司列表", operation_id="companies_list")
def get_companies(
    industry: Optional[str] = Query(None, description="行业筛选，支持中文。例如：医药、新能源、半导体、金融、房地产"),
    skip: int = Query(0, description="跳过记录数，用于分页。默认：0"),
    limit: int = Query(100, description="返回记录数限制，最大1000。默认：100"),
    force_refresh: bool = Query(False, description="强制刷新数据，忽略缓存。默认False，建议仅在需要最新数据时使用")
):
    """
    获取公司列表
    
    **输入参数说明：**
    - **industry**: 行业筛选（可选）
      - 支持中文行业名称
      - 示例：医药、新能源、半导体、金融、房地产
      - 不填则返回所有公司
    
    - **skip**: 跳过记录数（可选）
      - 用于分页功能
      - 默认值：0
      - 示例：skip=10 跳过前10条记录
    
    - **limit**: 返回记录数限制（可选）
      - 默认值：100
      - 最大值：1000
      - 示例：limit=50 返回50条记录
    
    - **force_refresh**: 强制刷新（可选）
      - 默认值：False
      - 说明：True=强制从网络获取最新数据，False=优先使用缓存
    
    **返回数据：**
    - 公司基本信息（代码、名称、行业、市场）
    - 公司描述信息
    - 分页信息
    
    **使用示例：**
    ```
    # 获取所有公司（前100条）
    GET /api/v1/companies/
    
    # 获取医药行业公司
    GET /api/v1/companies/?industry=医药
    
    # 分页获取新能源公司
    GET /api/v1/companies/?industry=新能源&skip=0&limit=50
    
    # 获取下一页数据
    GET /api/v1/companies/?industry=新能源&skip=50&limit=50
    
    # 强制刷新获取最新数据
    GET /api/v1/companies/?industry=医药&force_refresh=true
    ```
    """
    realtime_service = RealtimeDataService()
    
    try:
        if industry:
            # 如果指定了行业，使用实时数据服务获取该行业的公司
            companies_data = realtime_service.get_companies_by_industry_realtime(industry, force_refresh)
            
            # 转换为CompanyResponse格式
            company_list = []
            for company_data in companies_data:
                company_response = CompanyResponse(
                    code=company_data.get('code', ''),
                    name=company_data.get('name', ''),
                    industry=company_data.get('industry', industry),
                    market=company_data.get('market', 'A股'),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                company_list.append(company_response)
        else:
            # 如果没有指定行业，从本地缓存获取所有公司
            companies = data_manager.get_all_companies()
            
            # 转换为列表格式
            company_list = []
            for company_id, company_data in companies.items():
                company_response = CompanyResponse(
                    code=company_id,
                    name=company_data.get('name', ''),
                    industry=company_data.get('industry', ''),
                    market=company_data.get('market', 'A股'),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                company_list.append(company_response)
        
        # 分页
        return company_list[skip:skip + limit]
        
    except Exception as e:
        # 如果实时获取失败，降级到本地数据
        companies = data_manager.get_all_companies()
        
        # 转换为列表格式
        company_list = []
        for company_id, company_data in companies.items():
            if industry and company_data.get('industry') != industry:
                continue
            
            company_response = CompanyResponse(
                code=company_id,
                name=company_data.get('name', ''),
                industry=company_data.get('industry', ''),
                market=company_data.get('market', 'A股'),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            company_list.append(company_response)
        
        # 分页
        return company_list[skip:skip + limit]


@router.get("/{company_code}", response_model=CompanyResponse, summary="🏢 获取公司详细信息", operation_id="company_details")
def get_company(
    company_code: str = Path(..., description="公司代码，6位数字。例如：000001（平安银行）、000002（万科A）、300750（宁德时代）"),
    force_refresh: bool = Query(False, description="强制刷新数据，忽略缓存。默认False，建议仅在需要最新数据时使用")
):
    """
    获取公司详情
    
    **输入参数说明：**
    - **company_code**: 公司代码（必填）
      - 格式：6位数字代码
      - 示例：000001、000002、300750
      - 支持A股所有股票代码
    
    - **force_refresh**: 强制刷新（可选）
      - 默认值：False
      - 说明：True=强制从网络获取最新数据，False=优先使用缓存
    
    **返回数据：**
    - 公司基本信息（代码、名称、行业、市场）
    - 公司详细描述
    - 公司状态信息
    
    **使用示例：**
    ```
    GET /api/v1/companies/000001
    GET /api/v1/companies/300750
    GET /api/v1/companies/000001?force_refresh=true
    ```
    """
    realtime_service = RealtimeDataService()
    
    try:
        # 首先尝试从实时数据服务获取
        stock_data = realtime_service.get_stock_realtime_data(company_code, force_refresh)
        
        if stock_data and "error" not in stock_data:
            # 从实时数据构建公司信息
            return CompanyResponse(
                code=company_code,
                name=stock_data.get('name', ''),
                industry=stock_data.get('industry', ''),
                market=stock_data.get('market', 'A股'),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        else:
            # 如果实时获取失败，尝试从本地缓存获取
            company_data = data_manager.get_company(company_code)
            if not company_data:
                raise HTTPException(status_code=404, detail="公司不存在")
            
            return CompanyResponse(
                code=company_code,
                name=company_data.get('name', ''),
                industry=company_data.get('industry', ''),
                market=company_data.get('market', 'A股'),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
    except Exception as e:
        # 如果实时获取失败，降级到本地数据
        company_data = data_manager.get_company(company_code)
        if not company_data:
            raise HTTPException(status_code=404, detail="公司不存在")
        
        return CompanyResponse(
            code=company_code,
            name=company_data.get('name', ''),
            industry=company_data.get('industry', ''),
            market=company_data.get('market', 'A股'),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )


@router.get("/{company_code}/financial-data", response_model=List[FinancialDataResponse], summary="💰 获取公司财务数据", operation_id="company_financial_data")
def get_company_financial_data(
    company_code: str = Path(..., description="公司代码，6位数字。例如：000001"),
    data_type: Optional[str] = Query(None, description="财务数据类型筛选，可选值：annual、quarterly。不填则返回所有类型"),
    start_date: Optional[str] = Query(None, description="起始日期，格式YYYY-MM-DD。例如：2023-01-01"),
    end_date: Optional[str] = Query(None, description="结束日期，格式YYYY-MM-DD。例如：2023-12-31"),
    force_refresh: bool = Query(False, description="强制刷新，优先获取最新数据。默认False，优先本地缓存")
):
    """
    获取公司财务数据

    **功能说明**：
    - 根据公司代码获取该公司的财务数据。
    - 支持按数据类型、时间范围筛选。
    - 支持force_refresh参数，优先尝试实时数据，失败降级本地。
    - 返回营业收入、净利润、总资产、总负债、经营现金流等关键财务指标。

    **参数说明**：
    - company_code: str，公司代码，必填，6位数字。例如：000001
    - data_type: str，财务数据类型筛选，可选，annual/quarterly
    - start_date: datetime，起始日期，可选，格式YYYY-MM-DD
    - end_date: datetime，结束日期，可选，格式YYYY-MM-DD
    - force_refresh: bool，是否强制实时获取，默认False

    **返回**：
    - List[FinancialDataResponse]，财务数据列表，包含：
      - report_date: 报告期
      - data_type: 数据类型（年报/季报）
      - revenue: 营业收入
      - net_profit: 净利润
      - total_assets: 总资产
      - total_liabilities: 总负债
      - operating_cash_flow: 经营现金流
      - created_at: 创建时间

    **异常**：
    - 404: 未找到公司或财务数据

    **示例**：
    ```
    GET /api/v1/companies/000001/financial-data
    GET /api/v1/companies/000001/financial-data?data_type=annual
    GET /api/v1/companies/000001/financial-data?start_date=2023-01-01&end_date=2023-12-31
    GET /api/v1/companies/000001/financial-data?force_refresh=true
    ```
    """
    # 优先尝试实时数据
    from app.services.realtime_data_service import RealtimeDataService
    realtime_service = RealtimeDataService()
    financial_records = None
    
    # 1. 优先尝试实时数据采集
    if force_refresh:
        financial_records = realtime_service.get_financial_data(company_code, force_refresh)
    
    # 2. 如果本地没有数据，自动启动采集
    if not financial_records:
        financial_records = data_manager.get_financial_data(company_code)
        
        # 如果本地也没有数据，尝试实时采集
        if not financial_records:
            logger.info(f"本地无数据，启动实时采集: {company_code}")
            financial_records = realtime_service.get_financial_data(company_code, force_refresh=True)
    
    # 3. 如果仍然没有数据，返回错误
    if not financial_records:
        raise HTTPException(status_code=404, detail=f"未找到公司 {company_code} 的财务数据，请检查股票代码是否正确")
    
    # 过滤数据
    filtered_records = []
    for record in financial_records:
        if data_type and record.get('data_type') != data_type:
            continue
        
        # 修复日期解析逻辑
        record_date_str = record.get('report_date', '')
        try:
            # 处理AKShare返回的日期格式（如：20250331）
            if len(record_date_str) == 8 and record_date_str.isdigit():
                # 格式：YYYYMMDD
                record_date = datetime.strptime(record_date_str, '%Y%m%d')
            else:
                # 尝试其他格式
                record_date = datetime.fromisoformat(record_date_str.replace('Z', '+00:00'))
        except Exception as e:
            logger.warning(f"日期解析失败: {record_date_str}, 错误: {e}")
            # 如果日期解析失败，跳过这条记录
            continue
        
        # 日期过滤
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                if record_date < start_dt:
                    continue
            except Exception as e:
                logger.warning(f"起始日期解析失败: {start_date}, 错误: {e}")
        
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                if record_date > end_dt:
                    continue
            except Exception as e:
                logger.warning(f"结束日期解析失败: {end_date}, 错误: {e}")
        
        filtered_records.append(FinancialDataResponse(
            report_date=record_date,
            data_type=record.get('data_type', ''),
            revenue=record.get('revenue'),
            net_profit=record.get('net_profit'),
            total_assets=record.get('total_assets'),
            total_liabilities=record.get('total_liabilities'),
            operating_cash_flow=record.get('operating_cash_flow'),
            created_at=datetime.now()
        ))
    
    return filtered_records


@router.post("/{company_code}/analyze", response_model=AnalysisResponse, summary="🤖 AI智能分析公司", operation_id="company_ai_analysis")
def analyze_company(
    company_code: str = Path(..., description="公司代码，6位数字。例如：000001"),
    request: AnalysisRequest = ...,
    force_refresh: bool = Query(False, description="强制刷新，优先获取最新数据。默认False，优先本地缓存")
):
    """
    分析公司财务状况/趋势（AI分析报告）

    **功能说明**：
    - 根据公司代码和分析类型，生成AI分析报告。
    - 支持财务分析、趋势分析等。
    - 支持force_refresh参数，优先尝试实时数据，失败降级本地。

    **参数说明**：
    - company_code: str，公司代码，必填，6位数字。例如：000001
    - request: AnalysisRequest，请求体，包含分析类型（financial/industry）
    - force_refresh: bool，是否强制实时获取，默认False

    **返回**：
    - AnalysisResponse，分析报告，包括分析结论、分数、风险等级等

    **异常**：
    - 404: 未找到公司或财务数据
    - 500: AI分析服务异常

    **示例**：
    ```json
    POST /api/v1/companies/000001/analyze?force_refresh=true
    {
      "analysis_type": "financial"
    }
    ```
    """
    # 优先尝试实时数据
    from app.services.realtime_data_service import RealtimeDataService
    realtime_service = RealtimeDataService()
    company_data = None
    financial_records = None
    if force_refresh:
        # 实时获取公司基本信息
        stock_data = realtime_service.get_stock_realtime_data(company_code, force_refresh)
        if stock_data and "error" not in stock_data:
            company_data = {
                "code": company_code,
                "name": stock_data.get("name", ""),
                "industry": stock_data.get("industry", ""),
                "market": stock_data.get("market", "A股")
            }
        # 实时获取财务数据（如有实现，可补充）
        # financial_records = realtime_service.get_financial_data(company_code, force_refresh)
    # 降级本地
    if not company_data:
        company_data = data_manager.get_company(company_code)
    if not company_data:
        raise HTTPException(status_code=404, detail="公司不存在")
    if not financial_records:
        financial_records = data_manager.get_financial_data(company_code)
    if not financial_records:
        raise HTTPException(status_code=404, detail="未找到财务数据")
    # 准备分析数据
    latest_financial = financial_records[0] if financial_records else {}
    analysis_data = {
        'company_code': company_code,
        'company_name': company_data.get('name', ''),
        'industry': company_data.get('industry', ''),
        'financial_data': latest_financial
    }
    # AI分析
    analyzer = GeminiAnalyzer()
    if request.analysis_type == "financial":
        analysis_result = analyzer.analyze_financial_data(analysis_data)
    else:
        analysis_result = analyzer.analyze_company_trends(analysis_data)
    if "error" in analysis_result:
        raise HTTPException(status_code=500, detail=analysis_result["error"])
    # 保存分析结果
    analysis_id = f"{company_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    analysis_data = {
        "id": analysis_id,
        "target_type": "company",
        "target_id": company_code,
        "analysis_type": request.analysis_type,
        "title": f"{company_data.get('name', '')}分析报告",
        "summary": analysis_result.get("summary", ""),
        "details": analysis_result.get("full_analysis", ""),
        "score": analysis_result.get("score"),
        "risk_level": analysis_result.get("risk_level", "medium"),
        "ai_model": "gemini-pro",
        "confidence": analysis_result.get("confidence", 0.8),
        "created_at": datetime.now().isoformat()
    }
    data_manager.save_analysis_result(analysis_id, analysis_data)
    return AnalysisResponse(
        id=analysis_id,
        target_type="company",
        target_id=company_code,
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


@router.get("/{company_code}/analysis", response_model=List[AnalysisResponse], summary="📊 获取公司分析报告", operation_id="company_analysis_reports")
def get_company_analysis(
    company_code: str = Path(..., description="公司代码，6位数字。例如：000001"),
    analysis_type: Optional[str] = Query(None, description="分析类型筛选，可选值：financial、industry。不填则返回所有类型")
):
    """
    获取公司分析结果列表

    **功能说明**：
    - 根据公司代码获取该公司的所有分析报告。
    - 支持按分析类型筛选（财务分析、行业分析等）。
    - 返回按时间倒序排列的分析结果列表。

    **参数说明**：
    - company_code: str，公司代码，必填，6位数字。例如：000001
    - analysis_type: str，分析类型筛选，可选，financial/industry

    **返回**：
    - List[AnalysisResponse]，分析结果列表，包含：
      - id: 分析报告ID
      - target_type: 目标类型（company）
      - target_id: 目标ID（公司代码）
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
    - 404: 公司不存在（如果公司代码无效）

    **示例**：
    ```
    GET /api/v1/companies/000001/analysis
    GET /api/v1/companies/000001/analysis?analysis_type=financial
    ```
    """
    analysis_results = data_manager.get_analysis_results()
    
    # 过滤该公司的分析结果
    company_analyses = []
    for analysis_id, analysis_data in analysis_results.items():
        if analysis_data.get('target_type') == 'company' and analysis_data.get('target_id') == company_code:
            if analysis_type and analysis_data.get('analysis_type') != analysis_type:
                continue
            
            company_analyses.append(AnalysisResponse(
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
    
    return company_analyses


@router.get("/summary", response_model=dict, summary="📈 获取公司数据概览", operation_id="companies_summary")
def get_companies_summary():
    """
    获取公司汇总信息

    **功能说明**：
    - 获取系统中所有公司的统计汇总信息。
    - 包括公司总数、行业分布、市场分布等统计指标。
    - 用于快速了解系统数据概况和分布情况。

    **参数说明**：
    - 无参数

    **返回**：
    - dict，汇总信息，包含：
      - total_companies: 公司总数
      - industries: 行业分布统计，格式：{行业名: 公司数量}
      - market_distribution: 市场分布统计，格式：{市场名: 公司数量}

    **异常**：
    - 无异常情况

    **示例**：
    ```
    GET /api/v1/companies/summary
    ```

    **返回示例**：
    ```json
    {
      "total_companies": 8,
      "industries": {
        "医药": 2,
        "新能源": 2,
        "半导体": 1,
        "金融": 1,
        "房地产": 1,
        "科技": 1
      },
      "market_distribution": {
        "A股": 4,
        "美股": 4
      }
    }
    ```
    """
    companies = data_manager.get_all_companies()
    
    summary = {
        "total_companies": len(companies),
        "industries": {},
        "market_distribution": {}
    }
    
    for company_id, company_data in companies.items():
        industry = company_data.get('industry', '未知')
        market = company_data.get('market', '未知')
        
        # 统计行业分布
        if industry not in summary["industries"]:
            summary["industries"][industry] = 0
        summary["industries"][industry] += 1
        
        # 统计市场分布
        if market not in summary["market_distribution"]:
            summary["market_distribution"][market] = 0
        summary["market_distribution"][market] += 1
    
    return summary 