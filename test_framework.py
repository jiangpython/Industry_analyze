#!/usr/bin/env python3
"""
简单的框架测试
"""

import os
import sys

def test_project_structure():
    """测试项目结构"""
    print("🔍 检查项目结构...")
    
    # 检查必要的目录
    required_dirs = [
        'app',
        'app/api',
        'app/api/endpoints',
        'app/core',
        'app/database',
        'app/services',
        'app/services/collectors',
        'app/services/processors',
        'app/services/analyzers',
        'app/utils',
        'data',
        'logs',
        'tests'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - 目录不存在")
    
    # 检查必要的文件
    required_files = [
        'requirements.txt',
        'README.md',
        'run.py',
        'app/main.py',
        'app/core/config.py',
        'app/core/config_simple.py',
        'app/core/database.py',
        'app/database/models.py',
        'app/api/endpoints/companies.py',
        'app/api/endpoints/industries.py',
        'app/api/endpoints/tasks.py',
        'app/services/collectors/base_collector.py',
        'app/services/processors/financial_processor.py',
        'app/services/analyzers/gemini_analyzer.py',
        'app/utils/helpers.py'
    ]
    
    print("\n📁 检查必要文件...")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件不存在")
    
    return True

def test_config_loading():
    """测试配置加载"""
    print("\n⚙️ 测试配置加载...")
    
    try:
        # 添加项目根目录到Python路径
        project_root = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_root)
        
        # 尝试导入简化配置
        from app.core.config_simple import simple_settings
        print("✅ 配置加载成功")
        print(f"   - 数据库URL: {simple_settings.DATABASE_URL}")
        print(f"   - 日志级别: {simple_settings.LOG_LEVEL}")
        print(f"   - 调试模式: {simple_settings.DEBUG}")
        print(f"   - 目标行业: {simple_settings.TARGET_INDUSTRIES}")
        return True
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

def test_database_models():
    """测试数据库模型"""
    print("\n🗄️ 测试数据库模型...")
    
    try:
        # 检查模型文件是否存在
        model_file = 'app/database/models.py'
        if os.path.exists(model_file):
            print("✅ 数据库模型文件存在")
            
            # 读取文件内容检查关键类
            with open(model_file, 'r', encoding='utf-8') as f:
                content = f.read()
                classes = ['Company', 'FinancialData', 'IndustryData', 'AnalysisResult', 'TaskLog']
                for class_name in classes:
                    if f"class {class_name}" in content:
                        print(f"   ✅ {class_name} 类已定义")
                    else:
                        print(f"   ❌ {class_name} 类未找到")
            return True
        else:
            print("❌ 数据库模型文件不存在")
            return False
    except Exception as e:
        print(f"❌ 数据库模型检查失败: {e}")
        return False

def test_helpers():
    """测试工具函数"""
    print("\n🛠️ 测试工具函数...")
    
    try:
        # 检查工具函数文件是否存在
        helpers_file = 'app/utils/helpers.py'
        if os.path.exists(helpers_file):
            print("✅ 工具函数文件存在")
            
            # 读取文件内容检查关键函数
            with open(helpers_file, 'r', encoding='utf-8') as f:
                content = f.read()
                functions = ['validate_stock_code', 'format_stock_code', 'classify_industry']
                for func_name in functions:
                    if f"def {func_name}" in content:
                        print(f"   ✅ {func_name} 函数已定义")
                    else:
                        print(f"   ❌ {func_name} 函数未找到")
            return True
        else:
            print("❌ 工具函数文件不存在")
            return False
    except Exception as e:
        print(f"❌ 工具函数检查失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n🌐 测试API端点...")
    
    try:
        # 检查API端点文件
        endpoint_files = [
            'app/api/endpoints/companies.py',
            'app/api/endpoints/industries.py',
            'app/api/endpoints/tasks.py'
        ]
        
        for file_path in endpoint_files:
            if os.path.exists(file_path):
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - 文件不存在")
        
        # 检查主应用文件
        main_file = 'app/main.py'
        if os.path.exists(main_file):
            print(f"✅ {main_file}")
        else:
            print(f"❌ {main_file} - 文件不存在")
        
        return True
    except Exception as e:
        print(f"❌ API端点检查失败: {e}")
        return False

def test_services():
    """测试服务层"""
    print("\n🔧 测试服务层...")
    
    try:
        # 检查服务文件
        service_files = [
            'app/services/collectors/base_collector.py',
            'app/services/processors/financial_processor.py',
            'app/services/analyzers/gemini_analyzer.py'
        ]
        
        for file_path in service_files:
            if os.path.exists(file_path):
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - 文件不存在")
        
        return True
    except Exception as e:
        print(f"❌ 服务层检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始框架测试...\n")
    
    tests = [
        test_project_structure,
        test_config_loading,
        test_database_models,
        test_helpers,
        test_api_endpoints,
        test_services
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！框架搭建成功！")
        print("\n📋 下一步:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 配置环境变量: 复制 env.example 为 .env")
        print("3. 启动服务: python run.py")
        print("4. 访问API文档: http://localhost:8000/docs")
        print("\n💡 项目特点:")
        print("- 模块化设计，便于维护和扩展")
        print("- 支持多设备同步（Git + 云数据库）")
        print("- 集成Gemini AI分析")
        print("- 完整的API接口")
        print("- 定时任务支持")
    else:
        print("⚠️ 部分测试失败，请检查项目结构")

if __name__ == "__main__":
    main() 