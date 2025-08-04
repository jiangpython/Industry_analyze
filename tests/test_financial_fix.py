#!/usr/bin/env python3
"""
测试修复后的财务数据获取功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.services.collectors.akshare_collector import AKShareCollector
from app.services.processors.akshare_processor import AKShareDataProcessor
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_financial_data_collection():
    """测试财务数据采集"""
    print("🔍 测试财务数据采集功能")
    print("=" * 60)
    
    collector = AKShareCollector()
    processor = AKShareDataProcessor()
    
    test_symbols = ["000001", "000002", "300750", "600519"]  # 平安银行、万科A、宁德时代、贵州茅台
    
    for symbol in test_symbols:
        print(f"\n📊 测试股票代码: {symbol}")
        print("-" * 40)
        
        try:
            # 获取股票数据
            stock_data = collector.get_stock_data(symbol)
            
            if "error" in stock_data:
                print(f"   ❌ 获取股票数据失败: {stock_data['error']}")
                continue
            
            print(f"   ✅ 成功获取股票基本信息")
            print(f"   公司名称: {stock_data.get('company_name', '未知')}")
            print(f"   所属行业: {stock_data.get('industry', '未知')}")
            print(f"   市场: {stock_data.get('market', '未知')}")
            
            # 检查财务数据
            financial_data = stock_data.get('financial_data', {})
            if financial_data:
                print(f"   ✅ 成功获取财务数据")
                
                # 检查资产负债表
                balance_sheet = financial_data.get('balance_sheet', {})
                if balance_sheet:
                    print(f"   资产负债表数据:")
                    for key, value in balance_sheet.items():
                        print(f"     {key}: {value}")
                
                # 检查利润表
                income_statement = financial_data.get('income_statement', {})
                if income_statement:
                    print(f"   利润表数据:")
                    for key, value in income_statement.items():
                        print(f"     {key}: {value}")
                
                # 检查现金流量表
                cash_flow = financial_data.get('cash_flow', {})
                if cash_flow:
                    print(f"   现金流量表数据:")
                    for key, value in cash_flow.items():
                        print(f"     {key}: {value}")
                
                # 检查关键指标
                key_indicators = financial_data.get('key_indicators', {})
                if key_indicators:
                    print(f"   关键财务指标:")
                    for key, value in key_indicators.items():
                        print(f"     {key}: {value}")
                
                # 处理财务数据
                processed_financial = processor.process_financial_data(stock_data)
                if processed_financial and not any("error" in item for item in processed_financial):
                    print(f"   ✅ 财务数据处理成功")
                    print(f"   处理后的数据条数: {len(processed_financial)}")
                else:
                    print(f"   ⚠️  财务数据处理失败或无数据")
            else:
                print(f"   ⚠️  无财务数据")
            
            # 检查历史数据
            historical_data = stock_data.get('historical_data', [])
            if historical_data:
                print(f"   ✅ 成功获取历史数据")
                print(f"   历史数据条数: {len(historical_data)}")
                if historical_data:
                    latest_data = historical_data[0]
                    print(f"   最新数据日期: {latest_data.get('date', '未知')}")
                    print(f"   最新收盘价: {latest_data.get('close', '未知')}")
            else:
                print(f"   ⚠️  无历史数据")
                
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")

def test_financial_analysis():
    """测试财务分析功能"""
    print("\n🔍 测试财务分析功能")
    print("=" * 60)
    
    from app.services.processors.financial_processor import FinancialProcessor
    
    processor = FinancialProcessor()
    
    # 模拟财务数据
    test_financial_data = {
        'revenue': 1000000,  # 100万元
        'net_profit': 100000,  # 10万元
        'total_assets': 2000000,  # 200万元
        'total_liabilities': 800000,  # 80万元
        'operating_cash_flow': 120000,  # 12万元
        'revenue_growth': 15.5,
        'profit_growth': 12.3
    }
    
    try:
        # 处理财务数据
        processed_data = processor.process_company_data(test_financial_data)
        print(f"   ✅ 财务数据处理成功")
        
        # 计算财务比率
        ratios = processor.calculate_financial_ratios(test_financial_data)
        print(f"   财务比率:")
        for key, value in ratios.items():
            print(f"     {key}: {value:.2f}")
        
        # 分析财务健康
        health_analysis = processor.analyze_financial_health(processed_data)
        print(f"   财务健康分析:")
        print(f"     评分: {health_analysis.get('score', 0)}")
        print(f"     风险等级: {health_analysis.get('risk_level', 'unknown')}")
        print(f"     优势: {health_analysis.get('strengths', [])}")
        print(f"     劣势: {health_analysis.get('weaknesses', [])}")
        print(f"     建议: {health_analysis.get('recommendations', [])}")
        
    except Exception as e:
        print(f"   ❌ 财务分析失败: {e}")

def test_api_integration():
    """测试API集成"""
    print("\n🔍 测试API集成")
    print("=" * 60)
    
    try:
        from app.api.endpoints.companies_simple import data_manager
        
        test_symbol = "000001"
        
        # 测试获取公司信息
        company_data = data_manager.get_company(test_symbol)
        if company_data:
            print(f"   ✅ 成功获取公司信息: {company_data.get('name', '未知')}")
        else:
            print(f"   ⚠️  未找到公司信息")
        
        # 测试获取财务数据
        financial_data = data_manager.get_financial_data(test_symbol)
        if financial_data:
            print(f"   ✅ 成功获取财务数据")
            print(f"   财务数据条数: {len(financial_data)}")
            if financial_data:
                latest_financial = financial_data[0]
                print(f"   最新财务数据:")
                for key, value in latest_financial.items():
                    if key not in ['created_at', 'updated_at']:
                        print(f"     {key}: {value}")
        else:
            print(f"   ⚠️  未找到财务数据")
            
    except Exception as e:
        print(f"   ❌ API集成测试失败: {e}")

def main():
    """主函数"""
    print("🚀 财务数据获取功能测试")
    print("=" * 80)
    
    # 测试财务数据采集
    test_financial_data_collection()
    
    # 测试财务分析功能
    test_financial_analysis()
    
    # 测试API集成
    test_api_integration()
    
    print("\n🎯 测试总结:")
    print("1. 检查AKShare财务数据获取是否正常")
    print("2. 验证财务数据处理和分析功能")
    print("3. 确认API集成是否正常工作")

if __name__ == "__main__":
    main() 