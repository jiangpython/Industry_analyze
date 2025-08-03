from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.database.models import Company, FinancialData, AnalysisResult
from app.services.processors.financial_processor import FinancialProcessor
from app.services.analyzers.gemini_analyzer import GeminiAnalyzer
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/companies", tags=["companies"])

# Pydantic模型
class CompanyBase(BaseModel):
    code: str
    name: str
    industry: str
    market: str = "A股"

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class FinancialDataBase(BaseModel):
    report_date: datetime
    data_type: str
    revenue: Optional[float] = None
    net_profit: Optional[float] = None
    total_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    operating_cash_flow: Optional[float] = None

class FinancialDataResponse(FinancialDataBase):
    id: int
    company_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AnalysisRequest(BaseModel):
    analysis_type: str = "financial"  # financial, industry

class AnalysisResponse(BaseModel):
    id: int
    target_type: str
    target_id: int
    analysis_type: str
    title: str
    summary: str
    details: str
    score: Optional[float] = None
    risk_level: Optional[str] = None
    ai_model: str
    confidence: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[CompanyResponse])
def get_companies(
    industry: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取公司列表"""
    query = db.query(Company)
    
    if industry:
        query = query.filter(Company.industry == industry)
    
    companies = query.offset(skip).limit(limit).all()
    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """获取公司详情"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="公司不存在")
    return company


@router.get("/{company_id}/financial-data", response_model=List[FinancialDataResponse])
def get_company_financial_data(
    company_id: int,
    data_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """获取公司财务数据"""
    query = db.query(FinancialData).filter(FinancialData.company_id == company_id)
    
    if data_type:
        query = query.filter(FinancialData.data_type == data_type)
    if start_date:
        query = query.filter(FinancialData.report_date >= start_date)
    if end_date:
        query = query.filter(FinancialData.report_date <= end_date)
    
    financial_data = query.order_by(FinancialData.report_date.desc()).all()
    return financial_data


@router.post("/{company_id}/analyze", response_model=AnalysisResponse)
def analyze_company(
    company_id: int,
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """分析公司财务状况"""
    # 获取公司信息
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="公司不存在")
    
    # 获取最新财务数据
    latest_financial = db.query(FinancialData).filter(
        FinancialData.company_id == company_id
    ).order_by(FinancialData.report_date.desc()).first()
    
    if not latest_financial:
        raise HTTPException(status_code=404, detail="未找到财务数据")
    
    # 处理财务数据
    processor = FinancialProcessor()
    processed_data = processor.process_company_data({
        'name': company.name,
        'code': company.code,
        'industry': company.industry,
        'revenue': latest_financial.revenue,
        'net_profit': latest_financial.net_profit,
        'total_assets': latest_financial.total_assets,
        'total_liabilities': latest_financial.total_liabilities,
        'operating_cash_flow': latest_financial.operating_cash_flow,
        'roe': latest_financial.roe,
        'roa': latest_financial.roa,
        'debt_ratio': latest_financial.debt_ratio,
        'current_ratio': latest_financial.current_ratio,
    })
    
    # AI分析
    analyzer = GeminiAnalyzer()
    analysis_result = analyzer.analyze_company_financials(processed_data)
    
    if "error" in analysis_result:
        raise HTTPException(status_code=500, detail=analysis_result["error"])
    
    # 保存分析结果
    analysis = AnalysisResult(
        target_type="company",
        target_id=company_id,
        analysis_type=request.analysis_type,
        title=f"{company.name}财务分析报告",
        summary=analysis_result.get("summary", ""),
        details=analysis_result.get("full_analysis", ""),
        score=processed_data.get("score", 0),
        risk_level=processed_data.get("risk_level", "unknown"),
        ai_model="gemini-pro",
        confidence=analysis_result.get("confidence", 0.8)
    )
    
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return analysis


@router.get("/{company_id}/analysis", response_model=List[AnalysisResponse])
def get_company_analysis(
    company_id: int,
    analysis_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取公司分析结果"""
    query = db.query(AnalysisResult).filter(
        AnalysisResult.target_type == "company",
        AnalysisResult.target_id == company_id
    )
    
    if analysis_type:
        query = query.filter(AnalysisResult.analysis_type == analysis_type)
    
    analyses = query.order_by(AnalysisResult.created_at.desc()).all()
    return analyses 