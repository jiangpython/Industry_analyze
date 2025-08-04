#!/usr/bin/env python3
"""
金融分析系统启动脚本
"""

import uvicorn
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.config import settings

def main():
    """主函数"""
    print("🚀 启动金融分析系统...")
    print(f"💾 数据存储: {settings.DATA_DIR}")
    print(f"🔧 调试模式: {settings.DEBUG}")
    print(f"📝 日志级别: {settings.LOG_LEVEL}")
    print(f"🎯 目标行业: {settings.TARGET_INDUSTRIES}")
    print("🌐 访问地址:")
    print("   📱 本地访问: http://localhost:8000")
    print("   🌍 网络访问: http://0.0.0.0:8000")
    print("   📚 API文档: http://localhost:8000/docs")
    print("   📖 交互文档: http://localhost:8000/redoc")
    print("=" * 50)
    
    # 启动服务器
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    main() 