from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Company(Base):
    """公司信息表"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, comment="股票代码")
    name = Column(String(100), index=True, comment="公司名称")
    industry = Column(String(50), index=True, comment="所属行业")
    market = Column(String(20), comment="市场类型")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class FinancialData(Base):
    """财务数据表"""
    __tablename__ = "financial_data"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True, comment="公司ID")
    report_date = Column(DateTime, index=True, comment="报告期")
    data_type = Column(String(50), index=True, comment="数据类型")
    
    # 财务指标
    revenue = Column(Float, comment="营业收入")
    net_profit = Column(Float, comment="净利润")
    total_assets = Column(Float, comment="总资产")
    total_liabilities = Column(Float, comment="总负债")
    operating_cash_flow = Column(Float, comment="经营现金流")
    
    # 财务比率
    roe = Column(Float, comment="净资产收益率")
    roa = Column(Float, comment="总资产收益率")
    debt_ratio = Column(Float, comment="资产负债率")
    current_ratio = Column(Float, comment="流动比率")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class IndustryData(Base):
    """行业数据表"""
    __tablename__ = "industry_data"
    
    id = Column(Integer, primary_key=True, index=True)
    industry = Column(String(50), index=True, comment="行业名称")
    data_date = Column(DateTime, index=True, comment="数据日期")
    data_type = Column(String(50), index=True, comment="数据类型")
    
    # 行业指标
    market_size = Column(Float, comment="市场规模")
    growth_rate = Column(Float, comment="增长率")
    company_count = Column(Integer, comment="公司数量")
    avg_pe = Column(Float, comment="平均市盈率")
    
    description = Column(Text, comment="描述")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AnalysisResult(Base):
    """分析结果表"""
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    target_type = Column(String(50), index=True, comment="分析目标类型")
    target_id = Column(Integer, index=True, comment="分析目标ID")
    analysis_type = Column(String(50), index=True, comment="分析类型")
    
    # 分析结果
    title = Column(String(200), comment="分析标题")
    summary = Column(Text, comment="分析摘要")
    details = Column(Text, comment="详细分析")
    score = Column(Float, comment="评分")
    risk_level = Column(String(20), comment="风险等级")
    
    # AI分析相关
    ai_model = Column(String(50), comment="AI模型")
    confidence = Column(Float, comment="置信度")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TaskLog(Base):
    """任务日志表"""
    __tablename__ = "task_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(100), index=True, comment="任务名称")
    status = Column(String(20), index=True, comment="任务状态")
    start_time = Column(DateTime, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    
    # 任务详情
    total_items = Column(Integer, comment="总项目数")
    success_items = Column(Integer, comment="成功项目数")
    error_items = Column(Integer, comment="错误项目数")
    
    error_message = Column(Text, comment="错误信息")
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 