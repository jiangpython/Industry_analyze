# 安装指南

## 🚀 快速安装

### 方法1：使用安装脚本（推荐）

```bash
# 运行自动安装脚本
python install_dependencies.py
```

### 方法2：手动安装

```bash
# 1. 创建虚拟环境
python -m venv .venv

# 2. 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

## 📦 依赖包说明

### Web框架和服务器
- **fastapi**: 现代化Python Web框架
- **uvicorn**: ASGI服务器，用于运行FastAPI应用
- **pydantic**: 数据验证和序列化
- **pydantic-settings**: 配置管理

### 数据处理和分析
- **pandas**: 数据分析和处理
- **numpy**: 数值计算
- **openpyxl**: Excel文件读写

### 金融数据采集
- **yfinance**: Yahoo Finance数据获取
- **akshare**: 中国A股市场数据

### 网络请求和爬虫
- **requests**: HTTP请求库
- **httpx**: 异步HTTP客户端
- **beautifulsoup4**: HTML解析
- **selenium**: 浏览器自动化
- **lxml**: XML/HTML解析器

### AI分析
- **google-generativeai**: Google Gemini AI接口

### 工具包
- **python-dotenv**: 环境变量管理
- **schedule**: 任务调度

### 开发工具
- **pytest**: 单元测试
- **black**: 代码格式化
- **flake8**: 代码检查

## 🔧 环境配置

### 1. 复制环境变量文件
```bash
cp env.example .env
```

### 2. 编辑配置文件
```bash
# 编辑.env文件，配置以下内容：
GEMINI_API_KEY=your_gemini_api_key_here
DEBUG=True
LOG_LEVEL=INFO
```

## 🎯 验证安装

### 1. 检查Python版本
```bash
python --version
# 建议Python 3.8+
```

### 2. 验证关键依赖
```bash
python -c "
import fastapi
import uvicorn
import pandas
import yfinance
import akshare
import google.generativeai
print('✅ 所有关键依赖安装成功!')
"
```

### 3. 启动服务测试
```bash
# 启动API服务
python run.py

# 在浏览器中访问
# http://localhost:8000/docs
```

## 🐛 常见问题

### 问题1：pip安装失败
**解决方案**：
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 问题2：yfinance安装失败
**解决方案**：
```bash
# 单独安装yfinance
pip install yfinance --upgrade

# 或者使用conda
conda install -c conda-forge yfinance
```

### 问题3：akshare安装失败
**解决方案**：
```bash
# 升级pip和setuptools
pip install --upgrade pip setuptools wheel

# 重新安装akshare
pip install akshare --upgrade
```

### 问题4：权限问题
**解决方案**：
```bash
# Windows: 以管理员身份运行
# Linux/Mac: 使用sudo
sudo pip install -r requirements.txt
```

## 📋 系统要求

### 最低要求
- Python 3.8+
- 内存: 4GB RAM
- 磁盘空间: 2GB

### 推荐配置
- Python 3.9+
- 内存: 8GB RAM
- 磁盘空间: 5GB

## 🌐 网络要求

### 必需的网络访问
- **Yahoo Finance**: 获取美股数据
- **AKShare**: 获取A股数据
- **Google Gemini API**: AI分析功能

### 代理设置（如需要）
```bash
# 设置代理环境变量
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

## 🔄 更新依赖

### 更新所有依赖
```bash
pip install -r requirements.txt --upgrade
```

### 更新特定包
```bash
pip install yfinance --upgrade
pip install akshare --upgrade
```

## 📊 安装验证

运行以下命令验证安装：

```bash
# 1. 运行安装脚本
python install_dependencies.py

# 2. 运行示例程序
#python example_local_storage.py

# 3. 启动API服务
python run.py

# 4. 访问API文档
# 浏览器打开: http://localhost:8000/docs
```

## ✅ 安装完成检查清单

- [ ] Python 3.8+ 已安装
- [ ] 虚拟环境已创建并激活
- [ ] 所有依赖包已安装
- [ ] 环境变量已配置
- [ ] API服务能正常启动
- [ ] 示例程序能正常运行
- [ ] 数据采集功能正常

## 🆘 获取帮助

如果遇到安装问题：

1. **检查错误信息**：仔细阅读错误输出
2. **查看日志**：检查 `logs/` 目录下的日志文件
3. **验证网络**：确保能访问外部API
4. **更新依赖**：尝试升级相关包
5. **重新安装**：删除虚拟环境重新安装

## 📞 技术支持

- 查看项目文档：`README.md`
- 查看API文档：`http://localhost:8000/docs`
- 运行测试：`python -m pytest tests/` 