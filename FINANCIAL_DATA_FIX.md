# 财务数据采集功能修复说明

## 问题分析

### 原始问题
用户请求财务数据时，系统直接返回404错误，没有自动启动数据采集。

### 根本原因
1. **缺少自动采集逻辑**：当本地没有数据时，直接返回错误
2. **实时数据服务未实现**：`RealtimeDataService` 的财务数据获取方法被注释
3. **没有降级采集机制**：缺少从网络自动采集数据的逻辑

## 修复内容

### 1. 实现财务数据采集服务

**文件**: `app/services/realtime_data_service.py`

新增方法：
- `get_financial_data()` - 获取公司财务数据（混合模式）
- `_fetch_financial_data()` - 从AKShare采集财务数据

**采集逻辑**：
```python
def get_financial_data(self, company_code: str, force_refresh: bool = False):
    # 1. 检查本地缓存
    # 2. 实时采集财务数据
    # 3. 保存到本地
    # 4. 降级到本地存储
```

### 2. 修复API端点逻辑

**文件**: `app/api/endpoints/companies_simple.py`

**修复前**：
```python
if not financial_records:
    raise HTTPException(status_code=404, detail="未找到财务数据")
```

**修复后**：
```python
# 1. 优先尝试实时数据采集
if force_refresh:
    financial_records = realtime_service.get_financial_data(company_code, force_refresh)

# 2. 如果本地没有数据，自动启动采集
if not financial_records:
    financial_records = data_manager.get_financial_data(company_code)
    
    # 如果本地也没有数据，尝试实时采集
    if not financial_records:
        financial_records = realtime_service.get_financial_data(company_code, force_refresh=True)

# 3. 如果仍然没有数据，返回错误
if not financial_records:
    raise HTTPException(status_code=404, detail=f"未找到公司 {company_code} 的财务数据")
```

### 3. 数据采集功能

**支持的财务数据**：
- 资产负债表
- 利润表  
- 现金流量表

**数据源**：AKShare
**数据格式**：JSON
**存储位置**：`data/financial_data.json`

## 新的工作流程

### 用户请求财务数据时的处理流程：

```
用户请求财务数据
    ↓
检查本地缓存
    ↓
本地有数据？ → 返回本地数据
    ↓ 否
尝试实时数据采集
    ↓
采集成功？ → 保存到本地并返回
    ↓ 否
尝试本地数据采集（AKShare等）
    ↓
采集成功？ → 保存到本地并返回
    ↓ 否
返回404错误（包含详细错误信息）
```

### 支持的操作模式：

1. **智能模式**（默认）
   ```bash
   GET /api/v1/companies/000999/financial-data
   ```
   - 优先使用本地缓存
   - 本地无数据时自动采集

2. **强制刷新模式**
   ```bash
   GET /api/v1/companies/000999/financial-data?force_refresh=true
   ```
   - 强制重新采集数据
   - 忽略本地缓存

3. **筛选模式**
   ```bash
   GET /api/v1/companies/000999/financial-data?data_type=quarterly&start_date=2023-01-01&end_date=2025-01-01
   ```
   - 按数据类型筛选
   - 按时间范围筛选

## 测试验证

### 测试脚本
运行 `test_financial_data.py` 来验证修复：

```bash
python test_financial_data.py
```

### 手动测试
```bash
# 测试自动采集
curl -X GET "http://localhost:8000/api/v1/companies/000999/financial-data"

# 测试强制刷新
curl -X GET "http://localhost:8000/api/v1/companies/000999/financial-data?force_refresh=true"

# 测试筛选功能
curl -X GET "http://localhost:8000/api/v1/companies/000999/financial-data?data_type=quarterly&start_date=2023-01-01&end_date=2025-01-01"
```

## 性能优化

### 缓存策略
- **本地缓存**：财务数据永久保存
- **实时缓存**：5分钟有效期
- **智能更新**：只获取缺失的数据

### 错误处理
- **网络异常**：自动降级到本地数据
- **数据源异常**：提供详细错误信息
- **格式异常**：自动数据清洗和转换

## 使用建议

### 1. 首次使用
```bash
# 启动服务器
python run.py

# 测试数据采集
curl -X GET "http://localhost:8000/api/v1/companies/000001/financial-data"
```

### 2. 批量采集
```bash
# 可以同时请求多个公司的数据
# 系统会自动并行处理
```

### 3. 数据管理
```bash
# 查看本地数据
ls -la data/

# 清理缓存
rm data/cache.json
```

## 注意事项

1. **网络依赖**：首次采集需要网络连接
2. **数据源限制**：依赖AKShare数据源的可用性
3. **采集时间**：首次采集可能需要几秒钟
4. **数据准确性**：建议验证采集的数据准确性

## 总结

✅ **修复完成**
- 实现了自动数据采集功能
- 修复了API端点的逻辑问题
- 添加了完整的错误处理机制
- 提供了测试验证工具

现在您的系统具备了完整的财务数据采集能力！🎉 