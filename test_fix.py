#!/usr/bin/env python3
"""
测试OpenAPI规范修复
"""

import requests
import time

def test_openapi_spec():
    """测试OpenAPI规范"""
    base_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            spec = response.json()
            if "openapi" in spec:
                print(f"✅ OpenAPI版本: {spec['openapi']}")
                print(f"✅ 标题: {spec['info']['title']}")
                print(f"✅ 标签数量: {len(spec['tags'])}")
                return True
        else:
            print(f"❌ 获取OpenAPI规范失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    print("🚀 测试OpenAPI规范修复...")
    time.sleep(2)
    
    if test_openapi_spec():
        print("\n✅ 修复成功！现在可以访问:")
        print("   📱 http://localhost:8000/docs")
        print("   🎨 http://localhost:8000/docs-custom")
    else:
        print("\n❌ 修复失败")

if __name__ == "__main__":
    main() 