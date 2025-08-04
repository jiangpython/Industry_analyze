#!/usr/bin/env python3
"""
行业映射工具
支持行业别名和模糊匹配
"""

import re
from typing import Dict, List, Optional


class IndustryMapper:
    """行业映射器"""
    
    # 行业别名映射
    INDUSTRY_ALIASES = {
        # 医药行业
        "医药": ["医药", "生物医药", "医疗器械", "医疗服务", "制药", "生物技术"],
        "生物医药": ["医药", "生物医药", "医疗器械", "医疗服务", "制药", "生物技术"],
        "医疗器械": ["医药", "生物医药", "医疗器械", "医疗服务", "制药", "生物技术"],
        "医疗服务": ["医药", "生物医药", "医疗器械", "医疗服务", "制药", "生物技术"],
        
        # 新能源行业
        "新能源": ["新能源", "光伏", "风电", "储能", "新能源汽车", "清洁能源", "可再生能源"],
        "光伏": ["新能源", "光伏", "风电", "储能", "新能源汽车", "清洁能源", "可再生能源"],
        "风电": ["新能源", "光伏", "风电", "储能", "新能源汽车", "清洁能源", "可再生能源"],
        "储能": ["新能源", "光伏", "风电", "储能", "新能源汽车", "清洁能源", "可再生能源"],
        "新能源汽车": ["新能源", "光伏", "风电", "储能", "新能源汽车", "清洁能源", "可再生能源"],
        
        # 半导体行业
        "半导体": ["半导体", "芯片", "集成电路", "电子元件", "微电子", "IC"],
        "芯片": ["半导体", "芯片", "集成电路", "电子元件", "微电子", "IC"],
        "集成电路": ["半导体", "芯片", "集成电路", "电子元件", "微电子", "IC"],
        "电子元件": ["半导体", "芯片", "集成电路", "电子元件", "微电子", "IC"],
    }
    
    # 标准行业名称
    STANDARD_INDUSTRIES = {
        "医药": "医药",
        "新能源": "新能源", 
        "半导体": "半导体",
        "芯片": "半导体"  # 芯片映射到半导体
    }
    
    @classmethod
    def map_industry(cls, input_industry: str) -> Optional[str]:
        """
        将输入的行业名称映射到标准行业名称
        
        Args:
            input_industry: 输入的行业名称
            
        Returns:
            标准行业名称，如果无法映射则返回None
        """
        # 清理输入
        cleaned_input = input_industry.strip().lower()
        
        # 1. 直接匹配
        if cleaned_input in cls.STANDARD_INDUSTRIES:
            return cls.STANDARD_INDUSTRIES[cleaned_input]
        
        # 2. 别名匹配
        for standard_name, aliases in cls.INDUSTRY_ALIASES.items():
            if cleaned_input in [alias.lower() for alias in aliases]:
                return standard_name
        
        # 3. 模糊匹配
        for standard_name, aliases in cls.INDUSTRY_ALIASES.items():
            for alias in aliases:
                if cls._fuzzy_match(cleaned_input, alias.lower()):
                    return standard_name
        
        return None
    
    @classmethod
    def _fuzzy_match(cls, input_text: str, target_text: str) -> bool:
        """
        模糊匹配算法
        
        Args:
            input_text: 输入文本
            target_text: 目标文本
            
        Returns:
            是否匹配
        """
        # 简单的包含匹配
        if input_text in target_text or target_text in input_text:
            return True
        
        # 关键词匹配
        keywords = input_text.split()
        target_keywords = target_text.split()
        
        # 检查是否有共同关键词
        common_keywords = set(keywords) & set(target_keywords)
        if len(common_keywords) > 0:
            return True
        
        return False
    
    @classmethod
    def get_suggestions(cls, input_industry: str) -> List[str]:
        """
        获取行业建议
        
        Args:
            input_industry: 输入的行业名称
            
        Returns:
            建议的行业名称列表
        """
        suggestions = []
        cleaned_input = input_industry.strip().lower()
        
        for standard_name, aliases in cls.INDUSTRY_ALIASES.items():
            # 检查是否包含输入的关键词
            for alias in aliases:
                if cleaned_input in alias.lower() or alias.lower() in cleaned_input:
                    suggestions.append(standard_name)
                    break
        
        return list(set(suggestions))
    
    @classmethod
    def get_all_industries(cls) -> List[str]:
        """
        获取所有支持的行业
        
        Returns:
            行业名称列表
        """
        return list(cls.STANDARD_INDUSTRIES.keys())


# 使用示例
if __name__ == "__main__":
    mapper = IndustryMapper()
    
    # 测试映射
    test_cases = [
        "医药", "生物医药", "光伏", "芯片", "集成电路", 
        "新能源", "半导体", "医疗器械", "储能"
    ]
    
    print("=== 行业映射测试 ===")
    for test_case in test_cases:
        mapped = mapper.map_industry(test_case)
        suggestions = mapper.get_suggestions(test_case)
        print(f"输入: {test_case} -> 映射: {mapped} | 建议: {suggestions}")
    
    print(f"\n所有支持的行业: {mapper.get_all_industries()}") 