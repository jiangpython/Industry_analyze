#!/usr/bin/env python3
"""
测试界面优化效果
"""

import requests
import json
import time

def test_api_documentation():
    """测试API文档界面"""
    base_url = "http://localhost:8000"
    
    print("🧪 测试界面优化效果...")
    print("=" * 50)
    
    # 测试根路径
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ 根路径访问成功: {response.status_code}")
        print(f"   响应: {response.json()}")
    except Exception as e:
        print(f"❌ 根路径访问失败: {e}")
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ 健康检查成功: {response.status_code}")
        print(f"   响应: {response.json()}")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
    
    # 测试API概览
    try:
        response = requests.get(f"{base_url}/api/v1/")
        print(f"✅ API概览成功: {response.status_code}")
        data = response.json()
        print(f"   可用端点: {list(data.get('endpoints', {}).keys())}")
    except Exception as e:
        print(f"❌ API概览失败: {e}")
    
    # 测试实时数据API
    try:
        response = requests.get(f"{base_url}/api/v1/realtime/stock/000001")
        print(f"✅ 实时数据API成功: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   股票代码: {data.get('code')}")
            print(f"   股票名称: {data.get('name')}")
    except Exception as e:
        print(f"❌ 实时数据API失败: {e}")
    
    # 测试公司管理API
    try:
        response = requests.get(f"{base_url}/api/v1/companies/")
        print(f"✅ 公司管理API成功: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   返回公司数量: {len(data)}")
    except Exception as e:
        print(f"❌ 公司管理API失败: {e}")
    
    # 测试行业管理API
    try:
        response = requests.get(f"{base_url}/api/v1/industries/")
        print(f"✅ 行业管理API成功: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   支持行业数量: {len(data)}")
            print(f"   行业列表: {data[:5]}...")  # 显示前5个
    except Exception as e:
        print(f"❌ 行业管理API失败: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 界面优化说明:")
    print("1. 所有API标签已改为中文")
    print("2. 界面布局更加紧凑")
    print("3. 支持中文显示优化")
    print("4. 自定义CSS样式已应用")
    print("5. 新增美化文档页面")
    print("\n📖 访问地址:")
    print(f"   📱 API文档: {base_url}/docs")
    print(f"   🎨 美化文档: {base_url}/docs-beautiful")
    print(f"   📖 交互文档: {base_url}/redoc")
    print(f"   🏠 主页: {base_url}/")
    print(f"   🔍 API概览: {base_url}/api/v1/")

def test_custom_css():
    """测试自定义CSS文件"""
    try:
        response = requests.get("http://localhost:8000/static/custom.css")
        if response.status_code == 200:
            print("✅ 自定义CSS文件加载成功")
            print(f"   CSS文件大小: {len(response.text)} 字符")
        else:
            print(f"❌ 自定义CSS文件加载失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 自定义CSS文件测试失败: {e}")

def test_beautiful_docs():
    """测试美化文档页面"""
    try:
        response = requests.get("http://localhost:8000/docs-beautiful")
        if response.status_code == 200:
            print("✅ 美化文档页面加载成功")
            print(f"   页面大小: {len(response.text)} 字符")
            if "金融分析系统" in response.text:
                print("   ✅ 页面包含正确的标题")
            if "实时数据监控" in response.text:
                print("   ✅ 页面包含功能说明")
            if "API端点概览" in response.text:
                print("   ✅ 页面包含API端点说明")
        else:
            print(f"❌ 美化文档页面加载失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 美化文档页面测试失败: {e}")

def test_api_tags():
    """测试API标签的中文说明"""
    try:
        response = requests.get("http://localhost:8000/openapi.json")
        if response.status_code == 200:
            data = response.json()
            tags = data.get('tags', [])
            print(f"✅ API标签数量: {len(tags)}")
            
            for tag in tags:
                name = tag.get('name', '')
                description = tag.get('description', '')
                print(f"   📋 {name}: {description[:50]}...")
                
            # 检查是否有中文标签
            chinese_tags = [tag for tag in tags if any('\u4e00' <= char <= '\u9fff' for char in tag.get('name', ''))]
            print(f"   ✅ 中文标签数量: {len(chinese_tags)}")
            
        else:
            print(f"❌ OpenAPI文档加载失败: {response.status_code}")
    except Exception as e:
        print(f"❌ API标签测试失败: {e}")

if __name__ == "__main__":
    print("🚀 开始测试界面优化效果...")
    print("请确保应用已启动: python run.py")
    print()
    
    # 等待应用启动
    print("⏳ 等待应用启动...")
    time.sleep(2)
    
    # 测试API功能
    test_api_documentation()
    
    # 测试CSS文件
    test_custom_css()
    
    # 测试美化文档页面
    test_beautiful_docs()
    
    # 测试API标签
    test_api_tags()
    
    print("\n✨ 测试完成！")
    print("现在可以访问以下地址查看优化后的界面:")
    print("   📱 标准API文档: http://localhost:8000/docs")
    print("   🎨 美化API文档: http://localhost:8000/docs-beautiful")
    print("   📖 交互式文档: http://localhost:8000/redoc") 