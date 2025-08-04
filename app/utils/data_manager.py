import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class DataManager:
    """本地数据管理器"""
    
    def __init__(self):
        self.data_dir = settings.DATA_DIR
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保数据目录存在"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _get_file_path(self, filename: str) -> str:
        """获取文件完整路径"""
        return os.path.join(self.data_dir, filename)
    
    def save_json(self, data: Dict[str, Any], filename: str) -> bool:
        """保存JSON数据"""
        try:
            filepath = self._get_file_path(filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已保存到: {filepath}")
            return True
        except Exception as e:
            logger.error(f"保存JSON文件失败: {e}")
            return False
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """加载JSON数据"""
        try:
            filepath = self._get_file_path(filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"加载JSON文件失败: {e}")
            return {}
    
    def save_csv(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """保存CSV数据"""
        try:
            if not data:
                return False
            
            filepath = self._get_file_path(filename)
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"CSV数据已保存到: {filepath}")
            return True
        except Exception as e:
            logger.error(f"保存CSV文件失败: {e}")
            return False
    
    def load_csv(self, filename: str) -> List[Dict[str, Any]]:
        """加载CSV数据"""
        try:
            filepath = self._get_file_path(filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    return list(reader)
            return []
        except Exception as e:
            logger.error(f"加载CSV文件失败: {e}")
            return []
    
    # 公司数据管理
    def save_company(self, company_data: Dict[str, Any]) -> bool:
        """保存公司数据"""
        companies = self.load_json("companies.json")
        company_id = company_data.get('code', company_data.get('id'))
        companies[company_id] = company_data
        return self.save_json(companies, "companies.json")
    
    def get_company(self, company_id: str) -> Optional[Dict[str, Any]]:
        """获取公司数据"""
        companies = self.load_json("companies.json")
        return companies.get(company_id)
    
    def get_all_companies(self) -> Dict[str, Any]:
        """获取所有公司数据"""
        return self.load_json("companies.json")
    
    def delete_company(self, company_id: str) -> bool:
        """删除公司数据"""
        companies = self.load_json("companies.json")
        if company_id in companies:
            del companies[company_id]
            return self.save_json(companies, "companies.json")
        return False
    
    # 财务数据管理
    def save_financial_data(self, company_id: str, financial_data: Dict[str, Any]) -> bool:
        """保存财务数据"""
        all_data = self.load_json("financial_data.json")
        if company_id not in all_data:
            all_data[company_id] = []
        
        # 添加时间戳
        financial_data['updated_at'] = datetime.now().isoformat()
        all_data[company_id].append(financial_data)
        
        return self.save_json(all_data, "financial_data.json")
    
    def get_financial_data(self, company_id: str) -> List[Dict[str, Any]]:
        """获取公司财务数据"""
        all_data = self.load_json("financial_data.json")
        return all_data.get(company_id, [])
    
    def delete_financial_data(self, company_id: str, data_id: str = None) -> bool:
        """删除财务数据"""
        all_data = self.load_json("financial_data.json")
        if company_id in all_data:
            if data_id:
                # 删除特定记录
                all_data[company_id] = [item for item in all_data[company_id] 
                                      if item.get('id') != data_id]
            else:
                # 删除所有记录
                del all_data[company_id]
            return self.save_json(all_data, "financial_data.json")
        return False
    
    # 行业数据管理
    def save_industry_data(self, industry_name: str, industry_data: Dict[str, Any]) -> bool:
        """保存行业数据"""
        all_data = self.load_json("industry_data.json")
        industry_data['updated_at'] = datetime.now().isoformat()
        all_data[industry_name] = industry_data
        return self.save_json(all_data, "industry_data.json")
    
    def get_industry_data(self, industry_name: str) -> Optional[Dict[str, Any]]:
        """获取行业数据"""
        all_data = self.load_json("industry_data.json")
        return all_data.get(industry_name)
    
    def get_all_industries(self) -> Dict[str, Any]:
        """获取所有行业数据"""
        return self.load_json("industry_data.json")
    
    # 分析结果管理
    def save_analysis_result(self, analysis_data: Dict[str, Any]) -> bool:
        """保存分析结果"""
        all_results = self.load_json("analysis_results.json")
        analysis_id = f"{analysis_data.get('target_type')}_{analysis_data.get('target_id')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        analysis_data['id'] = analysis_id
        analysis_data['created_at'] = datetime.now().isoformat()
        all_results[analysis_id] = analysis_data
        return self.save_json(all_results, "analysis_results.json")
    
    def get_analysis_results(self, target_type: str = None, target_id: str = None) -> List[Dict[str, Any]]:
        """获取分析结果"""
        all_results = self.load_json("analysis_results.json")
        results = []
        
        for result in all_results.values():
            if target_type and result.get('target_type') != target_type:
                continue
            if target_id and result.get('target_id') != target_id:
                continue
            results.append(result)
        
        # 按时间排序
        results.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return results
    
    # 数据导出功能
    def export_to_excel(self, filename: str = None) -> bool:
        """导出数据到Excel文件"""
        try:
            import pandas as pd
            
            if not filename:
                filename = f"financial_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            filepath = self._get_file_path(filename)
            
            # 准备数据
            data_sheets = {}
            
            # 公司数据
            companies = self.get_all_companies()
            if companies:
                company_list = []
                for company_id, company_data in companies.items():
                    company_data['id'] = company_id
                    company_list.append(company_data)
                data_sheets['companies'] = pd.DataFrame(company_list)
            
            # 财务数据
            all_financial = self.load_json("financial_data.json")
            if all_financial:
                financial_list = []
                for company_id, financial_records in all_financial.items():
                    for record in financial_records:
                        record['company_id'] = company_id
                        financial_list.append(record)
                data_sheets['financial_data'] = pd.DataFrame(financial_list)
            
            # 行业数据
            industries = self.get_all_industries()
            if industries:
                industry_list = []
                for industry_name, industry_data in industries.items():
                    industry_data['industry_name'] = industry_name
                    industry_list.append(industry_data)
                data_sheets['industry_data'] = pd.DataFrame(industry_list)
            
            # 分析结果
            analysis_results = self.load_json("analysis_results.json")
            if analysis_results:
                analysis_list = []
                for result_id, result_data in analysis_results.items():
                    result_data['result_id'] = result_id
                    analysis_list.append(result_data)
                data_sheets['analysis_results'] = pd.DataFrame(analysis_list)
            
            # 保存到Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                for sheet_name, df in data_sheets.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            logger.info(f"数据已导出到Excel文件: {filepath}")
            return True
        except Exception as e:
            logger.error(f"导出Excel失败: {e}")
            return False
    
    def backup_data(self, backup_dir: str = None) -> bool:
        """备份数据"""
        if not backup_dir:
            backup_dir = os.path.join(self.data_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        try:
            os.makedirs(backup_dir, exist_ok=True)
            
            # 复制所有数据文件
            data_files = [
                "companies.json",
                "financial_data.json",
                "industry_data.json",
                "analysis_results.json"
            ]
            
            for filename in data_files:
                filepath = self._get_file_path(filename)
                if os.path.exists(filepath):
                    import shutil
                    shutil.copy2(filepath, backup_dir)
            
            logger.info(f"数据已备份到: {backup_dir}")
            return True
        except Exception as e:
            logger.error(f"备份数据失败: {e}")
            return False
    
    def get_data_summary(self) -> Dict[str, Any]:
        """获取数据摘要"""
        summary = {
            "companies": len(self.get_all_companies()),
            "industries": len(self.get_all_industries()),
            "analysis_results": len(self.load_json("analysis_results.json")),
            "total_financial_records": 0
        }
        
        # 计算财务记录总数
        all_financial = self.load_json("financial_data.json")
        for company_records in all_financial.values():
            summary["total_financial_records"] += len(company_records)
        
        return summary
    
    # 缓存数据管理
    def save_cache_data(self, cache_key: str, data: Any) -> bool:
        """保存缓存数据"""
        try:
            cache_data = self.load_json("cache.json")
            cache_data[cache_key] = {
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
            return self.save_json(cache_data, "cache.json")
        except Exception as e:
            logger.error(f"保存缓存数据失败: {e}")
            return False
    
    def get_cache_data(self, cache_key: str) -> Optional[Any]:
        """获取缓存数据"""
        try:
            cache_data = self.load_json("cache.json")
            cache_item = cache_data.get(cache_key)
            if cache_item:
                return cache_item.get("data")
            return None
        except Exception as e:
            logger.error(f"获取缓存数据失败: {e}")
            return None
    
    def clear_cache(self, cache_key: str = None) -> bool:
        """清除缓存数据"""
        try:
            if cache_key:
                # 清除指定缓存
                cache_data = self.load_json("cache.json")
                if cache_key in cache_data:
                    del cache_data[cache_key]
                    return self.save_json(cache_data, "cache.json")
            else:
                # 清除所有缓存
                return self.save_json({}, "cache.json")
        except Exception as e:
            logger.error(f"清除缓存失败: {e}")
            return False
    
    def get_cache_info(self) -> Dict[str, Any]:
        """获取缓存信息"""
        try:
            cache_data = self.load_json("cache.json")
            cache_info = {}
            for key, value in cache_data.items():
                cache_info[key] = {
                    "timestamp": value.get("timestamp"),
                    "data_type": type(value.get("data")).__name__
                }
            return cache_info
        except Exception as e:
            logger.error(f"获取缓存信息失败: {e}")
            return {}


# 创建全局数据管理器实例
data_manager = DataManager() 