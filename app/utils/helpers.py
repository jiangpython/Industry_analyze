import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import pandas as pd

logger = logging.getLogger(__name__)


def ensure_directory(path: str) -> None:
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)


def save_json(data: Dict[str, Any], filepath: str) -> bool:
    """保存JSON数据"""
    try:
        ensure_directory(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"保存JSON文件失败: {e}")
        return False


def load_json(filepath: str) -> Optional[Dict[str, Any]]:
    """加载JSON数据"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"加载JSON文件失败: {e}")
    return None


def save_csv(data: List[Dict[str, Any]], filepath: str) -> bool:
    """保存CSV数据"""
    try:
        ensure_directory(os.path.dirname(filepath))
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        return True
    except Exception as e:
        logger.error(f"保存CSV文件失败: {e}")
        return False


def load_csv(filepath: str) -> Optional[pd.DataFrame]:
    """加载CSV数据"""
    try:
        if os.path.exists(filepath):
            return pd.read_csv(filepath, encoding='utf-8-sig')
    except Exception as e:
        logger.error(f"加载CSV文件失败: {e}")
    return None


def format_number(value: float, decimal_places: int = 2) -> str:
    """格式化数字"""
    if value is None:
        return "0"
    
    if abs(value) >= 1e8:
        return f"{value/1e8:.{decimal_places}f}亿"
    elif abs(value) >= 1e4:
        return f"{value/1e4:.{decimal_places}f}万"
    else:
        return f"{value:.{decimal_places}f}"


def calculate_growth_rate(current: float, previous: float) -> float:
    """计算增长率"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100


def get_date_range(days: int = 30) -> tuple:
    """获取日期范围"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def validate_stock_code(code: str) -> bool:
    """验证股票代码格式"""
    if not code:
        return False
    
    # 移除可能的前缀
    code = code.upper().replace('SH', '').replace('SZ', '')
    
    # 检查是否为6位数字
    if len(code) != 6 or not code.isdigit():
        return False
    
    return True


def format_stock_code(code: str) -> str:
    """格式化股票代码"""
    if not validate_stock_code(code):
        return code
    
    code = code.upper()
    
    # 根据代码判断市场
    if code.startswith('6'):
        return f"SH{code}"
    else:
        return f"SZ{code}"


def extract_industry_keywords(text: str) -> List[str]:
    """提取行业关键词"""
    keywords = []
    
    # 医药行业关键词
    medical_keywords = ['医药', '生物', '制药', '医疗器械', '医疗服务', '中药', '西药']
    # 新能源行业关键词
    new_energy_keywords = ['新能源', '光伏', '风电', '储能', '新能源汽车', '电池', '充电桩']
    # 半导体行业关键词
    semiconductor_keywords = ['半导体', '芯片', '集成电路', 'IC', '晶圆', '封装']
    # 芯片行业关键词
    chip_keywords = ['芯片', '处理器', 'CPU', 'GPU', '存储芯片', '传感器']
    
    all_keywords = medical_keywords + new_energy_keywords + semiconductor_keywords + chip_keywords
    
    for keyword in all_keywords:
        if keyword in text:
            keywords.append(keyword)
    
    return list(set(keywords))


def classify_industry(company_name: str, description: str = "") -> str:
    """根据公司名称和描述分类行业"""
    text = f"{company_name} {description}".lower()
    
    # 医药行业
    medical_indicators = ['医药', '生物', '制药', '医疗器械', '医疗服务', '中药', '西药', '医院', '诊所']
    # 新能源行业
    new_energy_indicators = ['新能源', '光伏', '风电', '储能', '新能源汽车', '电池', '充电桩', '太阳能', '风能']
    # 半导体行业
    semiconductor_indicators = ['半导体', '集成电路', 'IC', '晶圆', '封装', '晶圆厂']
    # 芯片行业
    chip_indicators = ['芯片', '处理器', 'CPU', 'GPU', '存储芯片', '传感器', '微处理器']
    
    # 计算匹配度
    scores = {
        '医药': sum(1 for indicator in medical_indicators if indicator in text),
        '新能源': sum(1 for indicator in new_energy_indicators if indicator in text),
        '半导体': sum(1 for indicator in semiconductor_indicators if indicator in text),
        '芯片': sum(1 for indicator in chip_indicators if indicator in text)
    }
    
    # 返回得分最高的行业
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    
    return "其他"


def safe_float(value: Any, default: float = 0.0) -> float:
    """安全转换为浮点数"""
    if value is None:
        return default
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """安全转换为整数"""
    if value is None:
        return default
    
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def clean_text(text: str) -> str:
    """清理文本"""
    if not text:
        return ""
    
    # 移除多余的空白字符
    text = ' '.join(text.split())
    
    # 移除特殊字符
    import re
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
    
    return text.strip() 