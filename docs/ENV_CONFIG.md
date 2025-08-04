# 环境配置文件说明

## 概述

本项目使用 `.env` 文件来管理环境变量配置。为了安全起见，我们提供了 `env_template.txt` 作为配置模板。

**重要说明**: 本配置模板只包含 `Settings` 类中已定义的配置项，确保与代码完全兼容。

## 快速开始

### 1. 创建环境配置文件

```bash
# 复制模板文件为 .env
cp env_template.txt .env
```

### 2. 修改关键配置

编辑 `.env` 文件，至少需要修改以下配置：

```bash
# 生成安全的SECRET_KEY
SECRET_KEY=your-generated-secret-key-here

# 设置Gemini API密钥（如果需要AI分析功能）
GEMINI_API_KEY=your_actual_gemini_api_key

# 根据实际环境修改数据库配置
DATABASE_URL=sqlite:///./data/financial.db

# 如果使用Redis，修改Redis地址
REDIS_URL=redis://localhost:6379
```

## 配置分类说明

### 🔧 应用基础配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `DEBUG` | 调试模式开关 | `True` |
| `SECRET_KEY` | 应用密钥 | `your-secret-key-change-in-production` |

### 💾 数据存储配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `DATA_DIR` | 数据存储目录 | `./data` |
| `LOG_DIR` | 日志存储目录 | `./logs` |
| `DATABASE_URL` | 数据库连接URL | `sqlite:///./data/financial.db` |

### 🔑 API密钥配置

| 配置项 | 说明 | 必需性 |
|--------|------|--------|
| `GEMINI_API_KEY` | Gemini AI API密钥 | 可选 |

### 📊 数据源配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `EASTMONEY_BASE_URL` | 东方财富基础URL | `http://f10.eastmoney.com` |
| `THS_BASE_URL` | 同花顺基础URL | `http://basic.10jqka.com.cn` |
| `STATS_BASE_URL` | 国家统计局基础URL | `http://www.stats.gov.cn` |

### 🕷️ 爬虫配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `CRAWLER_DELAY` | 爬虫延迟时间（秒） | `1` |
| `CRAWLER_TIMEOUT` | 爬虫超时时间（秒） | `30` |
| `USER_AGENT` | 用户代理字符串 | Chrome浏览器UA |
| `REQUEST_RETRY_COUNT` | 请求重试次数 | `3` |

### 📈 行业分析配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `TARGET_INDUSTRIES` | 目标行业（逗号分隔） | `医药,新能源,半导体,芯片` |

### 📝 日志配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `LOG_LEVEL` | 日志级别 | `INFO` |
| `LOG_FILE` | 日志文件路径 | `./logs/app.log` |

## 环境特定配置

### 开发环境

```bash
# 开发环境推荐配置
DEBUG=True
LOG_LEVEL=DEBUG
```

### 生产环境

```bash
# 生产环境推荐配置
DEBUG=False
LOG_LEVEL=WARNING
SECRET_KEY=your-secure-production-secret-key
```

### 测试环境

```bash
# 测试环境推荐配置
LOG_LEVEL=DEBUG
```

## 安全注意事项

### 🔐 密钥管理

1. **SECRET_KEY**: 生产环境必须使用强随机字符串
2. **API密钥**: 不要在代码中硬编码，使用环境变量
3. **数据库密码**: 使用环境变量存储敏感信息

### 🛡️ 生产环境安全

```bash
# 生成安全的SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 设置强密码
SECRET_KEY=your-generated-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 配置验证

### 检查配置是否正确

```bash
# 运行配置检查
python setup_config.py
```

### 验证环境变量加载

```python
import os
from dotenv import load_dotenv

load_dotenv()
print(f"DEBUG: {os.getenv('DEBUG')}")
print(f"DATA_DIR: {os.getenv('DATA_DIR')}")
```

## 常见问题

### Q: 如何生成安全的SECRET_KEY？
A: 使用Python的secrets模块：
```python
import secrets
secret_key = secrets.token_urlsafe(32)
print(secret_key)
```

### Q: 如何设置不同环境的配置？
A: 可以创建多个配置文件：
- `.env.development`
- `.env.production`
- `.env.test`

### Q: 配置修改后需要重启吗？
A: 是的，环境变量修改后需要重启应用才能生效。

## 配置最佳实践

1. **版本控制**: 不要将包含敏感信息的 `.env` 文件提交到版本控制
2. **默认值**: 为所有配置项提供合理的默认值
3. **文档化**: 为每个配置项添加清晰的注释说明
4. **验证**: 在应用启动时验证关键配置项
5. **备份**: 定期备份配置文件

## 相关文件

- `env_template.txt`: 环境配置模板
- `setup_config.py`: 配置设置脚本
- `app/core/config.py`: 配置类定义
- `app/core/config_simple.py`: 简化配置类 