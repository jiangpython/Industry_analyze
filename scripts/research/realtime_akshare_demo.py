#!/usr/bin/env python3
"""
AKShare实时数据获取演示
展示如何从AKShare获取实时数据
"""

import akshare as ak
import pandas as pd
from typing import List, Dict, Any
import time

def get_ashare_companies_by_industry(industry: str) -> List[Dict[str, Any]]:
    """
    使用AKShare获取A股指定行业的公司
    """
    print(f"🔍 正在从AKShare获取 {industry} 行业的A股公司...")
    
    try:
        # 方法1：获取申万一级行业成分股
        if industry == "医药":
            # 获取申万医药生物行业成分股
            df = ak.stock_board_industry_cons_sw(symbol="医药生物")
        elif industry == "新能源":
            # 获取申万电气设备行业成分股（包含新能源）
            df = ak.stock_board_industry_cons_sw(symbol="电气设备")
        elif industry == "半导体":
            # 获取申万电子行业成分股
            df = ak.stock_board_industry_cons_sw(symbol="电子")
        else:
            print(f"⚠️ 未找到 {industry} 对应的申万行业分类")
            return []
        
        # 转换为标准格式
        companies = []
        for _, row in df.iterrows():
            company = {
                "code": row.get('代码', ''),
                "name": row.get('名称', ''),
                "industry": industry,
                "market": "A股",
                "source": "AKShare实时获取",
                "current_price": row.get('最新价', 0),
                "change_percent": row.get('涨跌幅', 0)
            }
            companies.append(company)
        
        print(f"✅ 成功获取 {len(companies)} 家 {industry} 行业公司")
        return companies
        
    except Exception as e:
        print(f"❌ 获取 {industry} 行业数据失败: {e}")
        return []

def get_stock_basic_info(symbol: str) -> Dict[str, Any]:
    """
    获取个股基本信息
    """
    try:
        # 获取股票基本信息
        stock_info = ak.stock_individual_info_em(symbol=symbol)
        
        # 获取实时行情
        stock_quote = ak.stock_zh_a_spot_em()
        stock_quote = stock_quote[stock_quote['代码'] == symbol]
        
        if not stock_quote.empty:
            return {
                "code": symbol,
                "name": stock_info.get('股票简称', ''),
                "current_price": stock_quote.iloc[0].get('最新价', 0),
                "change_percent": stock_quote.iloc[0].get('涨跌幅', 0),
                "volume": stock_quote.iloc[0].get('成交量', 0),
                "market_cap": stock_quote.iloc[0].get('总市值', 0)
            }
        else:
            return {"code": symbol, "error": "未找到行情数据"}
            
    except Exception as e:
        return {"code": symbol, "error": str(e)}

def get_industry_analysis(industry: str) -> Dict[str, Any]:
    """
    获取行业分析数据
    """
    try:
        # 获取行业指数数据
        if industry == "医药":
            index_code = "801150"  # 申万医药生物指数
        elif industry == "新能源":
            index_code = "801730"  # 申万电气设备指数
        elif industry == "半导体":
            index_code = "801080"  # 申万电子指数
        else:
            return {"error": f"未找到 {industry} 对应的指数"}
        
        # 获取指数行情
        index_data = ak.stock_zh_index_spot()
        index_info = index_data[index_data['代码'] == index_code]
        
        if not index_info.empty:
            return {
                "industry": industry,
                "index_code": index_code,
                "index_name": index_info.iloc[0].get('名称', ''),
                "current_value": index_info.iloc[0].get('最新价', 0),
                "change_percent": index_info.iloc[0].get('涨跌幅', 0),
                "volume": index_info.iloc[0].get('成交量', 0),
                "turnover": index_info.iloc[0].get('成交额', 0),
                "source": "AKShare实时获取"
            }
        else:
            return {"error": "未找到指数数据"}
            
    except Exception as e:
        return {"error": str(e)}

def demonstrate_realtime_akshare():
    """演示AKShare实时数据获取"""
    print("=== AKShare实时数据获取演示 ===\n")
    
    # 测试获取不同行业的公司
    industries = ["医药", "新能源", "半导体"]
    
    for industry in industries:
        print(f"📊 获取 {industry} 行业A股公司:")
        companies = get_ashare_companies_by_industry(industry)
        
        if companies:
            print(f"   找到 {len(companies)} 家公司:")
            # 显示前5家公司
            for i, company in enumerate(companies[:5]):
                print(f"   {i+1}. {company['code']}: {company['name']} "
                      f"(价格: {company.get('current_price', 'N/A')} "
                      f"涨跌幅: {company.get('change_percent', 'N/A')}%)")
            
            if len(companies) > 5:
                print(f"   ... 还有 {len(companies) - 5} 家公司")
        else:
            print(f"   未找到 {industry} 行业的公司")
        
        print()
        
        # 获取行业分析数据
        print(f"📈 获取 {industry} 行业分析:")
        analysis = get_industry_analysis(industry)
        if "error" not in analysis:
            print(f"   指数: {analysis.get('index_name', '')} ({analysis.get('index_code', '')})")
            print(f"   当前值: {analysis.get('current_value', 'N/A')}")
            print(f"   涨跌幅: {analysis.get('change_percent', 'N/A')}%")
            print(f"   成交量: {analysis.get('volume', 'N/A')}")
        else:
            print(f"   ❌ {analysis['error']}")
        
        print("-" * 50)

def show_akshare_integration():
    """展示如何集成到API中"""
    print("\n=== 集成到API的方案 ===\n")
    
    integration_code = '''
# 在API端点中集成AKShare
@router.get("/companies/realtime/{industry}")
def get_companies_realtime(industry: str):
    """实时获取指定行业的公司"""
    try:
        # 1. 从AKShare获取A股数据
        ashare_companies = get_ashare_companies_by_industry(industry)
        
        # 2. 从Yahoo Finance获取美股数据（可选）
        # yahoo_companies = get_yahoo_companies_by_industry(industry)
        
        # 3. 合并数据
        all_companies = ashare_companies  # + yahoo_companies
        
        # 4. 保存到本地缓存（可选）
        save_to_cache(industry, all_companies)
        
        return all_companies
        
    except Exception as e:
        # 5. 降级到本地存储
        return get_local_companies(industry)

# 定时更新数据
@schedule.scheduled_job("cron", hour=9, minute=30)
def update_daily_data():
    """每天开盘后更新数据"""
    industries = ["医药", "新能源", "半导体"]
    for industry in industries:
        companies = get_ashare_companies_by_industry(industry)
        save_to_local_storage(industry, companies)
    '''
    
    print("API集成代码示例:")
    print(integration_code)

def main():
    """主函数"""
    print("🚀 AKShare实时数据获取演示\n")
    
    # 演示实时数据获取
    demonstrate_realtime_akshare()
    
    # 展示集成方案
    show_akshare_integration()
    
    print("\n💡 使用建议:")
    print("1. 需要安装AKShare: pip install akshare")
    print("2. 网络环境要求：需要能访问AKShare数据源")
    print("3. 数据更新频率：建议每天开盘后更新")
    print("4. 错误处理：需要降级到本地存储")
    print("5. 性能优化：可以添加缓存机制")

if __name__ == "__main__":
    main() 