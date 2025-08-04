#!/usr/bin/env python3
"""
Yahoo Finance数据处理器
处理从Yahoo Finance获取的原始数据
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class YahooDataProcessor:
    """Yahoo Finance数据处理器"""
    
    def __init__(self):
        self.logger = logger
    
    def process_company_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理公司基本信息
        
        Args:
            data: Yahoo Finance原始数据
            
        Returns:
            处理后的公司数据
        """
        try:
            if "error" in data:
                return {"error": data["error"]}
            
            # 提取基本信息
            info = data.get("info", {})
            
            company_data = {
                "code": info.get("symbol", ""),
                "name": info.get("longName", info.get("shortName", "")),
                "industry": info.get("industry", ""),
                "sector": info.get("sector", ""),
                "market": "美股",  # Yahoo Finance主要是美股数据
                "exchange": info.get("exchange", ""),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "pb_ratio": info.get("priceToBook"),
                "dividend_yield": info.get("dividendYield"),
                "description": info.get("longBusinessSummary", ""),
                "website": info.get("website", ""),
                "country": info.get("country", ""),
                "currency": info.get("currency", ""),
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
            data: Yahoo Finance原始数据
            
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
                            "total_assets": balance_sheet.get("Total Assets", {}).get(date),
                            "total_liabilities": balance_sheet.get("Total Liabilities", {}).get(date),
                            "total_equity": balance_sheet.get("Total Equity", {}).get(date),
                            "cash": balance_sheet.get("Cash", {}).get(date),
                            "debt": balance_sheet.get("Total Debt", {}).get(date),
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
                            "revenue": income_statement.get("Total Revenue", {}).get(date),
                            "net_profit": income_statement.get("Net Income", {}).get(date),
                            "gross_profit": income_statement.get("Gross Profit", {}).get(date),
                            "operating_income": income_statement.get("Operating Income", {}).get(date),
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
                            "operating_cash_flow": cash_flow.get("Operating Cash Flow", {}).get(date),
                            "investing_cash_flow": cash_flow.get("Investing Cash Flow", {}).get(date),
                            "financing_cash_flow": cash_flow.get("Financing Cash Flow", {}).get(date),
                            "free_cash_flow": cash_flow.get("Free Cash Flow", {}).get(date),
                            "created_at": datetime.now().isoformat()
                        }
                        financial_data_list.append(financial_data)
            
            return financial_data_list
            
        except Exception as e:
            self.logger.error(f"处理财务数据失败: {str(e)}")
            return [{"error": f"处理财务数据失败: {str(e)}"}]
    
    def extract_industry_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取行业数据
        
        Args:
            data: Yahoo Finance原始数据
            
        Returns:
            处理后的行业数据
        """
        try:
            if "error" in data:
                return {"error": data["error"]}
            
            info = data.get("info", {})
            
            industry_data = {
                "industry": info.get("industry", ""),
                "sector": info.get("sector", ""),
                "market_size": info.get("marketCap"),  # 市值作为行业规模参考
                "company_count": 1,  # 单个公司数据，无法获取行业公司总数
                "avg_pe": info.get("trailingPE"),
                "description": f"{info.get('industry', '')}行业数据",
                "data_type": "company_extracted",
                "data_date": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            return industry_data
            
        except Exception as e:
            self.logger.error(f"提取行业数据失败: {str(e)}")
            return {"error": f"提取行业数据失败: {str(e)}"}
    
    def process_market_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理市场数据
        
        Args:
            data: Yahoo Finance原始数据
            
        Returns:
            处理后的市场数据
        """
        try:
            if "error" in data:
                return {"error": data["error"]}
            
            # 这里可以根据实际需求处理市场数据
            # 目前返回原始数据
            return {
                "market_data": data,
                "processed_at": datetime.now().isoformat()
            }
            
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
            required_fields = ["info"]
            for field in required_fields:
                if field not in data:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"数据验证失败: {str(e)}")
            return False 