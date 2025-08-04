import google.generativeai as genai
from typing import Dict, Any, List
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiAnalyzer:
    """Gemini AI分析器"""
    
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            logger.warning("未配置Gemini API密钥")
            self.model = None
        else:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_company_financials(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析公司财务状况"""
        if not self.model:
            return {"error": "Gemini API未配置"}
        
        try:
            # 构建分析提示
            prompt = self._build_financial_analysis_prompt(company_data)
            
            # 调用Gemini API
            response = self.model.generate_content(prompt)
            
            # 解析响应
            analysis = self._parse_financial_analysis_response(response.text)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Gemini分析失败: {e}")
            return {"error": f"分析失败: {str(e)}"}
    
    def analyze_financial_data(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析财务数据（兼容companies_simple.py的调用）"""
        if not self.model:
            return {"error": "Gemini API未配置"}
        
        try:
            # 提取财务数据
            financial_data = analysis_data.get('financial_data', {})
            company_name = analysis_data.get('company_name', '未知')
            industry = analysis_data.get('industry', '未知')
            company_code = analysis_data.get('company_code', '未知')
            
            # 构建分析数据
            company_data = {
                'name': company_name,
                'code': company_code,
                'industry': industry,
                'revenue': financial_data.get('revenue', 0),
                'net_profit': financial_data.get('net_profit', 0),
                'total_assets': financial_data.get('total_assets', 0),
                'total_liabilities': financial_data.get('total_liabilities', 0),
                'operating_cash_flow': financial_data.get('operating_cash_flow', 0),
                'roe': financial_data.get('roe', 0),
                'roa': financial_data.get('roa', 0),
                'debt_ratio': financial_data.get('debt_ratio', 0),
                'current_ratio': financial_data.get('current_ratio', 0),
                'revenue_growth': financial_data.get('revenue_growth', 0),
                'profit_growth': financial_data.get('profit_growth', 0)
            }
            
            # 使用现有的财务分析方法
            return self.analyze_company_financials(company_data)
            
        except Exception as e:
            logger.error(f"财务数据分析失败: {e}")
            return {"error": f"分析失败: {str(e)}"}
    
    def analyze_company_trends(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析公司趋势（兼容companies_simple.py的调用）"""
        if not self.model:
            return {"error": "Gemini API未配置"}
        
        try:
            # 提取数据
            company_name = analysis_data.get('company_name', '未知')
            industry = analysis_data.get('industry', '未知')
            company_code = analysis_data.get('company_code', '未知')
            financial_data = analysis_data.get('financial_data', {})
            
            # 构建趋势分析数据
            trend_data = {
                'name': company_name,
                'code': company_code,
                'industry': industry,
                'revenue_growth': financial_data.get('revenue_growth', 0),
                'profit_growth': financial_data.get('profit_growth', 0),
                'assets_growth': financial_data.get('assets_growth', 0),
                'revenue': financial_data.get('revenue', 0),
                'net_profit': financial_data.get('net_profit', 0),
                'total_assets': financial_data.get('total_assets', 0)
            }
            
            # 构建趋势分析提示
            prompt = self._build_trend_analysis_prompt(trend_data)
            
            # 调用Gemini API
            response = self.model.generate_content(prompt)
            
            # 解析响应
            analysis = self._parse_trend_analysis_response(response.text)
            
            return analysis
            
        except Exception as e:
            logger.error(f"趋势分析失败: {e}")
            return {"error": f"分析失败: {str(e)}"}
    
    def analyze_industry_trends(self, industry_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析行业趋势"""
        if not self.model:
            return {"error": "Gemini API未配置"}
        
        try:
            prompt = self._build_industry_analysis_prompt(industry_data)
            response = self.model.generate_content(prompt)
            analysis = self._parse_industry_analysis_response(response.text)
            
            return analysis
            
        except Exception as e:
            logger.error(f"行业分析失败: {e}")
            return {"error": f"分析失败: {str(e)}"}
    
    def _build_financial_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """构建财务分析提示"""
        prompt = f"""
请分析以下公司的财务状况，重点关注医药、新能源、半导体、芯片等行业特点：

公司信息：
- 公司名称：{data.get('name', '未知')}
- 所属行业：{data.get('industry', '未知')}
- 股票代码：{data.get('code', '未知')}

财务数据：
- 营业收入：{data.get('revenue', 0)} 万元
- 净利润：{data.get('net_profit', 0)} 万元
- 总资产：{data.get('total_assets', 0)} 万元
- 总负债：{data.get('total_liabilities', 0)} 万元
- 经营现金流：{data.get('operating_cash_flow', 0)} 万元

财务比率：
- 净资产收益率(ROE)：{data.get('roe', 0):.2f}%
- 总资产收益率(ROA)：{data.get('roa', 0):.2f}%
- 资产负债率：{data.get('debt_ratio', 0):.2f}%
- 流动比率：{data.get('current_ratio', 0):.2f}

增长率：
- 收入增长率：{data.get('revenue_growth', 0):.2f}%
- 净利润增长率：{data.get('profit_growth', 0):.2f}%

请从以下角度进行分析：
1. 财务健康状况评估
2. 盈利能力分析
3. 偿债能力分析
4. 成长性分析
5. 行业对比分析
6. 投资建议

请用中文回答，格式要清晰易读。
"""
        return prompt
    
    def _build_trend_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """构建趋势分析提示"""
        prompt = f"""
请分析以下公司的发展趋势，重点关注医药、新能源、半导体、芯片等行业特点：

公司信息：
- 公司名称：{data.get('name', '未知')}
- 所属行业：{data.get('industry', '未知')}
- 股票代码：{data.get('code', '未知')}

财务数据：
- 营业收入：{data.get('revenue', 0)} 万元
- 净利润：{data.get('net_profit', 0)} 万元
- 总资产：{data.get('total_assets', 0)} 万元

增长趋势：
- 收入增长率：{data.get('revenue_growth', 0):.2f}%
- 净利润增长率：{data.get('profit_growth', 0):.2f}%
- 资产增长率：{data.get('assets_growth', 0):.2f}%

请从以下角度进行分析：
1. 业务发展趋势
2. 盈利能力趋势
3. 资产扩张趋势
4. 行业地位变化
5. 未来发展前景
6. 投资价值评估

请用中文回答，格式要清晰易读。
"""
        return prompt
    
    def _build_industry_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """构建行业分析提示"""
        prompt = f"""
请分析以下行业的发展趋势和投资机会：

行业信息：
- 行业名称：{data.get('industry', '未知')}
- 市场规模：{data.get('market_size', 0)} 亿元
- 增长率：{data.get('growth_rate', 0):.2f}%
- 公司数量：{data.get('company_count', 0)} 家
- 平均市盈率：{data.get('avg_pe', 0):.2f}

请从以下角度进行分析：
1. 行业发展阶段判断
2. 市场前景分析
3. 政策环境分析
4. 技术发展趋势
5. 投资机会识别
6. 风险因素分析

请用中文回答，重点关注医药、新能源、半导体、芯片等行业特点。
"""
        return prompt
    
    def _parse_financial_analysis_response(self, response: str) -> Dict[str, Any]:
        """解析财务分析响应"""
        try:
            # 简单的响应解析，可以根据需要优化
            analysis = {
                "summary": response[:500] + "..." if len(response) > 500 else response,
                "full_analysis": response,
                "confidence": 0.8,  # 默认置信度
                "key_points": self._extract_key_points(response)
            }
            return analysis
        except Exception as e:
            logger.error(f"解析财务分析响应失败: {e}")
            return {"error": "解析响应失败"}
    
    def _parse_trend_analysis_response(self, response: str) -> Dict[str, Any]:
        """解析趋势分析响应"""
        try:
            analysis = {
                "summary": response[:500] + "..." if len(response) > 500 else response,
                "full_analysis": response,
                "confidence": 0.8,
                "key_points": self._extract_key_points(response)
            }
            return analysis
        except Exception as e:
            logger.error(f"解析趋势分析响应失败: {e}")
            return {"error": "解析响应失败"}
    
    def _parse_industry_analysis_response(self, response: str) -> Dict[str, Any]:
        """解析行业分析响应"""
        try:
            analysis = {
                "summary": response[:500] + "..." if len(response) > 500 else response,
                "full_analysis": response,
                "confidence": 0.8,
                "key_points": self._extract_key_points(response)
            }
            return analysis
        except Exception as e:
            logger.error(f"解析行业分析响应失败: {e}")
            return {"error": "解析响应失败"}
    
    def _extract_key_points(self, text: str) -> List[str]:
        """提取关键点"""
        # 简单的关键点提取，可以根据需要优化
        key_points = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or line.startswith('1.') or line.startswith('2.')):
                key_points.append(line)
        
        return key_points[:5]  # 最多返回5个关键点 