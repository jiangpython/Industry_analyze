#!/usr/bin/env python3
"""
AKShare数据获取方法详细研究
分析不同场景下的数据获取方式和效率
"""

import akshare as ak
import pandas as pd
import time
from typing import List, Dict, Any
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def research_single_stock_methods():
    """研究单个股票数据获取方法"""
    print("🔍 研究单个股票数据获取方法")
    print("=" * 60)
    
    test_symbol = "000001"  # 平安银行
    
    # 方法1: 获取个股基本信息
    print("1. 获取个股基本信息 (ak.stock_individual_info_em)")
    start_time = time.time()
    try:
        stock_info = ak.stock_individual_info_em(symbol=test_symbol)
        end_time = time.time()
        print(f"   ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"   数据量: {len(stock_info)} 条记录")
        print(f"   字段: {list(stock_info.columns) if not stock_info.empty else '无数据'}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    print()
    
    # 方法2: 获取实时行情（从所有A股中筛选）
    print("2. 获取实时行情 (ak.stock_zh_a_spot_em)")
    start_time = time.time()
    try:
        all_stocks = ak.stock_zh_a_spot_em()
        stock_data = all_stocks[all_stocks['代码'] == test_symbol]
        end_time = time.time()
        print(f"   ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"   总数据量: {len(all_stocks)} 只股票")
        print(f"   目标股票: {'找到' if not stock_data.empty else '未找到'}")
        if not stock_data.empty:
            print(f"   股票名称: {stock_data.iloc[0].get('名称', '')}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    print()
    
    # 方法3: 获取历史数据
    print("3. 获取历史数据 (ak.stock_zh_a_hist)")
    start_time = time.time()
    try:
        hist_data = ak.stock_zh_a_hist(symbol=test_symbol, period="daily", start_date="20240101", end_date="20240115")
        end_time = time.time()
        print(f"   ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"   数据量: {len(hist_data)} 条记录")
        print(f"   字段: {list(hist_data.columns) if not hist_data.empty else '无数据'}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    print()
    
    # 方法4: 获取财务数据
    print("4. 获取财务数据 (ak.stock_financial_report_sina)")
    start_time = time.time()
    try:
        financial_data = ak.stock_financial_report_sina(stock=test_symbol, symbol="资产负债表")
        end_time = time.time()
        print(f"   ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"   数据量: {len(financial_data)} 条记录")
        print(f"   字段: {list(financial_data.columns) if not financial_data.empty else '无数据'}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")

def research_industry_methods():
    """研究行业数据获取方法"""
    print("\n🔍 研究行业数据获取方法")
    print("=" * 60)
    
    test_industry = "医药生物"
    
    # 方法1: 获取申万行业成分股
    print("1. 获取申万行业成分股 (ak.stock_board_industry_cons_sw)")
    start_time = time.time()
    try:
        industry_stocks = ak.stock_board_industry_cons_sw(symbol=test_industry)
        end_time = time.time()
        print(f"   ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"   数据量: {len(industry_stocks)} 只股票")
        print(f"   字段: {list(industry_stocks.columns) if not industry_stocks.empty else '无数据'}")
        if not industry_stocks.empty:
            print(f"   前3只股票: {list(industry_stocks['名称'].head(3))}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    print()
    
    # 方法2: 获取行业分类信息
    print("2. 获取行业分类信息 (ak.stock_sector_detail)")
    start_time = time.time()
    try:
        sector_detail = ak.stock_sector_detail(sector="申万一级")
        end_time = time.time()
        print(f"   ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"   数据量: {len(sector_detail)} 只股票")
        print(f"   字段: {list(sector_detail.columns) if not sector_detail.empty else '无数据'}")
        # 筛选目标行业
        target_industry_stocks = sector_detail[sector_detail['行业'] == test_industry]
        print(f"   {test_industry} 行业股票数: {len(target_industry_stocks)}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    print()
    
    # 方法3: 获取行业板块信息
    print("3. 获取行业板块信息 (ak.stock_board_industry_name_em)")
    start_time = time.time()
    try:
        industry_names = ak.stock_board_industry_name_em()
        end_time = time.time()
        print(f"   ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"   数据量: {len(industry_names)} 个行业")
        print(f"   字段: {list(industry_names.columns) if not industry_names.empty else '无数据'}")
        # 查找目标行业
        target_industry = industry_names[industry_names['板块名称'].str.contains('医药', na=False)]
        print(f"   包含'医药'的行业: {list(target_industry['板块名称']) if not target_industry.empty else '无'}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")

def research_efficiency_comparison():
    """研究不同方法的效率对比"""
    print("\n🔍 效率对比研究")
    print("=" * 60)
    
    test_symbols = ["000001", "000002", "300750"]  # 平安银行、万科A、宁德时代
    
    # 方法1: 逐个获取（低效）
    print("1. 逐个获取股票数据（低效方法）:")
    start_time = time.time()
    try:
        for symbol in test_symbols:
            stock_info = ak.stock_individual_info_em(symbol=symbol)
            print(f"   获取 {symbol}: {'成功' if not stock_info.empty else '失败'}")
        end_time = time.time()
        print(f"   总耗时: {end_time - start_time:.2f}秒")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    print()
    
    # 方法2: 批量获取（高效）
    print("2. 批量获取股票数据（高效方法）:")
    start_time = time.time()
    try:
        all_stocks = ak.stock_zh_a_spot_em()
        end_time = time.time()
        print(f"   获取所有A股数据耗时: {end_time - start_time:.2f}秒")
        print(f"   总数据量: {len(all_stocks)} 只股票")
        
        # 从批量数据中筛选目标股票
        for symbol in test_symbols:
            stock_data = all_stocks[all_stocks['代码'] == symbol]
            print(f"   筛选 {symbol}: {'成功' if not stock_data.empty else '失败'}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")

def research_alternative_methods():
    """研究替代方法"""
    print("\n🔍 研究替代方法")
    print("=" * 60)
    
    # 方法1: 使用个股实时行情接口
    print("1. 个股实时行情接口:")
    test_symbol = "000001"
    start_time = time.time()
    try:
        # 尝试使用个股专用接口
        stock_quote = ak.stock_zh_a_spot_em()
        target_stock = stock_quote[stock_quote['代码'] == test_symbol]
        end_time = time.time()
        print(f"   ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"   获取方式: 从 {len(stock_quote)} 只股票中筛选")
        print(f"   是否找到目标股票: {'是' if not target_stock.empty else '否'}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    print()
    
    # 方法2: 使用行业分类接口
    print("2. 行业分类接口:")
    test_industry = "医药生物"
    start_time = time.time()
    try:
        # 获取申万行业分类
        industry_stocks = ak.stock_board_industry_cons_sw(symbol=test_industry)
        end_time = time.time()
        print(f"   ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"   获取方式: 直接获取 {test_industry} 行业成分股")
        print(f"   数据量: {len(industry_stocks)} 只股票")
    except Exception as e:
        print(f"   ❌ 失败: {e}")

def generate_recommendations():
    """生成优化建议"""
    print("\n📋 优化建议")
    print("=" * 60)
    
    print("1. 单个股票数据获取:")
    print("   ✅ 推荐方法: 使用 ak.stock_individual_info_em() 获取基本信息")
    print("   ✅ 推荐方法: 使用 ak.stock_zh_a_spot_em() 获取实时行情（配合缓存）")
    print("   ⚠️  注意: 实时行情需要获取所有A股数据，建议使用缓存机制")
    
    print("\n2. 行业数据获取:")
    print("   ✅ 推荐方法: 使用 ak.stock_board_industry_cons_sw() 获取行业成分股")
    print("   ✅ 推荐方法: 使用 ak.stock_sector_detail() 获取申万行业分类")
    print("   ⚠️  注意: 不同接口返回的行业名称可能不同，需要统一映射")
    
    print("\n3. 性能优化策略:")
    print("   ✅ 使用全局缓存机制，避免重复获取所有A股数据")
    print("   ✅ 缓存时间设置为5-10分钟，平衡实时性和性能")
    print("   ✅ 对于频繁查询的股票，使用本地缓存")
    print("   ✅ 对于行业数据，使用关键词匹配和智能映射")
    
    print("\n4. 数据源选择:")
    print("   ✅ 实时数据: AKShare (ak.stock_zh_a_spot_em)")
    print("   ✅ 历史数据: AKShare (ak.stock_zh_a_hist)")
    print("   ✅ 财务数据: AKShare (ak.stock_financial_report_sina)")
    print("   ✅ 行业分类: AKShare (ak.stock_board_industry_cons_sw)")

def main():
    """主函数"""
    print("🚀 AKShare数据获取方法详细研究")
    print("=" * 80)
    
    # 执行各项研究
    research_single_stock_methods()
    research_industry_methods()
    research_efficiency_comparison()
    research_alternative_methods()
    generate_recommendations()
    
    print("\n🎯 研究总结:")
    print("1. AKShare没有专门的单个股票实时数据接口")
    print("2. 所有实时数据都需要通过 ak.stock_zh_a_spot_em() 获取全部A股数据")
    print("3. 行业数据可以通过专门的行业成分股接口获取")
    print("4. 建议使用缓存机制来优化性能")
    print("5. 不同接口的数据格式和字段可能不同，需要统一处理")

if __name__ == "__main__":
    main() 