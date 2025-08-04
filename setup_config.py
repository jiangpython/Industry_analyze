#!/usr/bin/env python3
"""
自动配置脚本
生成安全的SECRET_KEY并创建.env文件
"""

import os
import secrets
from pathlib import Path

def generate_secret_key() -> str:
    """生成安全的SECRET_KEY"""
    return secrets.token_urlsafe(32)

def create_env_file():
    """创建.env文件"""
    print("🔧 正在创建.env配置文件...")
    
    # 生成安全的SECRET_KEY
    secret_key = generate_secret_key()
    
    # .env文件内容
    env_content = f"""# 应用配置
DEBUG=True
SECRET_KEY={secret_key}

# 数据存储路径
DATA_DIR=./data
LOG_DIR=./logs

# Gemini API配置
GEMINI_API_KEY=your_gemini_api_key_here

# 日志配置
LOG_LEVEL=INFO

# 爬虫配置
CRAWLER_DELAY=1
CRAWLER_TIMEOUT=30
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36

# 数据源配置
EASTMONEY_BASE_URL=http://f10.eastmoney.com
THS_BASE_URL=http://basic.10jqka.com.cn
STATS_BASE_URL=http://www.stats.gov.cn

# 行业配置
TARGET_INDUSTRIES=医药,新能源,半导体,芯片
"""
    
    # 写入.env文件
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ .env文件创建成功！")
        print(f"🔐 已生成安全的SECRET_KEY: {secret_key[:20]}...")
        return True
    except Exception as e:
        print(f"❌ 创建.env文件失败: {e}")
        return False

def check_existing_env():
    """检查是否已存在.env文件"""
    if os.path.exists('.env'):
        print("⚠️  发现已存在的.env文件")
        response = input("是否要覆盖现有文件? (y/N): ")
        return response.lower() == 'y'
    return True

def show_next_steps():
    """显示后续步骤"""
    print("\n📋 后续配置步骤:")
    print("=" * 50)
    
    print("\n1. 配置Gemini API密钥:")
    print("   - 访问 https://makersuite.google.com/app/apikey")
    print("   - 创建API密钥")
    print("   - 编辑.env文件，将your_gemini_api_key_here替换为您的实际API密钥")
    
    print("\n2. 验证配置:")
    print("   python -c \"from app.core.config import settings; print('配置加载成功')\"")
    
    print("\n3. 启动服务:")
    print("   python run.py")
    
    print("\n4. 访问API文档:")
    print("   http://localhost:8000/docs")
    
    print("\n5. 运行示例:")
    print("   python example_local_storage.py")

def main():
    """主函数"""
    print("🚀 金融分析系统配置向导")
    print("=" * 50)
    
    # 检查是否允许覆盖
    if not check_existing_env():
        print("❌ 操作已取消")
        return
    
    # 创建.env文件
    if create_env_file():
        show_next_steps()
        print("\n✅ 配置完成！")
    else:
        print("\n❌ 配置失败，请检查错误信息")

if __name__ == "__main__":
    main() 