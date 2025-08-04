#!/usr/bin/env python3
"""
测试API错误
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.services.realtime_data_service import RealtimeDataService
from app.utils.data_manager import data_manager
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_financial_data_api():
    """测试财务数据API"""
    print("🔍 测试财务数据API")
    print("=" * 60)
    
    company_code = "000999"
    
    try:
        # 测试RealtimeDataService
        print(f"1. 测试RealtimeDataService.get_financial_data({company_code})")
        realtime_service = RealtimeDataService()
        financial_data = realtime_service.get_financial_data(company_code, force_refresh=True)
        print(f"   结果: {len(financial_data) if financial_data else 0} 条数据")
        if financial_data:
            print(f"   第一条数据: {financial_data[0]}")
        
    except Exception as e:
        print(f"   ❌ RealtimeDataService错误: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        # 测试data_manager
        print(f"\n2. 测试data_manager.get_financial_data({company_code})")
        local_data = data_manager.get_financial_data(company_code)
        print(f"   结果: {len(local_data) if local_data else 0} 条数据")
        if local_data:
            print(f"   第一条数据: {local_data[0]}")
        
    except Exception as e:
        print(f"   ❌ data_manager错误: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        # 测试AKShare直接调用
        print(f"\n3. 测试AKShare直接调用")
        import akshare as ak
        
        # 测试资产负债表
        print("   测试资产负债表...")
        balance_sheet = ak.stock_balance_sheet_by_report_em(symbol=company_code)
        print(f"   资产负债表: {'成功' if not balance_sheet.empty else '无数据'}")
        if not balance_sheet.empty:
            print(f"   数据形状: {balance_sheet.shape}")
            print(f"   列名: {list(balance_sheet.columns)}")
        
        # 测试利润表
        print("   测试利润表...")
        income_statement = ak.stock_financial_analysis_indicator_em(symbol=company_code)
        print(f"   利润表: {'成功' if not income_statement.empty else '无数据'}")
        if not income_statement.empty:
            print(f"   数据形状: {income_statement.shape}")
            print(f"   列名: {list(income_statement.columns)}")
        
        # 测试现金流量表
        print("   测试现金流量表...")
        cash_flow = ak.stock_cash_flow_sheet_by_report_em(symbol=company_code)
        print(f"   现金流量表: {'成功' if not cash_flow.empty else '无数据'}")
        if not cash_flow.empty:
            print(f"   数据形状: {cash_flow.shape}")
            print(f"   列名: {list(cash_flow.columns)}")
        
    except Exception as e:
        print(f"   ❌ AKShare直接调用错误: {e}")
        import traceback
        traceback.print_exc()

def test_api_endpoint_simulation():
    """模拟API端点调用"""
    print("\n🔍 模拟API端点调用")
    print("=" * 60)
    
    company_code = "000999"
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    force_refresh = False
    
    try:
        from app.api.endpoints.companies_simple import get_company_financial_data
        from fastapi import HTTPException
        
        print(f"模拟调用: get_company_financial_data({company_code}, start_date={start_date}, end_date={end_date}, force_refresh={force_refresh})")
        
        # 这里不能直接调用，因为需要FastAPI的依赖注入
        # 我们直接测试核心逻辑
        
        # 测试RealtimeDataService
        realtime_service = RealtimeDataService()
        financial_records = None
        
        if force_refresh:
            financial_records = realtime_service.get_financial_data(company_code, force_refresh)
        
        if not financial_records:
            financial_records = data_manager.get_financial_data(company_code)
            
            if not financial_records:
                print(f"   本地无数据，启动实时采集: {company_code}")
                financial_records = realtime_service.get_financial_data(company_code, force_refresh=True)
        
        if not financial_records:
            print(f"   ❌ 未找到公司 {company_code} 的财务数据")
        else:
            print(f"   ✅ 找到 {len(financial_records)} 条财务数据")
            for i, record in enumerate(financial_records[:3]):  # 只显示前3条
                print(f"   数据{i+1}: {record}")
        
    except Exception as e:
        print(f"   ❌ 模拟API调用错误: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("🚀 API错误诊断测试")
    print("=" * 80)
    
    # 测试财务数据API
    test_financial_data_api()
    
    # 模拟API端点调用
    test_api_endpoint_simulation()
    
    print("\n🎯 测试总结:")
    print("1. 检查RealtimeDataService是否正常工作")
    print("2. 检查data_manager是否正常工作")
    print("3. 检查AKShare API调用是否正常")
    print("4. 模拟API端点调用逻辑")

if __name__ == "__main__":
    main() 