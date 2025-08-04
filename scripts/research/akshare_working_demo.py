#!/usr/bin/env python3
"""
AKShare工作演示
使用正确的API获取实时数据
"""

import akshare as ak
import pandas as pd
from typing import List, Dict, Any
import time

def get_ashare_stocks():
    """获取A股所有股票列表"""
    try:
        print("🔍 正在获取A股股票列表...")
        # 获取A股实时行情
        df = ak.stock_zh_a_spot_em()
        print(f"✅ 成功获取 {len(df)} 只A股股票")
        return df
    except Exception as e:
        print(f"❌ 获取A股股票列表失败: {e}")
        return pd.DataFrame()

def get_stock_industry_info():
    """获取股票行业信息"""
    try:
        print("🔍 正在获取股票行业信息...")
        # 获取申万一级行业分类
        df = ak.stock_sector_detail(sector="申万一级")
        print(f"✅ 成功获取 {len(df)} 只股票的行业信息")
        return df
    except Exception as e:
        print(f"❌ 获取行业信息失败: {e}")
        return pd.DataFrame()

def get_companies_by_industry(industry: str) -> List[Dict[str, Any]]:
    """
    根据行业筛选公司
    """
    print(f"🔍 正在筛选 {industry} 行业的公司...")
    
    try:
        # 获取所有A股股票
        stocks_df = get_ashare_stocks()
        if stocks_df.empty:
            return []
        
        # 获取行业信息
        industry_df = get_stock_industry_info()
        if industry_df.empty:
            return []
        
        # 合并数据
        merged_df = pd.merge(stocks_df, industry_df, left_on='代码', right_on='代码', how='inner')
        
        # 筛选指定行业
        industry_stocks = merged_df[merged_df['行业'] == industry]
        
        # 转换为标准格式
        companies = []
        for _, row in industry_stocks.iterrows():
            company = {
                "code": row.get('代码', ''),
                "name": row.get('名称', ''),
                "industry": industry,
                "market": "A股",
                "source": "AKShare实时获取",
                "current_price": row.get('最新价', 0),
                "change_percent": row.get('涨跌幅', 0),
                "volume": row.get('成交量', 0),
                "turnover": row.get('成交额', 0),
                "market_cap": row.get('总市值', 0)
            }
            companies.append(company)
        
        print(f"✅ 找到 {len(companies)} 家 {industry} 行业公司")
        return companies
        
    except Exception as e:
        print(f"❌ 筛选 {industry} 行业公司失败: {e}")
        return []

def get_stock_detail(symbol: str) -> Dict[str, Any]:
    """获取个股详细信息"""
    try:
        print(f"🔍 正在获取 {symbol} 的详细信息...")
        
        # 获取个股基本信息
        stock_info = ak.stock_individual_info_em(symbol=symbol)
        
        # 获取实时行情
        stock_quote = ak.stock_zh_a_spot_em()
        stock_data = stock_quote[stock_quote['代码'] == symbol]
        
        if not stock_data.empty:
            return {
                "code": symbol,
                "name": stock_info.get('股票简称', ''),
                "current_price": stock_data.iloc[0].get('最新价', 0),
                "change_percent": stock_data.iloc[0].get('涨跌幅', 0),
                "volume": stock_data.iloc[0].get('成交量', 0),
                "turnover": stock_data.iloc[0].get('成交额', 0),
                "market_cap": stock_data.iloc[0].get('总市值', 0),
                "pe_ratio": stock_data.iloc[0].get('市盈率', 0),
                "pb_ratio": stock_data.iloc[0].get('市净率', 0)
            }
        else:
            return {"code": symbol, "error": "未找到行情数据"}
            
    except Exception as e:
        return {"code": symbol, "error": str(e)}

def demonstrate_akshare_features():
    """演示AKShare功能"""
    print("=== AKShare功能演示 ===\n")
    
    # 1. 获取A股股票列表
    stocks_df = get_ashare_stocks()
    if not stocks_df.empty:
        print("📊 A股股票示例（前5只）:")
        for i, (_, row) in enumerate(stocks_df.head().iterrows()):
            print(f"   {i+1}. {row['代码']}: {row['名称']} "
                  f"(价格: {row.get('最新价', 'N/A')} "
                  f"涨跌幅: {row.get('涨跌幅', 'N/A')}%)")
        print()
    
    # 2. 获取行业信息
    industry_df = get_stock_industry_info()
    if not industry_df.empty:
        print("📈 行业分布示例:")
        industry_counts = industry_df['行业'].value_counts()
        for industry, count in industry_counts.head(10).items():
            print(f"   {industry}: {count} 家公司")
        print()
    
    # 3. 测试获取特定行业的公司
    test_industries = ["医药生物", "电子", "电气设备"]
    
    for industry in test_industries:
        print(f"🔍 获取 {industry} 行业公司:")
        companies = get_companies_by_industry(industry)
        
        if companies:
            print(f"   找到 {len(companies)} 家公司:")
            # 显示前3家公司
            for i, company in enumerate(companies[:3]):
                print(f"   {i+1}. {company['code']}: {company['name']} "
                      f"(价格: {company.get('current_price', 'N/A')} "
                      f"涨跌幅: {company.get('change_percent', 'N/A')}%)")
            
            if len(companies) > 3:
                print(f"   ... 还有 {len(companies) - 3} 家公司")
        else:
            print(f"   未找到 {industry} 行业的公司")
        
        print("-" * 50)

def show_api_integration():
    """展示API集成方案"""
    print("\n=== API集成方案 ===\n")
    
    integration_code = '''
# 实时数据API端点
@router.get("/companies/realtime/{industry}")
def get_companies_realtime(industry: str):
    """实时获取指定行业的公司"""
    try:
        # 1. 从AKShare获取数据
        companies = get_companies_by_industry(industry)
        
        # 2. 转换为API响应格式
        response_data = []
        for company in companies:
            response_data.append({
                "code": company["code"],
                "name": company["name"],
                "industry": company["industry"],
                "market": company["market"],
                "current_price": company["current_price"],
                "change_percent": company["change_percent"],
                "source": "AKShare实时获取"
            })
        
        return response_data
        
    except Exception as e:
        # 3. 降级到本地存储
        return get_local_companies(industry)

# 个股详情API
@router.get("/stocks/{symbol}/detail")
def get_stock_detail_api(symbol: str):
    """获取个股详细信息"""
    try:
        detail = get_stock_detail(symbol)
        if "error" not in detail:
            return detail
        else:
            raise HTTPException(status_code=404, detail=detail["error"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 定时更新任务
@schedule.scheduled_job("cron", hour=9, minute=30)
def update_daily_market_data():
    """每天开盘后更新市场数据"""
    industries = ["医药生物", "电子", "电气设备", "计算机", "通信"]
    
    for industry in industries:
        try:
            companies = get_companies_by_industry(industry)
            # 保存到本地存储
            save_industry_companies(industry, companies)
            print(f"✅ 更新 {industry} 行业数据: {len(companies)} 家公司")
        except Exception as e:
            print(f"❌ 更新 {industry} 行业数据失败: {e}")
    '''
    
    print("API集成代码示例:")
    print(integration_code)

def main():
    """主函数"""
    print("🚀 AKShare实时数据获取演示\n")
    
    # 演示功能
    demonstrate_akshare_features()
    
    # 展示集成方案
    show_api_integration()
    
    print("\n💡 实现建议:")
    print("1. ✅ AKShare已安装并可用")
    print("2. 🔄 可以获取实时A股数据")
    print("3. 📊 支持按行业筛选公司")
    print("4. ⚡ 可以集成到现有API中")
    print("5. 🕐 建议添加定时更新任务")

if __name__ == "__main__":
    main() 