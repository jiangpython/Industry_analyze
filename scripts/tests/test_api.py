#!/usr/bin/env python3
"""
API测试脚本
"""

import requests
import json

def test_api():
    """测试API功能"""
    base_url = "http://localhost:8000"
    
    print("=== API测试 ===\n")
    
    # 1. 测试健康检查
    print("1. 健康检查:")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.json()}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. 测试获取公司列表
    print("2. 获取公司列表:")
    try:
        response = requests.get(f"{base_url}/api/v1/companies/")
        print(f"   状态码: {response.status_code}")
        companies = response.json()
        print(f"   公司数量: {len(companies)}")
        for company in companies:
            print(f"   - {company.get('code')}: {company.get('name')} ({company.get('industry')})")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. 测试获取特定公司
    print("3. 获取特定公司 (AAPL):")
    try:
        response = requests.get(f"{base_url}/api/v1/companies/AAPL")
        print(f"   状态码: {response.status_code}")
        company = response.json()
        print(f"   公司名称: {company.get('name')}")
        print(f"   行业: {company.get('industry')}")
        print(f"   市场: {company.get('market')}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 4. 测试获取财务数据
    print("4. 获取财务数据:")
    try:
        response = requests.get(f"{base_url}/api/v1/companies/AAPL/financial-data")
        print(f"   状态码: {response.status_code}")
        financial_data = response.json()
        print(f"   财务记录数: {len(financial_data)}")
        if financial_data:
            latest = financial_data[0]
            print(f"   最新记录:")
            print(f"   - 报告日期: {latest.get('report_date')}")
            print(f"   - 收入: {latest.get('revenue')}")
            print(f"   - 净利润: {latest.get('net_profit')}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 5. 测试获取行业列表
    print("5. 获取行业列表:")
    try:
        response = requests.get(f"{base_url}/api/v1/industries/")
        print(f"   状态码: {response.status_code}")
        industries = response.json()
        print(f"   行业列表: {industries}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 6. 测试行业建议
    print("6. 测试行业建议 (芯片):")
    try:
        response = requests.get(f"{base_url}/api/v1/industries/suggest/芯片")
        print(f"   状态码: {response.status_code}")
        suggestion = response.json()
        print(f"   查询: {suggestion.get('query')}")
        print(f"   映射行业: {suggestion.get('mapped_industry')}")
        print(f"   建议: {suggestion.get('suggestions')}")
    except Exception as e:
        print(f"   错误: {e}")

if __name__ == "__main__":
    test_api() 