# 行业分析系统

## 项目结构

```
Industry_analyze/
├── app/                    # 主应用代码
│   ├── api/               # API端点
│   ├── services/          # 服务层
│   └── utils/             # 工具类
├── scripts/               # 脚本文件
│   ├── tests/            # 测试脚本
│   ├── demos/            # 演示脚本
│   └── research/         # 研究脚本
├── docs/                  # 文档文件
├── data/                  # 数据目录
├── logs/                  # 日志目录
├── tests/                 # 单元测试
├── examples/              # 示例代码
├── run.py                 # 主启动文件
├── requirements.txt       # 依赖文件
└── config_manager.py      # 配置管理
```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动服务
```bash
python run.py
```

### 3. 访问API
- 本地访问: http://localhost:8000
- API文档: http://localhost:8000/docs

## 脚本使用

### 测试脚本
```bash
# API功能测试
python scripts/tests/test_api.py

# 实时API测试
python scripts/tests/test_realtime_api.py

# 缓存优化测试
python scripts/tests/test_optimization.py
```

### 演示脚本
```bash
# 实时数据演示
python scripts/demos/realtime_usage_demo.py

# 增量数据演示
python scripts/demos/incremental_demo.py
```

### 研究脚本
```bash
# AKShare方法研究
python scripts/research/akshare_methods_research.py

# 项目文件分析
python scripts/research/project_files_analysis.py
```

## 文档

- [安装指南](docs/INSTALL.md)
- [部署指南](docs/DEPLOYMENT.md)
- [AKShare分析报告](docs/akshare_detailed_analysis.md)

## 开发说明

- 核心代码在 `app/` 目录
- 测试和演示脚本在 `scripts/` 目录
- 文档在 `docs/` 目录
- 数据文件在 `data/` 目录
