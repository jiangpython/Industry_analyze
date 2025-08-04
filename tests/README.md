# 测试文件说明

本目录包含项目的所有测试文件。

## 📁 测试文件列表

### 1. `test_basic.py`
- **作用**: 基础功能测试
- **内容**: 测试项目的基本配置和核心功能
- **运行**: `python tests/test_basic.py`

### 2. `test_all_modules.py`
- **作用**: 所有模块的完整性测试
- **内容**: 测试所有主要模块的功能
- **运行**: `python tests/test_all_modules.py`

### 3. `test_financial_fix.py`
- **作用**: 财务数据功能测试
- **内容**: 测试财务数据获取、处理和分析功能
- **运行**: `python tests/test_financial_fix.py`

### 4. `test_api_error.py`
- **作用**: API错误诊断测试
- **内容**: 诊断和测试API相关问题
- **运行**: `python tests/test_api_error.py`

### 5. `run_all_tests.py`
- **作用**: 统一测试运行脚本
- **内容**: 自动运行所有测试文件并生成报告
- **运行**: `python tests/run_all_tests.py`

## 🚀 运行测试

### 运行所有测试
```bash
python tests/run_all_tests.py
```

### 运行单个测试
```bash
# 基础测试
python tests/test_basic.py

# 财务功能测试
python tests/test_financial_fix.py

# API诊断测试
python tests/test_api_error.py

# 所有模块测试
python tests/test_all_modules.py
```

## 📊 测试覆盖范围

- ✅ **基础功能**: 项目配置、核心模块
- ✅ **财务数据**: 数据获取、处理、分析
- ✅ **API功能**: 接口测试、错误处理
- ✅ **模块集成**: 各模块间的协作

## 🔧 添加新测试

1. 在 `tests/` 目录下创建新的测试文件
2. 文件名格式: `test_*.py`
3. 在 `run_all_tests.py` 中添加新测试文件
4. 更新本README文件

## 📝 注意事项

- 测试文件应该独立运行
- 测试不应该依赖外部服务（除非必要）
- 测试应该清理自己创建的数据
- 测试输出应该清晰易懂 