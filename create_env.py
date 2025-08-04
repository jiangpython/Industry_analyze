#!/usr/bin/env python3
"""
快速创建.env配置文件
只包含Settings类中已定义的配置项
"""

import os
import secrets
import shutil
from pathlib import Path


def generate_secret_key() -> str:
    """生成安全的SECRET_KEY"""
    return secrets.token_urlsafe(32)


def create_env_file():
    """创建.env文件"""
    print("🔧 正在创建.env配置文件...")
    
    # 检查是否已存在.env文件
    if os.path.exists('.env'):
        response = input("⚠️  .env文件已存在，是否覆盖？(y/N): ")
        if response.lower() != 'y':
            print("❌ 操作已取消")
            return False
    
    # 检查模板文件是否存在
    template_file = 'env_template.txt'
    if not os.path.exists(template_file):
        print(f"❌ 模板文件 {template_file} 不存在")
        return False
    
    try:
        # 复制模板文件
        shutil.copy(template_file, '.env')
        
        # 生成安全的SECRET_KEY
        secret_key = generate_secret_key()
        
        # 读取.env文件内容
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换SECRET_KEY
        content = content.replace('your-secret-key-change-in-production', secret_key)
        
        # 写回文件
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ .env文件创建成功！")
        print(f"🔐 已生成安全的SECRET_KEY: {secret_key[:20]}...")
        print("\n📝 请根据实际需要修改以下配置：")
        print("   - GEMINI_API_KEY: 如果需要AI分析功能")
        print("   - DATABASE_URL: 根据实际数据库配置")
        print("   - TARGET_INDUSTRIES: 根据分析需求调整")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建.env文件失败: {e}")
        return False


def validate_env_file():
    """验证.env文件配置"""
    print("\n🔍 验证.env文件配置...")
    
    if not os.path.exists('.env'):
        print("❌ .env文件不存在")
        return False
    
    # Settings类中定义的配置项
    settings_configs = [
        'DATA_DIR',
        'LOG_DIR',
        'COMPANIES_FILE',
        'FINANCIAL_DATA_FILE',
        'INDUSTRY_DATA_FILE',
        'ANALYSIS_RESULTS_FILE',
        'COMPANIES_CSV',
        'FINANCIAL_DATA_CSV',
        'GEMINI_API_KEY',
        'LOG_LEVEL',
        'LOG_FILE',
        'DEBUG',
        'SECRET_KEY',
        'CRAWLER_DELAY',
        'CRAWLER_TIMEOUT',
        'USER_AGENT',
        'DATABASE_URL',
        'EASTMONEY_BASE_URL',
        'THS_BASE_URL',
        'STATS_BASE_URL',
        'TARGET_INDUSTRIES'
    ]
    
    print("✅ Settings类中定义的配置项：")
    print("📋 已创建.env文件，包含以下配置项：")
    for config in settings_configs:
        print(f"   - {config}")
    
    print("\n💡 提示：")
    print("   - 所有配置项都有合理的默认值")
    print("   - 可以根据需要修改.env文件中的值")
    print("   - 修改后需要重启应用才能生效")
    
    return True


def main():
    """主函数"""
    print("🚀 金融分析系统环境配置工具")
    print("=" * 50)
    
    # 创建.env文件
    if create_env_file():
        # 验证配置
        validate_env_file()
        
        print("\n🎉 配置完成！")
        print("📖 详细配置说明请查看: docs/ENV_CONFIG.md")
        print("🚀 现在可以运行: python run.py")
    else:
        print("\n❌ 配置失败，请检查错误信息")


if __name__ == "__main__":
    main() 