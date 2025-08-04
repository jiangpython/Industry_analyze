#!/usr/bin/env python3
"""
AKShare数据处理器
处理从AKShare获取的原始数据
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AKShareDataProcessor:
    """AKShare数据处理器"""
    
    def __init__(self):
        self.logger = logger
    
    def process_stock_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理股票数据
        
        Args:
            data: AKShare原始数据
            
        Returns:
            处理后的股票数据
        """
        try:
            if "error" in data:
                return {"error": data["error"]}
            
            # 提取基本信息
            stock_data = {
                "code": data.get("code", ""),
                "name": data.get("name", ""),
                "industry": data.get("industry", ""),
                "market": "A股",
                "current_price": data.get("current_price"),
                "change_percent": data.get("change_percent"),
                "volume": data.get("volume"),
                "turnover": data.get("turnover"),
                "market_cap": data.get("market_cap"),
                "pe_ratio": data.get("pe_ratio"),
                "pb_ratio": data.get("pb_ratio"),
                "source": "akshare",
                "update_time": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            return stock_data
            
        except Exception as e:
            self.logger.error(f"处理股票数据失败: {str(e)}")
            return {"error": f"处理股票数据失败: {str(e)}"}
    
    def process_company_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理公司基本信息
        
        Args:
            data: AKShare原始数据
            
        Returns:
            处理后的公司数据
        """
        try:
            if "error" in data:
                return {"error": data["error"]}
            
            company_data = {
                "code": data.get("code", ""),
                "name": data.get("name", ""),
                "industry": data.get("industry", ""),
                "sector": data.get("sector", ""),
                "market": "A股",
                "exchange": "沪深交易所",
                "market_cap": data.get("market_cap"),
                "pe_ratio": data.get("pe_ratio"),
                "pb_ratio": data.get("pb_ratio"),
                "dividend_yield": data.get("dividend_yield"),
                "description": data.get("description", ""),
                "website": data.get("website", ""),
                "country": "中国",
                "currency": "CNY",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            return company_data
            
        except Exception as e:
            self.logger.error(f"处理公司数据失败: {str(e)}")
            return {"error": f"处理公司数据失败: {str(e)}"}
    
    def process_financial_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        处理财务数据
        
        Args:
            data: AKShare原始数据
            
        Returns:
            处理后的财务数据列表
        """
        try:
            if "error" in data:
                return [{"error": data["error"]}]
            
            financial_data_list = []
            
            # 处理财务报表数据
            financials = data.get("financials", {})
            
            # 处理资产负债表
            if "balance_sheet" in financials:
                balance_sheet = financials["balance_sheet"]
                if isinstance(balance_sheet, pd.DataFrame):
                    for date in balance_sheet.columns:
                        financial_data = {
                            "report_date": date.isoformat(),
                            "data_type": "balance_sheet",
                            "total_assets": balance_sheet.get("总资产", {}).get(date),
                            "total_liabilities": balance_sheet.get("总负债", {}).get(date),
                            "total_equity": balance_sheet.get("股东权益", {}).get(date),
                            "cash": balance_sheet.get("货币资金", {}).get(date),
                            "debt": balance_sheet.get("总负债", {}).get(date),
                            "created_at": datetime.now().isoformat()
                        }
                        financial_data_list.append(financial_data)
            
            # 处理利润表
            if "income_statement" in financials:
                income_statement = financials["income_statement"]
                if isinstance(income_statement, pd.DataFrame):
                    for date in income_statement.columns:
                        financial_data = {
                            "report_date": date.isoformat(),
                            "data_type": "income_statement",
                            "revenue": income_statement.get("营业收入", {}).get(date),
                            "net_profit": income_statement.get("净利润", {}).get(date),
                            "gross_profit": income_statement.get("营业利润", {}).get(date),
                            "operating_income": income_statement.get("营业利润", {}).get(date),
                            "created_at": datetime.now().isoformat()
                        }
                        financial_data_list.append(financial_data)
            
            # 处理现金流量表
            if "cash_flow" in financials:
                cash_flow = financials["cash_flow"]
                if isinstance(cash_flow, pd.DataFrame):
                    for date in cash_flow.columns:
                        financial_data = {
                            "report_date": date.isoformat(),
                            "data_type": "cash_flow",
                            "operating_cash_flow": cash_flow.get("经营活动现金流量净额", {}).get(date),
                            "investing_cash_flow": cash_flow.get("投资活动现金流量净额", {}).get(date),
                            "financing_cash_flow": cash_flow.get("筹资活动现金流量净额", {}).get(date),
                            "free_cash_flow": cash_flow.get("自由现金流量", {}).get(date),
                            "created_at": datetime.now().isoformat()
                        }
                        financial_data_list.append(financial_data)
            
            return financial_data_list
            
        except Exception as e:
            self.logger.error(f"处理财务数据失败: {str(e)}")
            return [{"error": f"处理财务数据失败: {str(e)}"}]
    
    def process_industry_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理行业数据
        
        Args:
            data: AKShare原始数据
            
        Returns:
            处理后的行业数据
        """
        try:
            if "error" in data:
                return {"error": data["error"]}
            
            industry_data = {
                "industry": data.get("industry", ""),
                "sector": data.get("sector", ""),
                "market_size": data.get("market_size"),
                "company_count": data.get("company_count"),
                "avg_pe": data.get("avg_pe"),
                "avg_pb": data.get("avg_pb"),
                "growth_rate": data.get("growth_rate"),
                "description": f"{data.get('industry', '')}行业数据",
                "data_type": "industry_analysis",
                "data_date": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            return industry_data
            
        except Exception as e:
            self.logger.error(f"处理行业数据失败: {str(e)}")
            return {"error": f"处理行业数据失败: {str(e)}"}
    
    def process_market_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理市场数据
        
        Args:
            data: AKShare原始数据
            
        Returns:
            处理后的市场数据
        """
        try:
            if "error" in data:
                return {"error": data["error"]}
            
            market_data = {
                "market": data.get("market", ""),
                "index_code": data.get("index_code", ""),
                "index_name": data.get("index_name", ""),
                "current_value": data.get("current_value"),
                "change_percent": data.get("change_percent"),
                "volume": data.get("volume"),
                "turnover": data.get("turnover"),
                "pe_ratio": data.get("pe_ratio"),
                "pb_ratio": data.get("pb_ratio"),
                "source": "akshare",
                "update_time": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            return market_data
            
        except Exception as e:
            self.logger.error(f"处理市场数据失败: {str(e)}")
            return {"error": f"处理市场数据失败: {str(e)}"}
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        验证数据有效性
        
        Args:
            data: 要验证的数据
            
        Returns:
            数据是否有效
        """
        try:
            if not data:
                return False
            
            if "error" in data:
                return False
            
            # 检查必要字段
            required_fields = ["code"]
            for field in required_fields:
                if field not in data:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"数据验证失败: {str(e)}")
            return False 