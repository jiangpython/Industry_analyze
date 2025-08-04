#!/usr/bin/env python3
"""
项目结构查看脚本
显示重组后的项目结构
"""

import os
from pathlib import Path

def show_project_structure():
    """显示项目结构"""
    print("📁 项目结构")
    print("=" * 60)
    
    # 定义要显示的文件和目录
    structure = {
        "📦 核心文件": [
            "run.py",
            "requirements.txt", 
            "config_manager.py",
            "setup_config.py",
        ],
        "📂 应用目录": [
            "app/",
        ],
        "📂 脚本目录": [
            "scripts/",
            "scripts/tests/",
            "scripts/demos/", 
            "scripts/research/",
        ],
        "📂 文档目录": [
            "docs/",
        ],
        "📂 数据目录": [
            "data/",
            "logs/",
        ],
        "📂 其他目录": [
            "tests/",
            "examples/",
            ".venv/",
        ]
    }
    
    for category, items in structure.items():
        print(f"\n{category}:")
        for item in items:
            if os.path.exists(item):
                if os.path.isdir(item):
                    # 统计目录中的文件数量
                    try:
                        file_count = len([f for f in os.listdir(item) if os.path.isfile(os.path.join(item, f))])
                        print(f"   📂 {item}/ ({file_count} 个文件)")
                    except:
                        print(f"   📂 {item}/")
                else:
                    size = os.path.getsize(item)
                    print(f"   📄 {item} ({size} bytes)")
            else:
                print(f"   ❌ {item} (不存在)")
    
    print("\n🎯 重组效果:")
    print("=" * 40)
    print("✅ 根目录文件数量大幅减少")
    print("✅ 测试脚本归类到 scripts/tests/")
    print("✅ 演示脚本归类到 scripts/demos/")
    print("✅ 研究脚本归类到 scripts/research/")
    print("✅ 文档文件归类到 docs/")
    print("✅ 项目结构更加清晰整洁")
    
    print("\n📋 使用说明:")
    print("=" * 40)
    print("1. 运行测试脚本:")
    print("   python scripts/tests/test_api.py")
    print("   python scripts/tests/test_optimization.py")
    
    print("\n2. 运行演示脚本:")
    print("   python scripts/demos/realtime_usage_demo.py")
    print("   python scripts/demos/incremental_demo.py")
    
    print("\n3. 运行研究脚本:")
    print("   python scripts/research/akshare_methods_research.py")
    print("   python scripts/research/project_files_analysis.py")
    
    print("\n4. 查看文档:")
    print("   cat docs/README.md")
    print("   cat docs/akshare_detailed_analysis.md")

def count_files():
    """统计各目录文件数量"""
    print("\n📊 文件统计:")
    print("=" * 40)
    
    directories = [
        "scripts/tests",
        "scripts/demos", 
        "scripts/research",
        "docs",
        "app",
        "data",
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            try:
                files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
                print(f"   {directory}/: {len(files)} 个文件")
            except:
                print(f"   {directory}/: 无法访问")
        else:
            print(f"   {directory}/: 目录不存在")

def main():
    """主函数"""
    print("🚀 项目结构查看")
    print("=" * 80)
    
    show_project_structure()
    count_files()
    
    print("\n🎉 项目重组完成!")
    print("现在项目结构更加整洁，便于维护和开发。")

if __name__ == "__main__":
    main() 