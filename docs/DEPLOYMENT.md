# 部署说明

## 环境要求

- Python 3.8+
- Redis (可选，用于任务队列)
- PostgreSQL (可选，生产环境推荐)

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <your-repo-url>
cd 金融分析

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `env.example` 为 `.env` 并配置：

```bash
# 数据库配置 (开发阶段使用SQLite)
DATABASE_URL=sqlite:///./data/financial.db

# Redis配置 (可选)
REDIS_URL=redis://localhost:6379

# Gemini API配置 (必需)
GEMINI_API_KEY=your_gemini_api_key_here

# 其他配置
LOG_LEVEL=INFO
DEBUG=True
```

### 3. 初始化数据库

```bash
# 启动应用会自动创建数据库表
python run.py
```

### 4. 启动服务

```bash
# 方式1: 使用启动脚本
python run.py

# 方式2: 直接使用uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问API

- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## 生产环境部署

### 1. 使用PostgreSQL

```bash
# 安装PostgreSQL依赖
pip install psycopg2-binary

# 配置数据库URL
DATABASE_URL=postgresql://user:password@localhost/financial_db
```

### 2. 使用Redis (推荐)

```bash
# 安装Redis
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# 启动Redis
redis-server

# 配置Redis URL
REDIS_URL=redis://localhost:6379
```

### 3. 使用Gunicorn

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 4. 使用Docker (可选)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 多设备同步

### 1. 代码同步

使用Git仓库进行代码同步：

```bash
# 公司电脑
git add .
git commit -m "更新代码"
git push origin main

# 家里电脑
git pull origin main
```

### 2. 数据同步

#### 方案1: 云数据库 (推荐)

使用阿里云、腾讯云等云数据库服务：

```bash
# 配置云数据库连接
DATABASE_URL=postgresql://user:password@your-db-host:5432/financial_db
```

#### 方案2: 数据库备份同步

```bash
# 导出数据
pg_dump financial_db > backup.sql

# 导入数据
psql financial_db < backup.sql
```

## 定时任务配置

### 1. 使用Celery (推荐)

```bash
# 启动Celery工作进程
celery -A app.celery_app worker --loglevel=info

# 启动定时任务调度器
celery -A app.celery_app beat --loglevel=info
```

### 2. 使用系统Cron

```bash
# 编辑crontab
crontab -e

# 添加定时任务 (每天凌晨2点执行数据采集)
0 2 * * * cd /path/to/project && python -m app.tasks.daily_collection
```

## 监控和日志

### 1. 日志配置

```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
grep ERROR logs/app.log
```

### 2. 健康检查

```bash
# 检查服务状态
curl http://localhost:8000/health

# 检查API状态
curl http://localhost:8000/api/v1/
```

## 故障排除

### 1. 常见问题

**问题**: 数据库连接失败
```bash
# 检查数据库配置
echo $DATABASE_URL

# 测试数据库连接
python -c "from app.core.database import engine; print('数据库连接正常')"
```

**问题**: Gemini API调用失败
```bash
# 检查API密钥
echo $GEMINI_API_KEY

# 测试API连接
python -c "from app.services.analyzers.gemini_analyzer import GeminiAnalyzer; analyzer = GeminiAnalyzer(); print('API连接正常')"
```

**问题**: 端口被占用
```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>
```

### 2. 性能优化

- 使用连接池优化数据库连接
- 启用Redis缓存
- 使用异步处理提高并发性能
- 定期清理日志文件

## 安全建议

1. 生产环境中修改 `SECRET_KEY`
2. 配置防火墙规则
3. 使用HTTPS
4. 定期更新依赖包
5. 限制API访问频率 