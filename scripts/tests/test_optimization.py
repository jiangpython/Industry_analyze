#!/usr/bin/env python3
"""
测试优化效果
验证缓存机制是否有效减少重复获取
"""

import requests
import time
import json

def test_optimization():
    """测试优化效果"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🚀 测试优化效果")
    print("=" * 50)
    
    # 测试1: 第一次获取（应该显示获取所有A股数据）
    print("1. 第一次获取股票数据（应该获取所有A股数据）:")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/companies/000001?force_refresh=true")
        if response.status_code == 200:
            data = response.json()
            end_time = time.time()
            print(f"   ✅ 成功: {data.get('name')} - 耗时: {end_time - start_time:.2f}秒")
        else:
            print(f"   ❌ 失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 测试2: 第二次获取（应该使用缓存）
    print("2. 第二次获取股票数据（应该使用缓存）:")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/companies/000002?force_refresh=true")
        if response.status_code == 200:
            data = response.json()
            end_time = time.time()
            print(f"   ✅ 成功: {data.get('name')} - 耗时: {end_time - start_time:.2f}秒")
        else:
            print(f"   ❌ 失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 测试3: 第三次获取（应该使用缓存）
    print("3. 第三次获取股票数据（应该使用缓存）:")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/companies/300750?force_refresh=true")
        if response.status_code == 200:
            data = response.json()
            end_time = time.time()
            print(f"   ✅ 成功: {data.get('name')} - 耗时: {end_time - start_time:.2f}秒")
        else:
            print(f"   ❌ 失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 测试4: 获取行业数据（应该使用缓存）
    print("4. 获取行业数据（应该使用缓存）:")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/companies/?industry=医药&force_refresh=true")
        if response.status_code == 200:
            data = response.json()
            end_time = time.time()
            print(f"   ✅ 成功: 获取到 {len(data)} 家医药公司 - 耗时: {end_time - start_time:.2f}秒")
        else:
            print(f"   ❌ 失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n📊 优化说明:")
    print("- 第一次请求会获取所有A股数据并缓存5分钟")
    print("- 后续请求在5分钟内会使用缓存，大幅提升速度")
    print("- 缓存过期后会重新获取所有数据")

if __name__ == "__main__":
    test_optimization() 