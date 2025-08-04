#!/usr/bin/env python3
"""
测试运行脚本
统一运行所有测试文件
"""

import os
import sys
import subprocess
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_test_file(test_file: str) -> bool:
    """运行单个测试文件"""
    print(f"\n{'='*60}")
    print(f"🧪 运行测试: {test_file}")
    print(f"{'='*60}")
    
    try:
        # 运行测试文件
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent / test_file)
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print(f"✅ {test_file} 测试通过")
            if result.stdout:
                print("输出:")
                print(result.stdout)
            return True
        else:
            print(f"❌ {test_file} 测试失败")
            if result.stderr:
                print("错误:")
                print(result.stderr)
            if result.stdout:
                print("输出:")
                print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ 运行 {test_file} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始运行所有测试")
    print("=" * 80)
    
    # 测试文件列表
    test_files = [
        "test_basic.py",
        "test_all_modules.py", 
        "test_financial_fix.py",
        "test_api_error.py"
    ]
    
    # 运行统计
    total_tests = len(test_files)
    passed_tests = 0
    failed_tests = []
    
    # 运行每个测试文件
    for test_file in test_files:
        if run_test_file(test_file):
            passed_tests += 1
        else:
            failed_tests.append(test_file)
    
    # 输出测试结果
    print(f"\n{'='*80}")
    print("📊 测试结果汇总")
    print(f"{'='*80}")
    print(f"总测试数: {total_tests}")
    print(f"通过: {passed_tests}")
    print(f"失败: {len(failed_tests)}")
    
    if failed_tests:
        print(f"\n❌ 失败的测试:")
        for test in failed_tests:
            print(f"  - {test}")
    else:
        print(f"\n🎉 所有测试都通过了！")
    
    print(f"\n💡 提示:")
    print(f"  - 可以单独运行测试: python tests/test_basic.py")
    print(f"  - 查看详细错误信息请检查上面的输出")
    print(f"  - 测试文件位置: tests/")

if __name__ == "__main__":
    main() 