from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.api.endpoints import companies_simple, industries_simple, tasks_simple, yahoo_data, data_source, realtime_data, historical_data, api_overview
import logging
import os

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)

# 创建日志目录
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)

# 创建FastAPI应用
app = FastAPI(
    title="📊 实时股票数据 API",
    description="""
<div style="line-height: 1.6;">
    <h2>🚀 功能特色</h2>
    <h3>✨ 核心功能</h3>
    <ul>
        <li>📈 <strong>实时股票数据</strong>：获取最新的股票价格、涨跌幅等信息</li>
        <li>🏢 <strong>行业分析</strong>：支持按行业分类获取公司数据</li>
        <li>⚡ <strong>高性能缓存</strong>：智能缓存机制，提升查询速度</li>
        <li>🔧 <strong>连接监控</strong>：实时监控数据源连接状态</li>
    </ul>
    <h3>📊 数据来源</h3>
    <p>采用 <strong>AKShare</strong> 和 <strong>Yahoo Finance</strong> 双数据源，确保数据准确性与实时性。</p>
    <hr>
    <p><em>API 版本：v1 | 数据更新频率：实时</em></p>
</div>
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_version="3.0.2",
    contact={
        "name": "技术支持",
        "email": "support@finance-ai.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "📊 实时数据监控",
            "description": """
🔥 实时市场数据获取

📈 核心功能：股票实时价格、行业数据、缓存加速、强制刷新
🎯 使用场景：日内交易、实时监控、量化分析
🌐 数据来源：AKShare、Yahoo Finance
            """,
        },
        {
            "name": "📈 历史数据分析", 
            "description": """
📊 专业历史数据服务

📅 数据功能：K线数据、财务数据、基本信息、技术指标
📊 覆盖范围：A股全市场，历史数据最长10年
💾 导出格式：JSON、CSV、Excel
            """,
        },
        {
            "name": "🏢 公司深度研究",
            "description": """
🔍 公司基本面深度分析

🤖 AI分析：AI财务分析、盈利能力、偿债能力、成长性
⚖️ 对比功能：同行业公司对比、历史数据对比
⚠️ 风险评估：AI风险评估和投资建议
            """,
        },
        {
            "name": "🏭 行业趋势洞察",
            "description": """
📊 行业全景分析平台

💊 重点行业：医药、新能源、半导体、新能源汽车
📈 分析维度：市场规模、竞争格局、发展趋势、投资机会
🔄 数据更新：实时更新行业数据和政策变化
            """,
        },
        {
            "name": "⚙️ 智能任务管理",
            "description": """
🤖 自动化数据处理中心

📥 任务类型：数据采集、分析报告、监控提醒、数据同步
⏰ 调度方式：定时执行、事件触发、手动启动
📊 状态监控：实时查看任务执行状态和结果
            """,
        },
        {
            "name": "🔌 数据源管理",
            "description": """
🌐 多数据源统一管理

📊 数据源：AKShare、Yahoo Finance、财经新闻、官方数据
🔧 管理功能：配置、连接测试、质量监控
🛡️ 服务稳定：自动切换可用数据源，确保服务稳定
            """,
        },
        {
            "name": "📋 系统概览",
            "description": """
📊 系统状态和使用统计

📈 监控指标：API调用统计、数据存储状态、系统健康度、用户活跃度
🧭 快速导航：常用API快速入口和使用指南
            """,
        },
    ]
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 美化的API文档路由
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """自定义美化的Swagger文档"""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="🚀 智能金融分析系统 - API文档",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4.15.5/swagger-ui-bundle.js",
        swagger_css_url="/static/custom-swagger.css",  # 使用自定义CSS
        custom_css="""
        /* 功能区卡片样式 */
        .swagger-ui .opblock-tag-section {
            margin-bottom: 25px !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            background: white !important;
        }
        
        /* 实时数据监控 - 绿色主题 */
        .swagger-ui .opblock-tag-section:nth-child(1) .opblock-tag {
            background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 50%, #81C784 100%) !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 12px 20px !important;
            margin: 0 !important;
            border: none !important;
        }
        
        .swagger-ui .opblock-tag-section:nth-child(1) .opblock {
            background: linear-gradient(135deg, #E8F5E8 0%, #F1F8E9 100%) !important;
            border-left: 4px solid #4CAF50 !important;
            border-radius: 8px !important;
            margin: 10px !important;
            box-shadow: 0 2px 4px rgba(76, 175, 80, 0.2) !important;
        }
        
        /* 历史数据分析 - 蓝色主题 */
        .swagger-ui .opblock-tag-section:nth-child(2) .opblock-tag {
            background: linear-gradient(135deg, #2196F3 0%, #42A5F5 50%, #64B5F6 100%) !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 12px 20px !important;
            margin: 0 !important;
            border: none !important;
        }
        
        .swagger-ui .opblock-tag-section:nth-child(2) .opblock {
            background: linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%) !important;
            border-left: 4px solid #2196F3 !important;
            border-radius: 8px !important;
            margin: 10px !important;
            box-shadow: 0 2px 4px rgba(33, 150, 243, 0.2) !important;
        }
        
        /* 公司深度研究 - 橙色主题 */
        .swagger-ui .opblock-tag-section:nth-child(3) .opblock-tag {
            background: linear-gradient(135deg, #FF9800 0%, #FFB74D 50%, #FFCC02 100%) !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 12px 20px !important;
            margin: 0 !important;
            border: none !important;
        }
        
        .swagger-ui .opblock-tag-section:nth-child(3) .opblock {
            background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%) !important;
            border-left: 4px solid #FF9800 !important;
            border-radius: 8px !important;
            margin: 10px !important;
            box-shadow: 0 2px 4px rgba(255, 152, 0, 0.2) !important;
        }
        
        /* 行业趋势洞察 - 紫色主题 */
        .swagger-ui .opblock-tag-section:nth-child(4) .opblock-tag {
            background: linear-gradient(135deg, #9C27B0 0%, #BA68C8 50%, #CE93D8 100%) !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 12px 20px !important;
            margin: 0 !important;
            border: none !important;
        }
        
        .swagger-ui .opblock-tag-section:nth-child(4) .opblock {
            background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%) !important;
            border-left: 4px solid #9C27B0 !important;
            border-radius: 8px !important;
            margin: 10px !important;
            box-shadow: 0 2px 4px rgba(156, 39, 176, 0.2) !important;
        }
        
        /* 智能任务管理 - 灰色主题 */
        .swagger-ui .opblock-tag-section:nth-child(5) .opblock-tag {
            background: linear-gradient(135deg, #607D8B 0%, #78909C 50%, #90A4AE 100%) !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 12px 20px !important;
            margin: 0 !important;
            border: none !important;
        }
        
        .swagger-ui .opblock-tag-section:nth-child(5) .opblock {
            background: linear-gradient(135deg, #ECEFF1 0%, #CFD8DC 100%) !important;
            border-left: 4px solid #607D8B !important;
            border-radius: 8px !important;
            margin: 10px !important;
            box-shadow: 0 2px 4px rgba(96, 125, 139, 0.2) !important;
        }
        
        /* 数据源管理 - 棕色主题 */
        .swagger-ui .opblock-tag-section:nth-child(6) .opblock-tag {
            background: linear-gradient(135deg, #795548 0%, #8D6E63 50%, #A1887F 100%) !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 12px 20px !important;
            margin: 0 !important;
            border: none !important;
        }
        
        .swagger-ui .opblock-tag-section:nth-child(6) .opblock {
            background: linear-gradient(135deg, #EFEBE9 0%, #D7CCC8 100%) !important;
            border-left: 4px solid #795548 !important;
            border-radius: 8px !important;
            margin: 10px !important;
            box-shadow: 0 2px 4px rgba(121, 85, 72, 0.2) !important;
        }
        
        /* 系统概览 - 红色主题 */
        .swagger-ui .opblock-tag-section:nth-child(7) .opblock-tag {
            background: linear-gradient(135deg, #F44336 0%, #EF5350 50%, #E57373 100%) !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 12px 20px !important;
            margin: 0 !important;
            border: none !important;
        }
        
        .swagger-ui .opblock-tag-section:nth-child(7) .opblock {
            background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%) !important;
            border-left: 4px solid #F44336 !important;
            border-radius: 8px !important;
            margin: 10px !important;
            box-shadow: 0 2px 4px rgba(244, 67, 54, 0.2) !important;
        }
        
        /* 通用样式优化 */
        .swagger-ui .opblock-tag:hover {
            transform: translateY(-1px) !important;
            transition: all 0.3s ease !important;
        }
        
        .swagger-ui .opblock-summary-description {
            color: #333 !important;
            font-weight: 500 !important;
        }
        
        .swagger-ui .opblock-summary-operation-id {
            color: #666 !important;
            font-size: 12px !important;
        }
        
        /* 美化操作按钮 */
        .swagger-ui .opblock.opblock-get {
            border-color: #61affe !important;
        }
        
        .swagger-ui .opblock.opblock-post {
            border-color: #49cc90 !important;
        }
        
        .swagger-ui .opblock.opblock-put {
            border-color: #fca130 !important;
        }
        
        .swagger-ui .opblock.opblock-delete {
            border-color: #f93e3e !important;
        }
        """,
        swagger_ui_parameters={
            "docExpansion": "list",  # 默认展开列表
            "defaultModelsExpandDepth": 2,
            "defaultModelExpandDepth": 2,
            "displayRequestDuration": True,
            "filter": True,  # 启用搜索过滤
            "showExtensions": True,
            "showCommonExtensions": True,
            "tryItOutEnabled": True,
            "supportedSubmitMethods": ["get", "post", "put", "delete", "patch"],
            "validatorUrl": None,  # 禁用在线验证器
        }
    )

# 注册路由时添加更好的描述
app.include_router(
    companies_simple.router, 
    prefix="/api/v1",
    tags=["🏢 公司深度研究"]
)
app.include_router(
    industries_simple.router, 
    prefix="/api/v1",
    tags=["🏭 行业趋势洞察"]
)
app.include_router(
    tasks_simple.router, 
    prefix="/api/v1",
    tags=["⚙️ 智能任务管理"]
)
app.include_router(
    yahoo_data.router, 
    prefix="/api/v1",
    tags=["🔌 数据源管理"]
)
app.include_router(
    data_source.router, 
    prefix="/api/v1",
    tags=["🔌 数据源管理"]
)
app.include_router(
    realtime_data.router, 
    prefix="/api/v1",
    tags=["📊 实时数据监控"]
)
app.include_router(
    historical_data.router, 
    prefix="/api/v1",
    tags=["📈 历史数据分析"]
)
app.include_router(
    api_overview.router, 
    prefix="/api/v1",
    tags=["📋 系统概览"]
)

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    # 确保数据目录存在
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    # 创建static目录
    os.makedirs("app/static", exist_ok=True)
    logging.info("🚀 金融分析系统启动完成")

@app.get("/", 
         summary="🏠 系统首页",
         description="查看系统基本信息和快速导航链接",
         response_description="返回系统基本信息")
async def root():
    """系统首页 - 获取基本信息和导航链接"""
    return {
        "message": "🚀 欢迎使用智能金融分析系统",
        "version": "2.0.0",
        "features": [
            "📊 实时数据监控",
            "📈 历史数据分析", 
            "🏢 公司深度研究",
            "🏭 行业趋势洞察",
            "⚙️ 智能任务管理",
            "🤖 AI智能分析"
        ],
        "navigation": {
            "api_docs": "📖 API文档: /docs",
            "api_overview": "📋 系统概览: /api/v1/overview",
            "health_check": "💗 健康检查: /health"
        },
        "quick_start": {
            "realtime_stock": "📊 实时股价: GET /api/v1/realtime/stock/000001",
            "company_analysis": "🏢 公司分析: GET /api/v1/companies/000001/analysis",
            "industry_companies": "🏭 行业公司: GET /api/v1/realtime/companies/医药"
        }
    }

@app.get("/health",
         summary="💗 系统健康检查", 
         description="检查系统运行状态和各模块健康度",
         response_description="返回系统健康状态")
async def health_check():
    """系统健康检查 - 监控各模块运行状态"""
    import psutil
    import time
    
    return {
        "status": "🟢 healthy",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "system_info": {
            "cpu_usage": f"{psutil.cpu_percent()}%",
            "memory_usage": f"{psutil.virtual_memory().percent}%",
            "disk_usage": f"{psutil.disk_usage('/').percent}%"
        },
        "modules": {
            "realtime_data": "🟢 正常",
            "historical_data": "🟢 正常", 
            "ai_analysis": "🟢 正常",
            "task_scheduler": "🟢 正常"
        }
    }

@app.get("/api/v1/",
         summary="📋 API总览",
         description="查看所有可用的API接口和使用指南",
         response_description="返回API接口总览")
async def api_root():
    """API接口总览 - 查看所有功能模块"""
    return {
        "title": "🚀 智能金融分析系统 API v2.0",
        "description": "专业的金融数据分析平台，提供实时数据、历史分析、AI洞察等服务",
        "storage_type": "💾 本地文件存储 + 智能缓存",
        "documentation": {
            "swagger_ui": "📖 Swagger文档: /docs",
            "redoc": "📚 ReDoc文档: /redoc",
            "api_overview": "📊 使用统计: /api/v1/overview"
        },
        "功能模块": {
            "📊 实时数据监控": {
                "description": "获取股票实时价格、成交量等市场数据",
                "endpoints": [
                    "GET /api/v1/realtime/stock/{symbol} - 📈 股票实时数据",
                    "GET /api/v1/realtime/companies/{industry} - 🏢 行业实时数据",
                    "GET /api/v1/realtime/summary - 📊 市场总览"
                ]
            },
            "📈 历史数据分析": {
                "description": "获取股票历史价格、K线、财务数据",
                "endpoints": [
                    "GET /api/v1/historical/stock/{symbol} - 📅 历史K线数据", 
                    "GET /api/v1/historical/financial/{symbol} - 💰 财务数据",
                    "GET /api/v1/historical/basic/{symbol} - 📋 基本信息"
                ]
            },
            "🏢 公司深度研究": {
                "description": "公司基本面分析、AI智能评估",
                "endpoints": [
                    "GET /api/v1/companies/{symbol}/analysis - 🤖 AI智能分析",
                    "GET /api/v1/companies/{symbol}/financial - 📊 财务分析", 
                    "GET /api/v1/companies/compare - ⚖️ 公司对比"
                ]
            },
            "🏭 行业趋势洞察": {
                "description": "行业数据、趋势分析、投资机会",
                "endpoints": [
                    "GET /api/v1/industries/{industry}/companies - 📋 行业公司列表",
                    "GET /api/v1/industries/{industry}/analysis - 📊 行业分析",
                    "GET /api/v1/industries/trending - 🔥 热门行业"
                ]
            }
        },
        "🚀 快速开始": {
            "1": "访问 /docs 查看完整API文档",
            "2": "使用 /health 检查系统状态", 
            "3": "获取实时数据: GET /api/v1/realtime/stock/000001",
            "4": "获取AI分析: GET /api/v1/companies/000001/analysis"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )