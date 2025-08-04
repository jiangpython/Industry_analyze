#!/usr/bin/env python3
"""
测试实时API功能
"""

import requests
import json

def test_companies_api():
    """测试公司API"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 测试公司API功能")
    print("=" * 50)
    
    # 测试1: 获取医药行业公司（实时）
    print("1. 测试获取医药行业公司（实时数据）")
    try:
        response = requests.get(f"{base_url}/companies/?industry=医药&force_refresh=true")
        if response.status_code == 200:
            companies = response.json()
            print(f"✅ 成功获取医药行业公司: {len(companies)} 家")
            for company in companies[:3]:  # 显示前3家
                print(f"   - {company['code']}: {company['name']} ({company['industry']})")
        else:
            print(f"❌ 获取医药行业公司失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print()
    
    # 测试2: 获取特定公司（实时）
    print("2. 测试获取特定公司（实时数据）")
    try:
        response = requests.get(f"{base_url}/companies/000999?force_refresh=true")
        if response.status_code == 200:
            company = response.json()
            print(f"✅ 成功获取公司: {company['code']} - {company['name']}")
        else:
            print(f"❌ 获取公司失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print()
    
    # 测试3: 获取新能源行业公司（缓存）
    print("3. 测试获取新能源行业公司（缓存数据）")
    try:
        response = requests.get(f"{base_url}/companies/?industry=新能源")
        if response.status_code == 200:
            companies = response.json()
            print(f"✅ 成功获取新能源行业公司: {len(companies)} 家")
            for company in companies[:3]:  # 显示前3家
                print(f"   - {company['code']}: {company['name']} ({company['industry']})")
        else:
            print(f"❌ 获取新能源行业公司失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")

def test_realtime_api():
    """测试实时数据API"""
    base_url = "http://localhost:8000/api/v1"
    
    print("\n🧪 测试实时数据API功能")
    print("=" * 50)
    
    # 测试1: 获取股票实时数据
    print("1. 测试获取股票实时数据")
    try:
        response = requests.get(f"{base_url}/realtime/stock/000001?force_refresh=true")
        if response.status_code == 200:
            stock_data = response.json()
            print(f"✅ 成功获取股票数据: {stock_data['code']} - {stock_data['name']}")
            print(f"   当前价格: {stock_data.get('current_price', 'N/A')}")
            print(f"   涨跌幅: {stock_data.get('change_percent', 'N/A')}%")
        else:
            print(f"❌ 获取股票数据失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print()
    
    # 测试2: 获取行业实时数据
    print("2. 测试获取行业实时数据")
    try:
        response = requests.get(f"{base_url}/realtime/companies/医药?force_refresh=true")
        if response.status_code == 200:
            companies = response.json()
            print(f"✅ 成功获取医药行业实时数据: {len(companies)} 家")
            for company in companies[:3]:  # 显示前3家
                print(f"   - {company['code']}: {company['name']}")
        else:
            print(f"❌ 获取行业数据失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")

if __name__ == "__main__":
    print("🚀 开始测试实时API功能")
    print("请确保应用正在运行: http://localhost:8000")
    print()
    
    test_companies_api()
    test_realtime_api()
    
    print("\n✅ 测试完成！") 