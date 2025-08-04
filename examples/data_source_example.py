#!/usr/bin/env python3
"""
数据源选择示例
演示如何使用不同的数据源获取金融数据
"""

import requests
import json
from datetime import datetime, timedelta
import os
import sys

# 添加项目根目录到路径，以便直接运行此脚本
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 直接使用数据源选择器
from app.services.collectors.data_source_selector import DataSourceSelector

# API基础URL
API_BASE_URL = "http://localhost:8000/api/v1"

def print_separator(title):
    """打印分隔符"""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50 + "\n")

def pretty_print(data):
    """美化打印JSON数据"""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def example_direct_usage():
    """示例：直接使用数据源选择器"""
    print_separator("直接使用数据源选择器")
    
    # 创建数据源选择器
    selector = DataSourceSelector()
    
    # 获取A股数据（自动使用AKShare）
    print("获取A股数据（自动使用AKShare）:")
    data = selector.get_stock_data("000001", source="auto")
    if "error" not in data:
        print(f"公司名称: {data.get('company_name')}")
        print(f"行业: {data.get('industry')}")
        print(f"历史数据条数: {len(data.get('historical_data', []))}")
    else:
        print(f"错误: {data.get('error')}")
    
    # 获取美股数据（自动使用Yahoo）
    print("\n获取美股数据（自动使用Yahoo）:")
    data = selector.get_stock_data("AAPL", source="auto")
    if "error" not in data:
        print(f"公司名称: {data.get('company_name')}")
        print(f"行业: {data.get('industry')}")
        print(f"历史数据条数: {len(data.get('historical_data', []))}")
    else:
        print(f"错误: {data.get('error')}")
    
    # 获取市场数据
    print("\n获取市场数据:")
    data = selector.get_market_data("china", source="akshare")
    if "error" not in data:
        indices = data.get('indices', {})
        for code, index_data in indices.items():
            print(f"{index_data.get('name')}: {index_data.get('last_price')} ({index_data.get('change_percent', 0):.2f}%)")
    else:
        print(f"错误: {data.get('error')}")
    
    # 获取行业数据
    print("\n获取行业数据:")
    data = selector.get_industry_data("医药", source="akshare")
    if "error" not in data:
        stocks = data.get('stocks', [])
        print(f"行业: {data.get('industry')}")
        print(f"成分股数量: {len(stocks)}")
        for i, stock in enumerate(stocks[:5]):
            print(f"  {i+1}. {stock.get('name')} ({stock.get('symbol')}): {stock.get('price')} ({stock.get('change_pct', 0):.2f}%)")
        if len(stocks) > 5:
            print(f"  ... 共{len(stocks)}只股票")
    else:
        print(f"错误: {data.get('error')}")

def example_api_usage():
    """示例：通过API使用数据源选择器"""
    print_separator("通过API使用数据源选择器")
    
    # 获取A股数据
    print("获取A股数据:")
    response = requests.get(f"{API_BASE_URL}/data/stock/000001", params={
        "source": "auto",
        "start_date": (datetime.now() - timedelta(days=30)).strftime("%Y%m%d"),
        "end_date": datetime.now().strftime("%Y%m%d")
    })
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            data = result.get("data", {})
            print(f"公司名称: {data.get('company_name')}")
            print(f"行业: {data.get('industry')}")
            print(f"历史数据条数: {len(data.get('historical_data', []))}")
            print(f"使用数据源: {result.get('source')}")
        else:
            print(f"错误: {result.get('message')}")
    else:
        print(f"请求失败: {response.status_code}")
    
    # 获取美股数据
    print("\n获取美股数据:")
    response = requests.get(f"{API_BASE_URL}/data/stock/AAPL", params={
        "source": "auto",
        "period": "1mo"
    })
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            data = result.get("data", {})
            print(f"公司名称: {data.get('company_name')}")
            print(f"行业: {data.get('industry')}")
            print(f"历史数据条数: {len(data.get('historical_data', []))}")
            print(f"使用数据源: {result.get('source')}")
        else:
            print(f"错误: {result.get('message')}")
    else:
        print(f"请求失败: {response.status_code}")
    
    # 获取市场数据
    print("\n获取市场数据:")
    response = requests.get(f"{API_BASE_URL}/data/market/china")
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            data = result.get("data", {})
            indices = data.get('indices', {})
            for code, index_data in indices.items():
                print(f"{index_data.get('name')}: {index_data.get('last_price')} ({index_data.get('change_percent', 0):.2f}%)")
            print(f"使用数据源: {result.get('source')}")
        else:
            print(f"错误: {result.get('message')}")
    else:
        print(f"请求失败: {response.status_code}")
    
    # 获取行业数据
    print("\n获取行业数据:")
    response = requests.get(f"{API_BASE_URL}/data/industry/医药")
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            data = result.get("data", {})
            stocks = data.get('stocks', [])
            print(f"行业: {data.get('industry')}")
            print(f"成分股数量: {len(stocks)}")
            for i, stock in enumerate(stocks[:5]):
                print(f"  {i+1}. {stock.get('name')} ({stock.get('symbol')}): {stock.get('price')} ({stock.get('change_pct', 0):.2f}%)")
            if len(stocks) > 5:
                print(f"  ... 共{len(stocks)}只股票")
            print(f"使用数据源: {result.get('source')}")
        else:
            print(f"错误: {result.get('message')}")
    else:
        print(f"请求失败: {response.status_code}")

def example_compare_sources():
    """示例：比较不同数据源的数据"""
    print_separator("比较不同数据源的数据")
    
    # 创建数据源选择器
    selector = DataSourceSelector()
    
    # 获取同一只股票的数据（中国平安，同时在A股和港股上市）
    symbol_a = "601318"  # A股代码
    symbol_hk = "2318.HK"  # 港股代码
    
    print(f"比较中国平安的A股和港股数据:")
    
    # 获取A股数据（使用AKShare）
    data_akshare = selector.get_stock_data(symbol_a, source="akshare")
    
    # 获取港股数据（使用Yahoo）
    data_yahoo = selector.get_stock_data(symbol_hk, source="yahoo")
    
    if "error" not in data_akshare and "error" not in data_yahoo:
        # 打印基本信息比较
        print("\n基本信息比较:")
        print(f"{'数据项':<15} {'AKShare (A股)':<20} {'Yahoo (港股)':<20}")
        print("-" * 60)
        print(f"{'公司名称':<15} {data_akshare.get('company_name'):<20} {data_yahoo.get('company_name'):<20}")
        print(f"{'行业':<15} {data_akshare.get('industry'):<20} {data_yahoo.get('industry'):<20}")
        print(f"{'市场':<15} {data_akshare.get('market'):<20} {data_yahoo.get('market'):<20}")
        
        # 比较最近的价格数据
        akshare_hist = data_akshare.get('historical_data', [])
        yahoo_hist = data_yahoo.get('historical_data', [])
        
        if akshare_hist and yahoo_hist:
            print("\n最近价格数据比较:")
            print(f"{'日期':<15} {'A股收盘价':<15} {'港股收盘价(HKD)':<20} {'换算(CNY)':<15}")
            print("-" * 70)
            
            # 假设汇率为1港币=0.9人民币
            exchange_rate = 0.9
            
            for i in range(min(5, len(akshare_hist), len(yahoo_hist))):
                a_data = akshare_hist[i]
                y_data = yahoo_hist[i]
                
                a_date = a_data.get('date')
                a_close = a_data.get('close')
                y_date = y_data.get('date')
                y_close = y_data.get('close')
                y_close_cny = y_close * exchange_rate if y_close else None
                
                print(f"{a_date:<15} {a_close:<15.2f} {y_close:<20.2f} {y_close_cny:<15.2f}")
    else:
        if "error" in data_akshare:
            print(f"AKShare错误: {data_akshare.get('error')}")
        if "error" in data_yahoo:
            print(f"Yahoo错误: {data_yahoo.get('error')}")

def main():
    """主函数"""
    print("🚀 数据源选择示例\n")
    
    try:
        # 运行示例
        example_direct_usage()
        
        # 判断API是否可用
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                example_api_usage()
            else:
                print("\n⚠️ API服务不可用，跳过API示例")
        except requests.exceptions.RequestException:
            print("\n⚠️ API服务不可用，跳过API示例")
        
        example_compare_sources()
        
        print("\n✅ 所有示例执行完成！")
    except Exception as e:
        print(f"\n❌ 示例执行出错: {e}")

if __name__ == "__main__":
    main()