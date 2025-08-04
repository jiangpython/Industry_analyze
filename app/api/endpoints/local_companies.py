from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
from app.utils.local_storage import local_storage
from app.services.processors.financial_processor import FinancialProcessor
from app.services.analyzers.gemini_analyzer import GeminiAnalyzer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/local/companies", tags=["本地公司"])


@router.get("/")
def get_companies(industry: Optional[str] = None) -> Dict[str, Any]:
    """获取公司列表"""
    try:
        companies = local_storage.get_all_companies()
        
        if industry:
            # 过滤指定行业
            filtered_companies = {}
            for company_id, company_data in companies.items():
                if company_data.get('industry') == industry:
                    filtered_companies[company_id] = company_data
            companies = filtered_companies
        
        return {
            "total": len(companies),
            "companies": companies
        }
    except Exception as e:
        logger.error(f"获取公司列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取公司列表失败")


@router.get("/{company_id}")
def get_company(company_id: str) -> Dict[str, Any]:
    """获取公司详情"""
    try:
        company = local_storage.get_company(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="公司不存在")
        
        # 获取最新财务数据
        financial_data = local_storage.get_financial_data(company_id)
        if financial_data:
            company['latest_financial'] = financial_data[-1]  # 最新的财务数据
        
        return company
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取公司详情失败: {e}")
        raise HTTPException(status_code=500, detail="获取公司详情失败")


@router.get("/{company_id}/financial")
def get_company_financial(company_id: str) -> Dict[str, Any]:
    """获取公司财务数据"""
    try:
        financial_data = local_storage.get_financial_data(company_id)
        return {
            "company_id": company_id,
            "total_records": len(financial_data),
            "financial_data": financial_data
        }
    except Exception as e:
        logger.error(f"获取财务数据失败: {e}")
        raise HTTPException(status_code=500, detail="获取财务数据失败")


@router.post("/{company_id}/analyze")
def analyze_company(company_id: str) -> Dict[str, Any]:
    """分析公司财务状况"""
    try:
        # 获取公司信息
        company = local_storage.get_company(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="公司不存在")
        
        # 获取最新财务数据
        financial_data = local_storage.get_financial_data(company_id)
        if not financial_data:
            raise HTTPException(status_code=404, detail="未找到财务数据")
        
        latest_financial = financial_data[-1]
        
        # 处理财务数据
        processor = FinancialProcessor()
        processed_data = processor.process_company_data({
            'name': company.get('name'),
            'code': company.get('code'),
            'industry': company.get('industry'),
            'revenue': latest_financial.get('revenue'),
            'net_profit': latest_financial.get('net_profit'),
            'total_assets': latest_financial.get('total_assets'),
            'total_liabilities': latest_financial.get('total_liabilities'),
            'operating_cash_flow': latest_financial.get('operating_cash_flow'),
        })
        
        # AI分析
        analyzer = GeminiAnalyzer()
        analysis_result = analyzer.analyze_company_financials(processed_data)
        
        if "error" in analysis_result:
            raise HTTPException(status_code=500, detail=analysis_result["error"])
        
        # 保存分析结果
        analysis_data = {
            "target_type": "company",
            "target_id": company_id,
            "analysis_type": "financial",
            "title": f"{company.get('name')}财务分析报告",
            "summary": analysis_result.get("summary", ""),
            "details": analysis_result.get("full_analysis", ""),
            "score": processed_data.get("score", 0),
            "risk_level": processed_data.get("risk_level", "unknown"),
            "ai_model": "gemini-pro",
            "confidence": analysis_result.get("confidence", 0.8)
        }
        
        local_storage.save_analysis_result(analysis_data)
        
        return {
            "company_id": company_id,
            "analysis": analysis_data,
            "processed_data": processed_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"分析公司失败: {e}")
        raise HTTPException(status_code=500, detail="分析公司失败")


@router.get("/{company_id}/analysis")
def get_company_analysis(company_id: str) -> Dict[str, Any]:
    """获取公司分析结果"""
    try:
        analysis_results = local_storage.get_analysis_results("company", company_id)
        return {
            "company_id": company_id,
            "total_analyses": len(analysis_results),
            "analyses": analysis_results
        }
    except Exception as e:
        logger.error(f"获取分析结果失败: {e}")
        raise HTTPException(status_code=500, detail="获取分析结果失败")


@router.post("/")
def add_company(company_data: Dict[str, Any]) -> Dict[str, Any]:
    """添加公司"""
    try:
        # 验证必要字段
        required_fields = ['code', 'name', 'industry']
        for field in required_fields:
            if not company_data.get(field):
                raise HTTPException(status_code=400, detail=f"缺少必要字段: {field}")
        
        # 添加时间戳
        company_data['created_at'] = datetime.now().isoformat()
        company_data['updated_at'] = datetime.now().isoformat()
        
        # 保存公司数据
        success = local_storage.save_company(company_data)
        if not success:
            raise HTTPException(status_code=500, detail="保存公司数据失败")
        
        return {
            "message": "公司添加成功",
            "company": company_data
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加公司失败: {e}")
        raise HTTPException(status_code=500, detail="添加公司失败")


@router.post("/{company_id}/financial")
def add_financial_data(company_id: str, financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """添加财务数据"""
    try:
        # 验证公司是否存在
        company = local_storage.get_company(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="公司不存在")
        
        # 添加时间戳
        financial_data['company_id'] = company_id
        financial_data['created_at'] = datetime.now().isoformat()
        
        # 保存财务数据
        success = local_storage.save_financial_data(company_id, financial_data)
        if not success:
            raise HTTPException(status_code=500, detail="保存财务数据失败")
        
        return {
            "message": "财务数据添加成功",
            "financial_data": financial_data
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加财务数据失败: {e}")
        raise HTTPException(status_code=500, detail="添加财务数据失败")


@router.get("/export/csv")
def export_companies_csv() -> Dict[str, Any]:
    """导出公司数据到CSV"""
    try:
        success = local_storage.export_to_csv()
        if success:
            return {
                "message": "数据导出成功",
                "files": [
                    local_storage.settings.COMPANIES_CSV,
                    local_storage.settings.FINANCIAL_DATA_CSV
                ]
            }
        else:
            raise HTTPException(status_code=500, detail="数据导出失败")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"导出数据失败: {e}")
        raise HTTPException(status_code=500, detail="导出数据失败") 