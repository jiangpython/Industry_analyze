#!/usr/bin/env python3
"""
配置管理器示例
展示.env和config.json的使用方法和区别
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        # 加载.env文件
        load_dotenv()
        
        # 配置文件路径
        self.env_file = ".env"
        self.config_file = "config.json"
        
    def get_env_config(self) -> Dict[str, Any]:
        """获取环境变量配置"""
        return {
            "DEBUG": os.getenv("DEBUG", "True").lower() == "true",
            "SECRET_KEY": os.getenv("SECRET_KEY", "default-secret-key"),
            "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
            "DATA_DIR": os.getenv("DATA_DIR", "./data"),
            "LOG_DIR": os.getenv("LOG_DIR", "./logs"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            "CRAWLER_DELAY": int(os.getenv("CRAWLER_DELAY", "1")),
            "CRAWLER_TIMEOUT": int(os.getenv("CRAWLER_TIMEOUT", "30")),
            "USER_AGENT": os.getenv("USER_AGENT", "Mozilla/5.0"),
            "EASTMONEY_BASE_URL": os.getenv("EASTMONEY_BASE_URL", "http://f10.eastmoney.com"),
            "THS_BASE_URL": os.getenv("THS_BASE_URL", "http://basic.10jqka.com.cn"),
            "STATS_BASE_URL": os.getenv("STATS_BASE_URL", "http://www.stats.gov.cn"),
            "TARGET_INDUSTRIES": os.getenv("TARGET_INDUSTRIES", "医药,新能源,半导体,芯片").split(",")
        }
    
    def get_json_config(self) -> Dict[str, Any]:
        """获取JSON配置文件"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_env_config(self, config: Dict[str, Any]) -> bool:
        """保存环境变量配置到.env文件"""
        try:
            with open(self.env_file, 'w', encoding='utf-8') as f:
                f.write("# 应用配置\n")
                f.write(f"DEBUG={config.get('DEBUG', True)}\n")
                f.write(f"SECRET_KEY={config.get('SECRET_KEY', 'your-secret-key-change-in-production')}\n\n")
                
                f.write("# 数据存储路径\n")
                f.write(f"DATA_DIR={config.get('DATA_DIR', './data')}\n")
                f.write(f"LOG_DIR={config.get('LOG_DIR', './logs')}\n\n")
                
                f.write("# Gemini API配置\n")
                f.write(f"GEMINI_API_KEY={config.get('GEMINI_API_KEY', 'your_gemini_api_key_here')}\n\n")
                
                f.write("# 日志配置\n")
                f.write(f"LOG_LEVEL={config.get('LOG_LEVEL', 'INFO')}\n\n")
                
                f.write("# 爬虫配置\n")
                f.write(f"CRAWLER_DELAY={config.get('CRAWLER_DELAY', 1)}\n")
                f.write(f"CRAWLER_TIMEOUT={config.get('CRAWLER_TIMEOUT', 30)}\n")
                f.write(f"USER_AGENT={config.get('USER_AGENT', 'Mozilla/5.0')}\n\n")
                
                f.write("# 数据源配置\n")
                f.write(f"EASTMONEY_BASE_URL={config.get('EASTMONEY_BASE_URL', 'http://f10.eastmoney.com')}\n")
                f.write(f"THS_BASE_URL={config.get('THS_BASE_URL', 'http://basic.10jqka.com.cn')}\n")
                f.write(f"STATS_BASE_URL={config.get('STATS_BASE_URL', 'http://www.stats.gov.cn')}\n\n")
                
                f.write("# 行业配置\n")
                industries = config.get('TARGET_INDUSTRIES', ['医药', '新能源', '半导体', '芯片'])
                f.write(f"TARGET_INDUSTRIES={','.join(industries)}\n")
            
            return True
        except Exception as e:
            print(f"保存.env文件失败: {e}")
            return False
    
    def save_json_config(self, config: Dict[str, Any]) -> bool:
        """保存JSON配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存config.json文件失败: {e}")
            return False
    
    def generate_secret_key(self) -> str:
        """生成安全的SECRET_KEY"""
        import secrets
        return secrets.token_urlsafe(32)
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证配置的有效性"""
        required_keys = ['SECRET_KEY', 'GEMINI_API_KEY']
        
        for key in required_keys:
            if not config.get(key):
                print(f"⚠️  缺少必要的配置项: {key}")
                return False
        
        return True

def demonstrate_config_differences():
    """演示.env和config.json的区别"""
    print("🔧 配置文件对比演示")
    print("=" * 50)
    
    config_manager = ConfigManager()
    
    # 1. 环境变量配置（.env）
    print("\n📄 .env 文件特点:")
    print("- 键值对格式: KEY=VALUE")
    print("- 主要用于环境变量")
    print("- 包含敏感信息（API密钥等）")
    print("- 不提交到版本控制")
    
    env_config = config_manager.get_env_config()
    print(f"\n.env 配置示例:")
    for key, value in list(env_config.items())[:5]:
        print(f"  {key}: {value}")
    
    # 2. JSON配置文件
    print("\n📄 config.json 文件特点:")
    print("- JSON格式，支持复杂数据结构")
    print("- 主要用于应用配置")
    print("- 可以提交到版本控制")
    print("- 支持嵌套对象和数组")
    
    json_config = config_manager.get_json_config()
    if json_config:
        print(f"\nconfig.json 配置示例:")
        print(f"  应用名称: {json_config.get('app', {}).get('name', 'N/A')}")
        print(f"  数据源: {list(json_config.get('data_sources', {}).keys())}")
    
    # 3. SECRET_KEY 说明
    print("\n🔐 SECRET_KEY 说明:")
    print("- 用于会话加密和令牌签名")
    print("- 必须足够长且随机")
    print("- 绝不能提交到版本控制")
    print("- 每个环境应该不同")
    
    # 生成示例SECRET_KEY
    example_key = config_manager.generate_secret_key()
    print(f"\n示例SECRET_KEY: {example_key[:20]}...")

def show_usage_examples():
    """显示配置使用示例"""
    print("\n💡 配置使用示例:")
    print("=" * 50)
    
    # 1. 环境变量使用
    print("\n1. 环境变量使用 (.env):")
    print("""
# 在代码中使用
import os
from dotenv import load_dotenv

load_dotenv()  # 加载.env文件

api_key = os.getenv("GEMINI_API_KEY")
debug_mode = os.getenv("DEBUG", "False").lower() == "true"
    """)
    
    # 2. JSON配置使用
    print("\n2. JSON配置使用 (config.json):")
    print("""
# 在代码中使用
import json

with open('config.json', 'r') as f:
    config = json.load(f)

app_name = config['app']['name']
data_dir = config['database']['data_dir']
    """)
    
    # 3. 混合使用
    print("\n3. 混合使用 (推荐):")
    print("""
# 敏感信息使用.env
# 应用配置使用config.json

# .env文件
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# config.json文件
{
  "app": {"name": "金融分析系统"},
  "database": {"type": "file"}
}
    """)

def main():
    """主函数"""
    print("🚀 配置文件管理演示")
    print("=" * 60)
    
    # 演示配置差异
    demonstrate_config_differences()
    
    # 显示使用示例
    show_usage_examples()
    
    print("\n✅ 演示完成！")
    print("\n📝 总结:")
    print("- .env: 环境变量，敏感信息")
    print("- config.json: 应用配置，复杂数据")
    print("- SECRET_KEY: 安全密钥，必须保密")

if __name__ == "__main__":
    main() 