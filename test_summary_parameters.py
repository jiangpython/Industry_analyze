#!/usr/bin/env python3
"""
测试API端点的中文summary参数
"""

import requests
import json
import time

def test_api_summary_parameters():
    """测试API端点的中文summary参数"""
    base_url = "http://localhost:8000"
    
    print("🧪 测试API端点的中文summary参数...")
    print("=" * 60)
    
    try:
        # 获取OpenAPI规范
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code != 200:
            print(f"❌ 无法获取OpenAPI规范: {response.status_code}")
            return
        
        openapi_data = response.json()
        paths = openapi_data.get('paths', {})
        
        print("📋 检查API端点的summary参数:")
        print()
        
        # 统计信息
        total_endpoints = 0
        endpoints_with_summary = 0
        endpoints_with_chinese_summary = 0
        
        # 检查每个路径
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    total_endpoints += 1
                    summary = details.get('summary', '')
                    
                    if summary:
                        endpoints_with_summary += 1
                        # 检查是否包含中文字符
                        if any('\u4e00' <= char <= '\u9fff' for char in summary):
                            endpoints_with_chinese_summary += 1
                            print(f"✅ {method.upper()} {path}")
                            print(f"   📝 Summary: {summary}")
                        else:
                            print(f"⚠️  {method.upper()} {path}")
                            print(f"   📝 Summary: {summary} (非中文)")
                    else:
                        print(f"❌ {method.upper()} {path}")
                        print(f"   📝 Summary: 未设置")
                    
                    print()
        
        # 打印统计信息
        print("=" * 60)
        print("📊 统计结果:")
        print(f"   总端点数量: {total_endpoints}")
        print(f"   有summary的端点: {endpoints_with_summary}")
        print(f"   有中文summary的端点: {endpoints_with_chinese_summary}")
        print(f"   覆盖率: {endpoints_with_summary/total_endpoints*100:.1f}%")
        print(f"   中文覆盖率: {endpoints_with_chinese_summary/total_endpoints*100:.1f}%")
        
        # 检查特定端点
        print("\n🔍 检查关键端点:")
        key_endpoints = [
            "/api/v1/realtime/stock/{symbol}",
            "/api/v1/companies/",
            "/api/v1/industries/",
            "/api/v1/historical/stock/{symbol}",
            "/api/v1/tasks/",
            "/api/v1/data/stock/{symbol}",
            "/api/v1/overview/"
        ]
        
        for endpoint in key_endpoints:
            if endpoint in paths:
                method = list(paths[endpoint].keys())[0]
                summary = paths[endpoint][method].get('summary', '未设置')
                print(f"   {method.upper()} {endpoint}: {summary}")
            else:
                print(f"   ❌ {endpoint}: 端点不存在")
        
        print("\n🎯 建议:")
        if endpoints_with_chinese_summary < total_endpoints:
            print("   ⚠️  还有部分端点缺少中文summary参数")
            print("   💡 请检查以下端点:")
            for path, methods in paths.items():
                for method, details in methods.items():
                    if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                        summary = details.get('summary', '')
                        if not summary or not any('\u4e00' <= char <= '\u9fff' for char in summary):
                            print(f"      {method.upper()} {path}")
        else:
            print("   ✅ 所有端点都已添加中文summary参数")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_swagger_ui_display():
    """测试Swagger UI中的中文显示"""
    print("\n" + "=" * 60)
    print("🌐 测试Swagger UI中文显示...")
    
    try:
        # 测试Swagger UI页面
        response = requests.get("http://localhost:8000/docs")
        if response.status_code == 200:
            print("✅ Swagger UI页面加载成功")
            
            # 检查页面内容
            content = response.text
            if "金融分析系统" in content:
                print("✅ 页面包含中文标题")
            if "实时数据" in content or "历史数据" in content:
                print("✅ 页面包含中文标签")
            if "获取" in content or "📈" in content:
                print("✅ 页面包含中文summary")
        else:
            print(f"❌ Swagger UI页面加载失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Swagger UI测试失败: {e}")

if __name__ == "__main__":
    print("🚀 开始测试API端点的中文summary参数...")
    print("请确保应用已启动: python run.py")
    print()
    
    # 等待应用启动
    print("⏳ 等待应用启动...")
    time.sleep(3)
    
    # 测试summary参数
    test_api_summary_parameters()
    
    # 测试Swagger UI显示
    test_swagger_ui_display()
    
    print("\n✨ 测试完成！")
    print("现在可以访问 http://localhost:8000/docs 查看优化后的界面") 