#!/usr/bin/env python3
"""
实时数据使用演示
展示如何使用混合模式的实时数据API
"""

import requests
import json
from typing import Dict, Any

def test_realtime_api():
    """测试实时数据API"""
    base_url = "http://localhost:8000/api/v1/realtime"
    
    print("🚀 实时数据API测试\n")
    
    # 1. 测试AKShare连接
    print("1. 测试AKShare连接:")
    try:
        response = requests.get(f"{base_url}/test/akshare")
        result = response.json()
        print(f"   状态: {result.get('status')}")
        print(f"   消息: {result.get('message')}")
        print(f"   数据量: {result.get('data_count')}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 2. 测试获取个股实时数据
    print("2. 测试获取个股实时数据:")
    test_symbols = ["000001", "000002", "300750"]  # 平安银行、万科A、宁德时代
    
    for symbol in test_symbols:
        try:
            print(f"   获取 {symbol} 的实时数据:")
            response = requests.get(f"{base_url}/stock/{symbol}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ 成功: {data.get('name')} - 价格: {data.get('current_price')} "
                      f"涨跌幅: {data.get('change_percent')}% 来源: {data.get('source')}")
            else:
                print(f"   ❌ 失败: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
    
    print()
    
    # 3. 测试获取行业公司列表
    print("3. 测试获取行业公司列表:")
    test_industries = ["医药", "新能源", "半导体"]
    
    for industry in test_industries:
        try:
            print(f"   获取 {industry} 行业的公司:")
            response = requests.get(f"{base_url}/companies/{industry}")
            
            if response.status_code == 200:
                companies = response.json()
                print(f"   ✅ 成功: 找到 {len(companies)} 家公司")
                
                # 显示前3家公司
                for i, company in enumerate(companies[:3]):
                    print(f"     {i+1}. {company.get('code')}: {company.get('name')} "
                          f"(价格: {company.get('current_price')} "
                          f"涨跌幅: {company.get('change_percent')}%)")
                
                if len(companies) > 3:
                    print(f"     ... 还有 {len(companies) - 3} 家公司")
            else:
                print(f"   ❌ 失败: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
    
    print()
    
    # 4. 测试强制刷新
    print("4. 测试强制刷新:")
    try:
        print("   强制刷新 000001 的数据:")
        response = requests.get(f"{base_url}/stock/000001?force_refresh=true")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 强制刷新成功: 来源: {data.get('source')} "
                  f"更新时间: {data.get('update_time')}")
        else:
            print(f"   ❌ 强制刷新失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 5. 获取缓存信息
    print("5. 获取缓存信息:")
    try:
        response = requests.get(f"{base_url}/cache/info")
        if response.status_code == 200:
            cache_info = response.json()
            print(f"   ✅ 缓存数量: {len(cache_info)}")
            for key, info in cache_info.items():
                print(f"     {key}: {info.get('data_type')} - {info.get('timestamp')}")
        else:
            print(f"   ❌ 获取缓存信息失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 6. 获取实时数据摘要
    print("6. 获取实时数据摘要:")
    try:
        response = requests.get(f"{base_url}/summary")
        if response.status_code == 200:
            summary = response.json()
            print(f"   ✅ 缓存数量: {summary.get('cache_count')}")
            print(f"   数据摘要: {summary.get('data_summary')}")
            print(f"   AKShare状态: {summary.get('akshare_status', {}).get('status')}")
        else:
            print(f"   ❌ 获取摘要失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")

def show_api_usage():
    """展示API使用方法"""
    print("\n=== API使用方法 ===\n")
    
    usage_examples = """
# 1. 获取个股实时数据
GET /api/v1/realtime/stock/{symbol}
GET /api/v1/realtime/stock/000001
GET /api/v1/realtime/stock/000001?force_refresh=true

# 2. 获取行业公司列表
GET /api/v1/realtime/companies/{industry}
GET /api/v1/realtime/companies/医药
GET /api/v1/realtime/companies/新能源?force_refresh=true

# 3. 获取缓存信息
GET /api/v1/realtime/cache/info

# 4. 清除缓存
DELETE /api/v1/realtime/cache
DELETE /api/v1/realtime/cache?cache_key=stock_cache_000001

# 5. 测试AKShare连接
GET /api/v1/realtime/test/akshare

# 6. 获取实时数据摘要
GET /api/v1/realtime/summary
"""
    
    print("API端点示例:")
    print(usage_examples)

def main():
    """主函数"""
    print("🎯 实时数据API使用演示\n")
    
    # 测试API
    test_realtime_api()
    
    # 展示使用方法
    show_api_usage()
    
    print("\n💡 使用说明:")
    print("1. 系统会自动使用缓存数据（5分钟内有效）")
    print("2. 使用 force_refresh=true 可以强制获取最新数据")
    print("3. 如果实时获取失败，会自动降级到本地存储")
    print("4. 缓存数据会保存在 ./data/cache.json 中")
    print("5. 可以通过 /cache/info 查看缓存状态")

if __name__ == "__main__":
    main() 