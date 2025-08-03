"""
基础测试文件
"""

import pytest
from app.core.config import settings
from app.utils.helpers import validate_stock_code, format_stock_code, classify_industry


def test_config():
    """测试配置加载"""
    assert settings.DATABASE_URL is not None
    assert settings.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR"]


def test_stock_code_validation():
    """测试股票代码验证"""
    # 有效的股票代码
    assert validate_stock_code("000001") == True
    assert validate_stock_code("600000") == True
    assert validate_stock_code("300001") == True
    
    # 无效的股票代码
    assert validate_stock_code("00001") == False  # 5位
    assert validate_stock_code("0000001") == False  # 7位
    assert validate_stock_code("00000a") == False  # 包含字母
    assert validate_stock_code("") == False  # 空字符串


def test_stock_code_formatting():
    """测试股票代码格式化"""
    assert format_stock_code("000001") == "SZ000001"
    assert format_stock_code("600000") == "SH600000"
    assert format_stock_code("300001") == "SZ300001"
    assert format_stock_code("invalid") == "invalid"  # 无效代码保持不变


def test_industry_classification():
    """测试行业分类"""
    # 医药行业
    assert classify_industry("恒瑞医药") == "医药"
    assert classify_industry("生物制药公司") == "医药"
    
    # 新能源行业
    assert classify_industry("比亚迪") == "新能源"
    assert classify_industry("光伏科技") == "新能源"
    
    # 半导体行业
    assert classify_industry("中芯国际") == "半导体"
    assert classify_industry("集成电路公司") == "半导体"
    
    # 芯片行业
    assert classify_industry("华为海思") == "芯片"
    assert classify_industry("处理器公司") == "芯片"
    
    # 其他行业
    assert classify_industry("银行") == "其他"


if __name__ == "__main__":
    # 运行测试
    test_config()
    test_stock_code_validation()
    test_stock_code_formatting()
    test_industry_classification()
    print("✅ 所有测试通过！") 