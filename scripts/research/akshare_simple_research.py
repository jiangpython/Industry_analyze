#!/usr/bin/env python3
"""
AKShare数据获取方法简化研究
专注于实际可用的方法
"""

import akshare as ak
import pandas as pd
import time
from typing import List, Dict, Any

def research_available_methods():
    """研究可用的AKShare方法"""
    print("🔍 AKShare可用方法研究")
    print("=" * 60)
    
    # 测试单个股票数据获取
    print("1. 单个股票数据获取方法:")
    test_symbol = "000001"
    
    # 方法1: 个股基本信息
    print("   a) 个股基本信息 (ak.stock_individual_info_em):")
    try:
        start_time = time.time()
        stock_info = ak.stock_individual_info_em(symbol=test_symbol)
        end_time = time.time()
        print(f"      ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"      数据量: {len(stock_info)} 条记录")
        if not stock_info.empty:
            print(f"      字段: {list(stock_info.columns)}")
            # 显示部分数据
            for _, row in stock_info.iterrows():
                print(f"      {row['item']}: {row['value']}")
    except Exception as e:
        print(f"      ❌ 失败: {e}")
    
    print()
    
    # 方法2: 历史数据
    print("   b) 历史数据 (ak.stock_zh_a_hist):")
    try:
        start_time = time.time()
        hist_data = ak.stock_zh_a_hist(symbol=test_symbol, period="daily", start_date="20240101", end_date="20240115")
        end_time = time.time()
        print(f"      ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"      数据量: {len(hist_data)} 条记录")
        if not hist_data.empty:
            print(f"      字段: {list(hist_data.columns)}")
            print(f"      最新数据: {hist_data.iloc[-1].to_dict()}")
    except Exception as e:
        print(f"      ❌ 失败: {e}")
    
    print()
    
    # 方法3: 财务数据
    print("   c) 财务数据 (ak.stock_financial_report_sina):")
    try:
        start_time = time.time()
        financial_data = ak.stock_financial_report_sina(stock=test_symbol, symbol="资产负债表")
        end_time = time.time()
        print(f"      ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"      数据量: {len(financial_data)} 条记录")
        if not financial_data.empty:
            print(f"      字段数: {len(financial_data.columns)}")
            print(f"      最新报告期: {financial_data.iloc[-1].get('报告日', '未知')}")
    except Exception as e:
        print(f"      ❌ 失败: {e}")

def research_industry_methods():
    """研究行业数据获取方法"""
    print("\n2. 行业数据获取方法:")
    
    # 方法1: 行业板块信息
    print("   a) 行业板块信息 (ak.stock_board_industry_name_em):")
    try:
        start_time = time.time()
        industry_names = ak.stock_board_industry_name_em()
        end_time = time.time()
        print(f"      ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"      数据量: {len(industry_names)} 个行业")
        if not industry_names.empty:
            print(f"      字段: {list(industry_names.columns)}")
            # 显示医药相关行业
            medical_industries = industry_names[industry_names['板块名称'].str.contains('医药|医疗|生物', na=False)]
            print(f"      医药相关行业: {list(medical_industries['板块名称']) if not medical_industries.empty else '无'}")
    except Exception as e:
        print(f"      ❌ 失败: {e}")
    
    print()
    
    # 方法2: 尝试获取行业成分股
    print("   b) 尝试获取行业成分股:")
    try:
        # 尝试不同的行业成分股接口
        test_industry = "医药商业"
        print(f"      尝试获取 {test_industry} 成分股...")
        
        # 方法2.1: 使用板块成分股接口
        try:
            start_time = time.time()
            cons_data = ak.stock_board_industry_cons_em(symbol=test_industry)
            end_time = time.time()
            print(f"      ✅ ak.stock_board_industry_cons_em 成功: 耗时 {end_time - start_time:.2f}秒")
            print(f"      数据量: {len(cons_data)} 只股票")
            if not cons_data.empty:
                print(f"      字段: {list(cons_data.columns)}")
                print(f"      前3只股票: {list(cons_data['名称'].head(3))}")
        except Exception as e:
            print(f"      ❌ ak.stock_board_industry_cons_em 失败: {e}")
        
    except Exception as e:
        print(f"      ❌ 失败: {e}")

def research_real_time_methods():
    """研究实时数据获取方法"""
    print("\n3. 实时数据获取方法:")
    
    # 方法1: 尝试获取实时行情
    print("   a) 实时行情数据:")
    try:
        start_time = time.time()
        # 尝试获取实时行情
        realtime_data = ak.stock_zh_a_spot_em()
        end_time = time.time()
        print(f"      ✅ 成功: 耗时 {end_time - start_time:.2f}秒")
        print(f"      数据量: {len(realtime_data)} 只股票")
        if not realtime_data.empty:
            print(f"      字段: {list(realtime_data.columns)}")
            # 显示前3只股票
            print(f"      前3只股票: {list(realtime_data['名称'].head(3))}")
            
            # 测试筛选特定股票
            test_symbol = "000001"
            target_stock = realtime_data[realtime_data['代码'] == test_symbol]
            if not target_stock.empty:
                print(f"      找到目标股票 {test_symbol}: {target_stock.iloc[0]['名称']}")
                print(f"      最新价: {target_stock.iloc[0]['最新价']}")
                print(f"      涨跌幅: {target_stock.iloc[0]['涨跌幅']}%")
    except Exception as e:
        print(f"      ❌ 失败: {e}")

def analyze_data_quality():
    """分析数据质量"""
    print("\n4. 数据质量分析:")
    
    # 分析实时数据质量
    print("   a) 实时数据质量:")
    try:
        realtime_data = ak.stock_zh_a_spot_em()
        if not realtime_data.empty:
            print(f"      总股票数: {len(realtime_data)}")
            print(f"      数据完整性: {realtime_data.isnull().sum().sum()} 个空值")
            print(f"      价格范围: {realtime_data['最新价'].min():.2f} - {realtime_data['最新价'].max():.2f}")
            print(f"      涨跌幅范围: {realtime_data['涨跌幅'].min():.2f}% - {realtime_data['涨跌幅'].max():.2f}%")
            
            # 分析行业分布
            if '所属行业' in realtime_data.columns:
                industry_counts = realtime_data['所属行业'].value_counts()
                print(f"      行业分布: 前5个行业")
                for industry, count in industry_counts.head().items():
                    print(f"        {industry}: {count} 只股票")
    except Exception as e:
        print(f"      ❌ 分析失败: {e}")

def generate_optimization_suggestions():
    """生成优化建议"""
    print("\n📋 优化建议:")
    print("=" * 60)
    
    print("1. 单个股票数据获取策略:")
    print("   ✅ 基本信息: 使用 ak.stock_individual_info_em() - 快速、准确")
    print("   ✅ 实时行情: 使用 ak.stock_zh_a_spot_em() + 筛选 - 需要缓存")
    print("   ✅ 历史数据: 使用 ak.stock_zh_a_hist() - 按需获取")
    print("   ✅ 财务数据: 使用 ak.stock_financial_report_sina() - 数据丰富")
    
    print("\n2. 行业数据获取策略:")
    print("   ✅ 行业列表: 使用 ak.stock_board_industry_name_em() - 获取所有行业")
    print("   ✅ 行业成分股: 使用 ak.stock_board_industry_cons_em() - 直接获取")
    print("   ⚠️  注意: 行业名称需要统一映射")
    
    print("\n3. 性能优化策略:")
    print("   ✅ 实时数据缓存: 5-10分钟缓存所有A股数据")
    print("   ✅ 按需获取: 历史数据和财务数据按需获取")
    print("   ✅ 错误处理: 网络异常时降级到本地数据")
    print("   ✅ 数据验证: 检查数据完整性和有效性")
    
    print("\n4. 数据源选择优先级:")
    print("   1. 实时行情: ak.stock_zh_a_spot_em() (缓存)")
    print("   2. 基本信息: ak.stock_individual_info_em() (直接)")
    print("   3. 历史数据: ak.stock_zh_a_hist() (按需)")
    print("   4. 财务数据: ak.stock_financial_report_sina() (按需)")
    print("   5. 行业数据: ak.stock_board_industry_cons_em() (直接)")

def main():
    """主函数"""
    print("🚀 AKShare数据获取方法研究")
    print("=" * 80)
    
    try:
        research_available_methods()
        research_industry_methods()
        research_real_time_methods()
        analyze_data_quality()
        generate_optimization_suggestions()
        
        print("\n🎯 研究总结:")
        print("1. AKShare提供了丰富的数据接口，但需要合理使用")
        print("2. 实时数据需要获取全部A股数据，建议使用缓存")
        print("3. 行业数据可以通过专门的接口直接获取")
        print("4. 不同接口的数据格式和字段需要统一处理")
        print("5. 建议实现智能降级机制，确保系统稳定性")
        
    except Exception as e:
        print(f"❌ 研究过程中出现错误: {e}")

if __name__ == "__main__":
    main() 