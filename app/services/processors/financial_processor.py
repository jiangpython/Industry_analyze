import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FinancialProcessor:
    """财务数据处理器"""
    
    def __init__(self):
        self.required_fields = [
            'revenue', 'net_profit', 'total_assets', 
            'total_liabilities', 'operating_cash_flow'
        ]
    
    def calculate_financial_ratios(self, data: Dict[str, Any]) -> Dict[str, float]:
        """计算财务比率"""
        ratios = {}
        
        try:
            # 净资产收益率 (ROE)
            if data.get('net_profit') and data.get('total_assets') and data.get('total_liabilities'):
                equity = data['total_assets'] - data['total_liabilities']
                if equity > 0:
                    ratios['roe'] = (data['net_profit'] / equity) * 100
            
            # 总资产收益率 (ROA)
            if data.get('net_profit') and data.get('total_assets'):
                if data['total_assets'] > 0:
                    ratios['roa'] = (data['net_profit'] / data['total_assets']) * 100
            
            # 资产负债率
            if data.get('total_liabilities') and data.get('total_assets'):
                if data['total_assets'] > 0:
                    ratios['debt_ratio'] = (data['total_liabilities'] / data['total_assets']) * 100
            
            # 流动比率 (简化计算)
            if data.get('total_assets') and data.get('total_liabilities'):
                current_assets = data['total_assets'] * 0.6  # 假设60%为流动资产
                current_liabilities = data['total_liabilities'] * 0.8  # 假设80%为流动负债
                if current_liabilities > 0:
                    ratios['current_ratio'] = current_assets / current_liabilities
            
        except Exception as e:
            logger.error(f"计算财务比率时出错: {e}")
        
        return ratios
    
    def calculate_growth_rates(self, historical_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """计算增长率"""
        growth_rates = {}
        
        if len(historical_data) < 2:
            return growth_rates
        
        try:
            # 按时间排序
            sorted_data = sorted(historical_data, key=lambda x: x.get('report_date', ''))
            
            current = sorted_data[-1]
            previous = sorted_data[-2]
            
            # 收入增长率
            if current.get('revenue') and previous.get('revenue'):
                if previous['revenue'] > 0:
                    growth_rates['revenue_growth'] = (
                        (current['revenue'] - previous['revenue']) / previous['revenue']
                    ) * 100
            
            # 净利润增长率
            if current.get('net_profit') and previous.get('net_profit'):
                if previous['net_profit'] > 0:
                    growth_rates['profit_growth'] = (
                        (current['net_profit'] - previous['net_profit']) / previous['net_profit']
                    ) * 100
            
            # 资产增长率
            if current.get('total_assets') and previous.get('total_assets'):
                if previous['total_assets'] > 0:
                    growth_rates['assets_growth'] = (
                        (current['total_assets'] - previous['total_assets']) / previous['total_assets']
                    ) * 100
                    
        except Exception as e:
            logger.error(f"计算增长率时出错: {e}")
        
        return growth_rates
    
    def analyze_financial_health(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """分析财务健康状况"""
        analysis = {
            'score': 0,
            'risk_level': 'unknown',
            'strengths': [],
            'weaknesses': [],
            'recommendations': []
        }
        
        try:
            score = 0
            
            # 盈利能力分析
            if data.get('roe'):
                if data['roe'] > 15:
                    score += 25
                    analysis['strengths'].append('优秀的净资产收益率')
                elif data['roe'] > 10:
                    score += 15
                    analysis['strengths'].append('良好的净资产收益率')
                elif data['roe'] < 5:
                    score -= 10
                    analysis['weaknesses'].append('净资产收益率偏低')
            
            # 偿债能力分析
            if data.get('debt_ratio'):
                if data['debt_ratio'] < 50:
                    score += 20
                    analysis['strengths'].append('合理的资产负债率')
                elif data['debt_ratio'] > 70:
                    score -= 15
                    analysis['weaknesses'].append('资产负债率过高')
            
            # 现金流分析
            if data.get('operating_cash_flow') and data.get('net_profit'):
                if data['operating_cash_flow'] > data['net_profit']:
                    score += 15
                    analysis['strengths'].append('经营现金流良好')
                else:
                    score -= 10
                    analysis['weaknesses'].append('经营现金流需要关注')
            
            # 增长性分析
            if data.get('revenue_growth'):
                if data['revenue_growth'] > 20:
                    score += 20
                    analysis['strengths'].append('收入增长强劲')
                elif data['revenue_growth'] < 0:
                    score -= 15
                    analysis['weaknesses'].append('收入出现负增长')
            
            analysis['score'] = max(0, min(100, score))
            
            # 确定风险等级
            if analysis['score'] >= 80:
                analysis['risk_level'] = 'low'
            elif analysis['score'] >= 60:
                analysis['risk_level'] = 'medium'
            else:
                analysis['risk_level'] = 'high'
            
            # 生成建议
            if analysis['score'] < 60:
                analysis['recommendations'].append('建议深入分析财务风险')
            if data.get('debt_ratio', 0) > 70:
                analysis['recommendations'].append('关注债务风险')
            if data.get('revenue_growth', 0) < 0:
                analysis['recommendations'].append('关注业务发展')
                
        except Exception as e:
            logger.error(f"分析财务健康时出错: {e}")
        
        return analysis
    
    def process_company_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理公司财务数据"""
        processed_data = raw_data.copy()
        
        # 计算财务比率
        ratios = self.calculate_financial_ratios(raw_data)
        processed_data.update(ratios)
        
        # 验证数据完整性
        missing_fields = [field for field in self.required_fields if not raw_data.get(field)]
        if missing_fields:
            logger.warning(f"缺少必要字段: {missing_fields}")
        
        return processed_data 