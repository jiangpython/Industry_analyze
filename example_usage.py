#!/usr/bin/env python3
"""
本地存储使用示例
"""

import json
from app.utils.local_storage import local_storage
from app.services.processors.financial_processor import FinancialProcessor
from app.services.analyzers.gemini_analyzer import GeminiAnalyzer

def example_add_company():
    """示例：添加公司"""
    print("📝 添加公司示例")
    
    # 添加公司数据
    company_data = {
        "code": "000001",
        "name": "平安银行",
        "industry": "银行",
        "market": "A股",
        "description": "中国平安集团旗下银行"
    }
    
    success = local_storage.save_company(company_data)
    if success:
        print("✅ 公司添加成功")
    else:
        print("❌ 公司添加失败")

def example_add_financial_data():
    """示例：添加财务数据"""
    print("\n📊 添加财务数据示例")
    
    # 添加财务数据
    financial_data = {
        "report_date": "2024-01-01",
        "data_type": "年报",
        "revenue": 1000000,  # 营业收入（万元）
        "net_profit": 200000,  # 净利润（万元）
        "total_assets": 5000000,  # 总资产（万元）
        "total_liabilities": 3000000,  # 总负债（万元）
        "operating_cash_flow": 250000,  # 经营现金流（万元）
    }
    
    success = local_storage.save_financial_data("000001", financial_data)
    if success:
        print("✅ 财务数据添加成功")
    else:
        print("❌ 财务数据添加失败")

def example_process_financial_data():
    """示例：处理财务数据"""
    print("\n🔧 处理财务数据示例")
    
    # 获取财务数据
    financial_data = local_storage.get_financial_data("000001")
    if financial_data:
        latest_data = financial_data[-1]
        
        # 处理数据
        processor = FinancialProcessor()
        processed_data = processor.process_company_data(latest_data)
        
        print("📈 财务比率:")
        print(f"  - ROE: {processed_data.get('roe', 0):.2f}%")
        print(f"  - ROA: {processed_data.get('roa', 0):.2f}%")
        print(f"  - 资产负债率: {processed_data.get('debt_ratio', 0):.2f}%")
        print(f"  - 流动比率: {processed_data.get('current_ratio', 0):.2f}")
    else:
        print("❌ 未找到财务数据")

def example_ai_analysis():
    """示例：AI分析"""
    print("\n🤖 AI分析示例")
    
    # 获取公司数据
    company = local_storage.get_company("000001")
    financial_data = local_storage.get_financial_data("000001")
    
    if company and financial_data:
        latest_financial = financial_data[-1]
        
        # 准备分析数据
        analysis_data = {
            'name': company.get('name'),
            'code': company.get('code'),
            'industry': company.get('industry'),
            'revenue': latest_financial.get('revenue'),
            'net_profit': latest_financial.get('net_profit'),
            'total_assets': latest_financial.get('total_assets'),
            'total_liabilities': latest_financial.get('total_liabilities'),
            'operating_cash_flow': latest_financial.get('operating_cash_flow'),
        }
        
        # AI分析
        analyzer = GeminiAnalyzer()
        result = analyzer.analyze_company_financials(analysis_data)
        
        if "error" not in result:
            print("✅ AI分析完成")
            print(f"📝 分析摘要: {result.get('summary', '')[:100]}...")
            
            # 保存分析结果
            analysis_data = {
                "target_type": "company",
                "target_id": "000001",
                "analysis_type": "financial",
                "title": f"{company.get('name')}财务分析报告",
                "summary": result.get("summary", ""),
                "details": result.get("full_analysis", ""),
                "ai_model": "gemini-pro",
                "confidence": result.get("confidence", 0.8)
            }
            
            local_storage.save_analysis_result(analysis_data)
        else:
            print(f"❌ AI分析失败: {result['error']}")
    else:
        print("❌ 缺少公司或财务数据")

def example_export_data():
    """示例：导出数据"""
    print("\n📤 导出数据示例")
    
    # 导出到CSV
    success = local_storage.export_to_csv()
    if success:
        print("✅ 数据导出成功")
        print(f"📁 CSV文件位置:")
        print(f"  - 公司数据: {local_storage.settings.COMPANIES_CSV}")
        print(f"  - 财务数据: {local_storage.settings.FINANCIAL_DATA_CSV}")
    else:
        print("❌ 数据导出失败")

def example_backup_data():
    """示例：备份数据"""
    print("\n💾 备份数据示例")
    
    success = local_storage.backup_data()
    if success:
        print("✅ 数据备份成功")
    else:
        print("❌ 数据备份失败")

def example_view_data():
    """示例：查看数据"""
    print("\n👀 查看数据示例")
    
    # 查看所有公司
    companies = local_storage.get_all_companies()
    print(f"📊 公司总数: {len(companies)}")
    
    for company_id, company_data in companies.items():
        print(f"  - {company_id}: {company_data.get('name')} ({company_data.get('industry')})")
    
    # 查看财务数据
    financial_data = local_storage.get_financial_data("000001")
    print(f"📈 财务数据记录数: {len(financial_data)}")
    
    # 查看分析结果
    analysis_results = local_storage.get_analysis_results("company", "000001")
    print(f"🤖 分析结果数: {len(analysis_results)}")

def main():
    """主函数"""
    print("🚀 本地存储使用示例\n")
    
    # 运行示例
    example_add_company()
    example_add_financial_data()
    example_process_financial_data()
    example_ai_analysis()
    example_export_data()
    example_backup_data()
    example_view_data()
    
    print("\n✅ 所有示例执行完成！")
    print("\n💡 数据文件位置:")
    print(f"  - 公司数据: {local_storage.settings.COMPANIES_FILE}")
    print(f"  - 财务数据: {local_storage.settings.FINANCIAL_DATA_FILE}")
    print(f"  - 行业数据: {local_storage.settings.INDUSTRY_DATA_FILE}")
    print(f"  - 分析结果: {local_storage.settings.ANALYSIS_RESULTS_FILE}")

if __name__ == "__main__":
    main() 