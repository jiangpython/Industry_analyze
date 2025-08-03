# 金融分析系统

智能金融分析系统，专注于医药、新能源、半导体、芯片等行业的数据采集、处理和分析。

## 功能特性

- 📊 **数据采集**: 自动爬取上市公司财务数据
- 🔄 **数据处理**: 按业务逻辑处理和分析数据
- 🤖 **AI分析**: 使用Gemini API进行智能分析
- 📈 **趋势分析**: 财务指标和行业趋势分析
- 🌐 **API接口**: 提供RESTful API服务
- ⏰ **定时任务**: 支持定时数据更新

## 项目结构

```
financial-analysis/
├── app/                    # 主应用目录
│   ├── api/               # API接口
│   ├── core/              # 核心配置
│   ├── database/          # 数据库模型
│   ├── services/          # 业务服务
│   │   ├── collectors/    # 数据采集
│   │   ├── processors/    # 数据处理
│   │   └── analyzers/     # AI分析
│   └── utils/             # 工具函数
├── data/                  # 数据存储
├── logs/                  # 日志文件
├── tests/                 # 测试文件
└── config/                # 配置文件
```

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境

复制 `.env.example` 为 `.env` 并配置：

```bash
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost/financial_db

# Redis配置
REDIS_URL=redis://localhost:6379

# Gemini API配置
GEMINI_API_KEY=your_gemini_api_key

# 其他配置
LOG_LEVEL=INFO
```

### 3. 启动服务

```bash
# 启动API服务
uvicorn app.main:app --reload

# 启动Celery工作进程
celery -A app.celery_app worker --loglevel=info

# 启动定时任务
celery -A app.celery_app beat --loglevel=info
```

## API文档

启动服务后访问：http://localhost:8000/docs

## 行业关注

- 🏥 **医药行业**: 生物医药、医疗器械、医疗服务
- ⚡ **新能源**: 光伏、风电、储能、新能源汽车
- 🔌 **半导体**: 芯片设计、制造、封装测试
- 💻 **芯片**: 处理器、存储芯片、传感器

## 开发计划

- [x] 项目框架搭建
- [ ] 数据采集模块
- [ ] 数据处理模块
- [ ] AI分析模块
- [ ] API接口开发
- [ ] 定时任务配置
- [ ] 部署文档 