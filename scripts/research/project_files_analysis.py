#!/usr/bin/env python3
"""
项目文件分析脚本
分析根目录下各个脚本文件的作用
"""

import os
import re
from typing import Dict, List, Any

def analyze_project_files():
    """分析项目文件"""
    print("🔍 项目文件分析")
    print("=" * 60)
    
    # 定义文件分类
    file_categories = {
        "核心运行文件": [
            "run.py",  # 主启动文件
            "requirements.txt",  # 依赖文件
        ],
        "配置管理文件": [
            "config_manager.py",  # 配置管理器
            "setup_config.py",  # 配置设置
        ],
        "文档文件": [
            "README.md",  # 项目说明
            "INSTALL.md",  # 安装说明
            "DEPLOYMENT.md",  # 部署说明
            "akshare_detailed_analysis.md",  # AKShare分析文档
        ],
        "测试和演示文件": [
            "test_api.py",  # API测试
            "test_realtime_api.py",  # 实时API测试
            "test_optimization.py",  # 优化测试
            "add_test_data.py",  # 添加测试数据
        ],
        "AKShare研究文件": [
            "akshare_methods_research.py",  # AKShare方法研究
            "akshare_simple_research.py",  # AKShare简化研究
            "akshare_working_demo.py",  # AKShare工作演示
            "realtime_akshare_demo.py",  # 实时AKShare演示
        ],
        "数据演示文件": [
            "realtime_usage_demo.py",  # 实时使用演示
            "real_time_data_demo.py",  # 实时数据演示
            "incremental_demo.py",  # 增量数据演示
            "example_local_storage.py",  # 本地存储示例
        ],
        "目录结构": [
            "app/",  # 主应用目录
            "data/",  # 数据目录
            "logs/",  # 日志目录
            "tests/",  # 测试目录
            "examples/",  # 示例目录
            ".venv/",  # 虚拟环境
        ],
        "其他文件": [
            ".gitignore",  # Git忽略文件
            ".git/",  # Git版本控制
            ".idea/",  # IDE配置
        ]
    }
    
    # 分析每个分类
    for category, files in file_categories.items():
        print(f"\n📁 {category}:")
        for file in files:
            if os.path.exists(file):
                if os.path.isdir(file):
                    print(f"   📂 {file}/ - 目录")
                else:
                    size = os.path.getsize(file)
                    print(f"   📄 {file} - {size} bytes")
            else:
                print(f"   ❌ {file} - 不存在")
    
    print("\n🎯 核心运行相关文件:")
    print("=" * 40)
    
    core_files = [
        ("run.py", "主启动文件，启动FastAPI服务器"),
        ("requirements.txt", "Python依赖包列表"),
        ("config_manager.py", "配置管理器，处理系统配置"),
        ("setup_config.py", "配置设置脚本"),
        ("app/main.py", "FastAPI主应用文件"),
        ("app/api/endpoints/", "API端点目录"),
        ("app/services/", "服务层目录"),
        ("app/utils/", "工具类目录"),
    ]
    
    for file, description in core_files:
        if os.path.exists(file):
            print(f"   ✅ {file} - {description}")
        else:
            print(f"   ❌ {file} - {description} (不存在)")
    
    print("\n🔧 测试和演示文件:")
    print("=" * 40)
    
    test_files = [
        ("test_api.py", "API功能测试"),
        ("test_realtime_api.py", "实时API测试"),
        ("test_optimization.py", "缓存优化测试"),
        ("add_test_data.py", "添加测试数据"),
    ]
    
    for file, description in test_files:
        if os.path.exists(file):
            print(f"   ✅ {file} - {description}")
        else:
            print(f"   ❌ {file} - {description} (不存在)")
    
    print("\n📚 研究文档文件:")
    print("=" * 40)
    
    doc_files = [
        ("akshare_detailed_analysis.md", "AKShare详细分析报告"),
        ("README.md", "项目说明文档"),
        ("INSTALL.md", "安装指南"),
        ("DEPLOYMENT.md", "部署指南"),
    ]
    
    for file, description in doc_files:
        if os.path.exists(file):
            print(f"   ✅ {file} - {description}")
        else:
            print(f"   ❌ {file} - {description} (不存在)")
    
    print("\n🎯 文件作用总结:")
    print("=" * 40)
    print("1. 核心运行文件:")
    print("   - run.py: 项目主启动文件")
    print("   - requirements.txt: 依赖管理")
    print("   - config_manager.py: 配置管理")
    print("   - app/: 主应用代码")
    
    print("\n2. 测试和演示文件:")
    print("   - test_*.py: 各种测试脚本")
    print("   - *_demo.py: 功能演示脚本")
    print("   - akshare_*_research.py: AKShare研究脚本")
    
    print("\n3. 文档文件:")
    print("   - *.md: 项目文档和说明")
    print("   - akshare_detailed_analysis.md: 详细技术分析")
    
    print("\n4. 数据文件:")
    print("   - data/: 数据存储目录")
    print("   - logs/: 日志目录")
    print("   - add_test_data.py: 测试数据生成")

def check_file_dependencies():
    """检查文件依赖关系"""
    print("\n🔗 文件依赖关系分析:")
    print("=" * 40)
    
    dependencies = {
        "run.py": ["app.main", "uvicorn"],
        "app/main.py": ["app.api.endpoints", "app.services", "app.utils"],
        "app/api/endpoints/companies_simple.py": ["app.services.realtime_data_service", "app.utils.data_manager"],
        "app/services/realtime_data_service.py": ["akshare", "app.utils.data_manager"],
        "test_api.py": ["requests", "app.main"],
        "test_optimization.py": ["requests", "time"],
    }
    
    for file, deps in dependencies.items():
        if os.path.exists(file):
            print(f"   📄 {file}:")
            for dep in deps:
                print(f"      - 依赖: {dep}")
        else:
            print(f"   ❌ {file}: 文件不存在")

def main():
    """主函数"""
    print("🚀 项目文件分析")
    print("=" * 80)
    
    analyze_project_files()
    check_file_dependencies()
    
    print("\n📋 总结:")
    print("1. 核心运行文件: run.py, requirements.txt, app/目录")
    print("2. 测试文件: test_*.py 系列文件")
    print("3. 演示文件: *_demo.py 系列文件")
    print("4. 研究文件: akshare_*_research.py 系列文件")
    print("5. 文档文件: *.md 系列文件")
    print("\n这些文件都是项目开发和运行的重要组成部分，但只有核心运行文件是项目运行必需的。")

if __name__ == "__main__":
    main() 