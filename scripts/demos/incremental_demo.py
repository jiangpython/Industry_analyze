#!/usr/bin/env python3
"""
增量数据获取演示
展示智能增量更新逻辑
"""

import requests
import json
from datetime import datetime, timedelta

def demonstrate_incremental_logic():
    """演示增量更新逻辑"""
    base_url = "http://localhost:8000/api/v1/historical"
    
    print("🎯 增量数据获取演示\n")
    
    # 1. 演示增量更新逻辑
    print("1. 增量更新逻辑演示:")
    try:
        response = requests.get(f"{base_url}/incremental/demo")
        if response.status_code == 200:
            demo = response.json()
            print(f"   ✅ 演示信息获取成功")
            
            for scenario_name, scenario in demo['scenarios'].items():
                print(f"\n   📊 {scenario['description']}")
                print(f"      请求: {scenario['request']}")
                print(f"      缓存状态: {scenario['cache_status']}")
                print(f"      增量操作: {scenario['incremental_action']}")
                print(f"      效率提升: {scenario['efficiency_gain']}")
            
            print(f"\n   💡 优势:")
            for benefit in demo['benefits']:
                print(f"      • {benefit}")
        else:
            print(f"   ❌ 演示信息获取失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # 2. 测试获取历史数据
    print("2. 测试获取历史数据:")
    test_symbols = ["000001", "000002"]
    
    for symbol in test_symbols:
        try:
            print(f"\n   获取 {symbol} 历史数据:")
            
            # 第一次获取（可能触发全量获取）
            response = requests.get(f"{base_url}/stock/{symbol}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ 成功: {data.get('total_records')} 条记录")
                print(f"      来源: {data.get('source')}")
                print(f"      日期范围: {data.get('date_range', {}).get('start')} 到 {data.get('date_range', {}).get('end')}")
            else:
                print(f"   ❌ 失败: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # 3. 测试增量更新
    print("3. 测试增量更新:")
    try:
        # 再次获取相同数据（应该使用缓存）
        response = requests.get(f"{base_url}/stock/000001")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 第二次获取: {data.get('source')}")
            print(f"      记录数: {data.get('total_records')}")
            
            # 强制刷新
            response = requests.get(f"{base_url}/stock/000001?force_refresh=true")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ 强制刷新: {data.get('source')}")
        else:
            print(f"   ❌ 增量更新测试失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # 4. 测试特定日期范围
    print("4. 测试特定日期范围:")
    try:
        # 获取最近30天数据
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        response = requests.get(f"{base_url}/stock/000001?start_date={start_date}&end_date={end_date}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 特定范围获取: {data.get('total_records')} 条记录")
            print(f"      来源: {data.get('source')}")
        else:
            print(f"   ❌ 特定范围获取失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # 5. 获取缓存状态
    print("5. 缓存状态:")
    try:
        response = requests.get(f"{base_url}/cache/status")
        if response.status_code == 200:
            status = response.json()
            print(f"   ✅ 总缓存数: {status.get('total_cache_count')}")
            print(f"      历史数据缓存: {status.get('historical_cache_count')}")
            
            if status.get('historical_caches'):
                print(f"      历史缓存详情:")
                for key, info in status['historical_caches'].items():
                    print(f"        {key}: {info.get('data_type')} - {info.get('timestamp')}")
        else:
            print(f"   ❌ 获取缓存状态失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # 6. 测试数据统计
    print("6. 数据统计:")
    try:
        response = requests.get(f"{base_url}/stock/000001/statistics")
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ 统计信息:")
            print(f"      总记录数: {stats.get('total_records')}")
            print(f"      价格统计: 最低 {stats.get('price_stats', {}).get('min')}, "
                  f"最高 {stats.get('price_stats', {}).get('max')}, "
                  f"平均 {stats.get('price_stats', {}).get('avg'):.2f}")
            print(f"      成交量统计: 总量 {stats.get('volume_stats', {}).get('total')}, "
                  f"平均 {stats.get('volume_stats', {}).get('avg'):.2f}")
        else:
            print(f"   ❌ 获取统计信息失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")

def show_usage_examples():
    """展示使用示例"""
    print("\n=== 使用示例 ===\n")
    
    examples = """
# 1. 获取默认历史数据（最近1年）
GET /api/v1/historical/stock/000001

# 2. 获取指定日期范围
GET /api/v1/historical/stock/000001?start_date=2023-01-01&end_date=2023-12-31

# 3. 强制刷新数据
GET /api/v1/historical/stock/000001?force_refresh=true

# 4. 获取不同周期数据
GET /api/v1/historical/stock/000001?period=weekly
GET /api/v1/historical/stock/000001?period=monthly

# 5. 获取数据统计
GET /api/v1/historical/stock/000001/statistics

# 6. 查看缓存状态
GET /api/v1/historical/cache/status

# 7. 清除缓存
DELETE /api/v1/historical/cache/000001
DELETE /api/v1/historical/cache/000001?period=daily

# 8. 演示增量逻辑
GET /api/v1/historical/incremental/demo
"""
    
    print("API使用示例:")
    print(examples)

def main():
    """主函数"""
    print("🚀 增量数据获取演示\n")
    
    # 演示增量逻辑
    demonstrate_incremental_logic()
    
    # 展示使用示例
    show_usage_examples()
    
    print("\n💡 增量更新优势:")
    print("1. 🚀 智能缓存：只获取缺失的数据")
    print("2. ⚡ 高效响应：减少网络请求次数")
    print("3. 💾 节省资源：避免重复获取已有数据")
    print("4. 🔄 自动合并：智能处理新旧数据")
    print("5. 📊 数据统计：提供价格和成交量分析")

if __name__ == "__main__":
    main() 