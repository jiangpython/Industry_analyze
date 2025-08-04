#!/usr/bin/env python3
"""
本地文件存储使用示例
演示如何使用JSON和Excel文件进行数据存储和管理
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.data_manager import data_manager
from datetime import datetime

def example_basic_operations():
    """基础操作示例"""
    print("=== 基础数据操作示例 ===")
    
    # 1. 保存公司数据
    company_data = {
        "code": "AAPL",
        "name": "Apple Inc.",
        "industry": "科技",
        "market": "美股",
        "description": "苹果公司"
    }
    
    success = data_manager.save_company(company_data)
    print(f"保存公司数据: {'成功' if success else '失败'}")
    
    # 2. 获取公司数据
    company = data_manager.get_company("AAPL")
    print(f"获取公司数据: {company.get('name', '未找到')}")
    
    # 3. 保存财务数据
    financial_data = {
        "report_date": "2024-01-01",
        "data_type": "年报",
        "revenue": 1000000,
        "net_profit": 200000,
        "total_assets": 5000000,
        "total_liabilities": 2000000
    }
    
    success = data_manager.save_financial_data("AAPL", financial_data)
    print(f"保存财务数据: {'成功' if success else '失败'}")
    
    # 4. 获取财务数据
    financial_records = data_manager.get_financial_data("AAPL")
    print(f"获取财务数据记录数: {len(financial_records)}")

def example_data_export():
    """数据导出示例"""
    print("\n=== 数据导出示例 ===")
    
    # 1. 导出到Excel
    success = data_manager.export_to_excel()
    print(f"导出Excel: {'成功' if success else '失败'}")
    
    # 2. 备份数据
    success = data_manager.backup_data()
    print(f"备份数据: {'成功' if success else '失败'}")
    
    # 3. 获取数据摘要
    summary = data_manager.get_data_summary()
    print("数据摘要:")
    for key, value in summary.items():
        print(f"  {key}: {value}")

def example_data_view():
    """数据查看示例"""
    print("\n=== 数据查看示例 ===")
    
    # 1. 查看所有公司
    companies = data_manager.get_all_companies()
    print(f"公司总数: {len(companies)}")
    for company_id, company_data in companies.items():
        print(f"  {company_id}: {company_data.get('name', '未知')}")
    
    # 2. 查看分析结果
    analysis_results = data_manager.get_analysis_results()
    print(f"\n分析结果总数: {len(analysis_results)}")

def example_industry_data():
    """行业数据示例"""
    print("\n=== 行业数据示例 ===")
    
    # 保存行业数据
    industry_data = {
        "name": "医药",
        "description": "医药行业分析",
        "companies_count": 50,
        "avg_pe": 25.5,
        "growth_rate": 0.15
    }
    
    success = data_manager.save_industry_data("医药", industry_data)
    print(f"保存行业数据: {'成功' if success else '失败'}")
    
    # 获取行业数据
    industry = data_manager.get_industry_data("医药")
    if industry:
        print(f"行业名称: {industry.get('name')}")
        print(f"公司数量: {industry.get('companies_count')}")

def main():
    """主函数"""
    print("🚀 本地文件存储使用示例\n")
    
    # 运行各种示例
    example_basic_operations()
    example_data_export()
    example_data_view()
    example_industry_data()
    
    print("\n✅ 所有示例执行完成！")
    print("\n📁 数据文件位置:")
    print(f"  - 公司数据: {data_manager._get_file_path('companies.json')}")
    print(f"  - 财务数据: {data_manager._get_file_path('financial_data.json')}")
    print(f"  - 行业数据: {data_manager._get_file_path('industry_data.json')}")
    print(f"  - 分析结果: {data_manager._get_file_path('analysis_results.json')}")
    
    print("\n💡 提示:")
    print("  - 数据文件会自动创建在 ./data/ 目录下")
    print("  - 可以使用 data_manager.export_to_excel() 导出Excel文件")
    print("  - 可以使用 data_manager.backup_data() 备份数据")

if __name__ == "__main__":
    main() 