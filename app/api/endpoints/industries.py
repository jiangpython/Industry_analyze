from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.database.models import IndustryData, AnalysisResult
from app.services.analyzers.gemini_analyzer import GeminiAnalyzer
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/industries", tags=["industries"])

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
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class IndustryAnalysisRequest(BaseModel):
    analysis_type: str = "trend"  # trend, investment, risk

class IndustryAnalysisResponse(BaseModel):
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


@router.get("/", response_model=List[str])
def get_industries(db: Session = Depends(get_db)):
    """获取所有行业列表"""
    industries = db.query(IndustryData.industry).distinct().all()
    return [industry[0] for industry in industries]


@router.get("/{industry_name}/data", response_model=List[IndustryDataResponse])
def get_industry_data(
    industry_name: str,
    data_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """获取行业数据"""
    query = db.query(IndustryData).filter(IndustryData.industry == industry_name)
    
    if data_type:
        query = query.filter(IndustryData.data_type == data_type)
    if start_date:
        query = query.filter(IndustryData.data_date >= start_date)
    if end_date:
        query = query.filter(IndustryData.data_date <= end_date)
    
    industry_data = query.order_by(IndustryData.data_date.desc()).all()
    return industry_data


@router.get("/{industry_name}/latest", response_model=IndustryDataResponse)
def get_latest_industry_data(industry_name: str, db: Session = Depends(get_db)):
    """获取行业最新数据"""
    latest_data = db.query(IndustryData).filter(
        IndustryData.industry == industry_name
    ).order_by(IndustryData.data_date.desc()).first()
    
    if not latest_data:
        raise HTTPException(status_code=404, detail="未找到行业数据")
    
    return latest_data


@router.post("/{industry_name}/analyze", response_model=IndustryAnalysisResponse)
def analyze_industry(
    industry_name: str,
    request: IndustryAnalysisRequest,
    db: Session = Depends(get_db)
):
    """分析行业趋势"""
    # 获取最新行业数据
    latest_data = db.query(IndustryData).filter(
        IndustryData.industry == industry_name
    ).order_by(IndustryData.data_date.desc()).first()
    
    if not latest_data:
        raise HTTPException(status_code=404, detail="未找到行业数据")
    
    # 准备分析数据
    analysis_data = {
        'industry': latest_data.industry,
        'market_size': latest_data.market_size,
        'growth_rate': latest_data.growth_rate,
        'company_count': latest_data.company_count,
        'avg_pe': latest_data.avg_pe,
        'description': latest_data.description
    }
    
    # AI分析
    analyzer = GeminiAnalyzer()
    analysis_result = analyzer.analyze_industry_trends(analysis_data)
    
    if "error" in analysis_result:
        raise HTTPException(status_code=500, detail=analysis_result["error"])
    
    # 保存分析结果
    analysis = AnalysisResult(
        target_type="industry",
        target_id=latest_data.id,
        analysis_type=request.analysis_type,
        title=f"{industry_name}行业分析报告",
        summary=analysis_result.get("summary", ""),
        details=analysis_result.get("full_analysis", ""),
        score=None,  # 行业分析暂不评分
        risk_level="medium",  # 默认风险等级
        ai_model="gemini-pro",
        confidence=analysis_result.get("confidence", 0.8)
    )
    
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return analysis


@router.get("/{industry_name}/analysis", response_model=List[IndustryAnalysisResponse])
def get_industry_analysis(
    industry_name: str,
    analysis_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取行业分析结果"""
    # 获取该行业的所有数据ID
    industry_data_ids = db.query(IndustryData.id).filter(
        IndustryData.industry == industry_name
    ).all()
    
    if not industry_data_ids:
        raise HTTPException(status_code=404, detail="未找到行业数据")
    
    data_ids = [data[0] for data in industry_data_ids]
    
    query = db.query(AnalysisResult).filter(
        AnalysisResult.target_type == "industry",
        AnalysisResult.target_id.in_(data_ids)
    )
    
    if analysis_type:
        query = query.filter(AnalysisResult.analysis_type == analysis_type)
    
    analyses = query.order_by(AnalysisResult.created_at.desc()).all()
    return analyses


@router.get("/summary", response_model=dict)
def get_industries_summary(db: Session = Depends(get_db)):
    """获取行业汇总信息"""
    # 获取各行业的最新数据
    industries = ["医药", "新能源", "半导体", "芯片"]
    summary = {}
    
    for industry in industries:
        latest_data = db.query(IndustryData).filter(
            IndustryData.industry == industry
        ).order_by(IndustryData.data_date.desc()).first()
        
        if latest_data:
            summary[industry] = {
                "market_size": latest_data.market_size,
                "growth_rate": latest_data.growth_rate,
                "company_count": latest_data.company_count,
                "avg_pe": latest_data.avg_pe,
                "last_update": latest_data.data_date
            }
    
    return summary 