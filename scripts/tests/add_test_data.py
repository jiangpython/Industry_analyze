#!/usr/bin/env python3
"""
添加测试数据脚本
"""

from app.utils.data_manager import data_manager
from datetime import datetime

def add_test_companies():
    """添加测试公司数据"""
    print("=== 添加测试公司数据 ===")
    
    # 医药行业公司
    medical_companies = {
        "PFE": {
            "code": "PFE",
            "name": "Pfizer Inc.",
            "industry": "医药",
            "market": "美股",
            "description": "辉瑞制药公司"
        },
        "JNJ": {
            "code": "JNJ", 
            "name": "Johnson & Johnson",
            "industry": "医药",
            "market": "美股",
            "description": "强生公司"
        },
        "000001": {
            "code": "000001",
            "name": "平安银行",
            "industry": "金融",
            "market": "A股",
            "description": "平安银行股份有限公司"
        }
    }
    
    # 新能源行业公司
    new_energy_companies = {
        "TSLA": {
            "code": "TSLA",
            "name": "Tesla Inc.",
            "industry": "新能源",
            "market": "美股",
            "description": "特斯拉公司"
        },
        "300750": {
            "code": "300750",
            "name": "宁德时代",
            "industry": "新能源",
            "market": "A股",
            "description": "宁德时代新能源科技股份有限公司"
        }
    }
    
    # 半导体行业公司
    semiconductor_companies = {
        "NVDA": {
            "code": "NVDA",
            "name": "NVIDIA Corporation",
            "industry": "半导体",
            "market": "美股",
            "description": "英伟达公司"
        },
        "000002": {
            "code": "000002",
            "name": "万科A",
            "industry": "房地产",
            "market": "A股",
            "description": "万科企业股份有限公司"
        }
    }
    
    # 合并所有公司
    all_companies = {**medical_companies, **new_energy_companies, **semiconductor_companies}
    
    # 添加公司数据
    for code, company_data in all_companies.items():
        success = data_manager.save_company(company_data)
        print(f"添加公司 {code}: {'成功' if success else '失败'}")
    
    print(f"\n总共添加了 {len(all_companies)} 家公司")

def add_test_financial_data():
    """添加测试财务数据"""
    print("\n=== 添加测试财务数据 ===")
    
    companies = ["PFE", "JNJ", "TSLA", "NVDA", "000001", "300750", "000002"]
    
    for company_code in companies:
        financial_data = {
            "report_date": "2024-01-01",
            "data_type": "年报",
            "revenue": 1000000 + hash(company_code) % 5000000,  # 随机收入
            "net_profit": 200000 + hash(company_code) % 1000000,  # 随机净利润
            "total_assets": 5000000 + hash(company_code) % 20000000,  # 随机总资产
            "total_liabilities": 2000000 + hash(company_code) % 8000000,  # 随机总负债
            "operating_cash_flow": 300000 + hash(company_code) % 1500000  # 随机经营现金流
        }
        
        success = data_manager.save_financial_data(company_code, financial_data)
        print(f"添加 {company_code} 财务数据: {'成功' if success else '失败'}")

def add_test_industry_data():
    """添加测试行业数据"""
    print("\n=== 添加测试行业数据 ===")
    
    industries = {
        "医药": {
            "name": "医药",
            "description": "医药行业分析",
            "companies_count": 2,
            "avg_pe": 25.5,
            "growth_rate": 0.15,
            "market_size": 5000000000,
            "updated_at": datetime.now().isoformat()
        },
        "新能源": {
            "name": "新能源",
            "description": "新能源行业分析",
            "companies_count": 2,
            "avg_pe": 35.2,
            "growth_rate": 0.25,
            "market_size": 3000000000,
            "updated_at": datetime.now().isoformat()
        },
        "半导体": {
            "name": "半导体",
            "description": "半导体行业分析",
            "companies_count": 1,
            "avg_pe": 28.8,
            "growth_rate": 0.20,
            "market_size": 4000000000,
            "updated_at": datetime.now().isoformat()
        }
    }
    
    for industry_name, industry_data in industries.items():
        success = data_manager.save_industry_data(industry_name, industry_data)
        print(f"添加 {industry_name} 行业数据: {'成功' if success else '失败'}")

def main():
    """主函数"""
    print("🚀 开始添加测试数据...\n")
    
    # 添加公司数据
    add_test_companies()
    
    # 添加财务数据
    add_test_financial_data()
    
    # 添加行业数据
    add_test_industry_data()
    
    print("\n✅ 测试数据添加完成！")
    print("\n📊 数据统计:")
    companies = data_manager.get_all_companies()
    print(f"  公司总数: {len(companies)}")
    
    # 按行业统计
    industry_count = {}
    for company_data in companies.values():
        industry = company_data.get('industry', '未知')
        industry_count[industry] = industry_count.get(industry, 0) + 1
    
    print("  行业分布:")
    for industry, count in industry_count.items():
        print(f"    {industry}: {count} 家公司")

if __name__ == "__main__":
    main() 