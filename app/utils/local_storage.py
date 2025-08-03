import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
from app.core.config_simple_local import local_settings

logger = logging.getLogger(__name__)


class LocalStorage:
    """本地文件存储工具"""
    
    def __init__(self):
        self.settings = local_settings
    
    def save_json(self, data: Dict[str, Any], filepath: str) -> bool:
        """保存JSON数据"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已保存到: {filepath}")
            return True
        except Exception as e:
            logger.error(f"保存JSON文件失败: {e}")
            return False
    
    def load_json(self, filepath: str) -> Optional[Dict[str, Any]]:
        """加载JSON数据"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"加载JSON文件失败: {e}")
            return {}
    
    def save_csv(self, data: List[Dict[str, Any]], filepath: str) -> bool:
        """保存CSV数据"""
        try:
            if not data:
                return False
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"CSV数据已保存到: {filepath}")
            return True
        except Exception as e:
            logger.error(f"保存CSV文件失败: {e}")
            return False
    
    def load_csv(self, filepath: str) -> List[Dict[str, Any]]:
        """加载CSV数据"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    return list(reader)
            return []
        except Exception as e:
            logger.error(f"加载CSV文件失败: {e}")
            return []
    
    def save_company(self, company_data: Dict[str, Any]) -> bool:
        """保存公司数据"""
        companies = self.load_json(self.settings.COMPANIES_FILE)
        company_id = company_data.get('code', company_data.get('id'))
        companies[company_id] = company_data
        return self.save_json(companies, self.settings.COMPANIES_FILE)
    
    def get_company(self, company_id: str) -> Optional[Dict[str, Any]]:
        """获取公司数据"""
        companies = self.load_json(self.settings.COMPANIES_FILE)
        return companies.get(company_id)
    
    def get_all_companies(self) -> Dict[str, Any]:
        """获取所有公司数据"""
        return self.load_json(self.settings.COMPANIES_FILE)
    
    def save_financial_data(self, company_id: str, financial_data: Dict[str, Any]) -> bool:
        """保存财务数据"""
        all_data = self.load_json(self.settings.FINANCIAL_DATA_FILE)
        if company_id not in all_data:
            all_data[company_id] = []
        
        # 添加时间戳
        financial_data['updated_at'] = datetime.now().isoformat()
        all_data[company_id].append(financial_data)
        
        return self.save_json(all_data, self.settings.FINANCIAL_DATA_FILE)
    
    def get_financial_data(self, company_id: str) -> List[Dict[str, Any]]:
        """获取公司财务数据"""
        all_data = self.load_json(self.settings.FINANCIAL_DATA_FILE)
        return all_data.get(company_id, [])
    
    def save_industry_data(self, industry_name: str, industry_data: Dict[str, Any]) -> bool:
        """保存行业数据"""
        all_data = self.load_json(self.settings.INDUSTRY_DATA_FILE)
        industry_data['updated_at'] = datetime.now().isoformat()
        all_data[industry_name] = industry_data
        return self.save_json(all_data, self.settings.INDUSTRY_DATA_FILE)
    
    def get_industry_data(self, industry_name: str) -> Optional[Dict[str, Any]]:
        """获取行业数据"""
        all_data = self.load_json(self.settings.INDUSTRY_DATA_FILE)
        return all_data.get(industry_name)
    
    def save_analysis_result(self, analysis_data: Dict[str, Any]) -> bool:
        """保存分析结果"""
        all_results = self.load_json(self.settings.ANALYSIS_RESULTS_FILE)
        analysis_id = f"{analysis_data.get('target_type')}_{analysis_data.get('target_id')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        analysis_data['id'] = analysis_id
        analysis_data['created_at'] = datetime.now().isoformat()
        all_results[analysis_id] = analysis_data
        return self.save_json(all_results, self.settings.ANALYSIS_RESULTS_FILE)
    
    def get_analysis_results(self, target_type: str = None, target_id: str = None) -> List[Dict[str, Any]]:
        """获取分析结果"""
        all_results = self.load_json(self.settings.ANALYSIS_RESULTS_FILE)
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
    
    def export_to_csv(self) -> bool:
        """导出数据到CSV文件"""
        try:
            # 导出公司数据
            companies = self.get_all_companies()
            if companies:
                company_list = []
                for company_id, company_data in companies.items():
                    company_data['id'] = company_id
                    company_list.append(company_data)
                self.save_csv(company_list, self.settings.COMPANIES_CSV)
            
            # 导出财务数据
            all_financial = self.load_json(self.settings.FINANCIAL_DATA_FILE)
            if all_financial:
                financial_list = []
                for company_id, financial_records in all_financial.items():
                    for record in financial_records:
                        record['company_id'] = company_id
                        financial_list.append(record)
                self.save_csv(financial_list, self.settings.FINANCIAL_DATA_CSV)
            
            logger.info("数据已导出到CSV文件")
            return True
        except Exception as e:
            logger.error(f"导出CSV失败: {e}")
            return False
    
    def backup_data(self, backup_dir: str = None) -> bool:
        """备份数据"""
        if not backup_dir:
            backup_dir = os.path.join(self.settings.DATA_DIR, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        try:
            os.makedirs(backup_dir, exist_ok=True)
            
            # 复制所有数据文件
            data_files = [
                self.settings.COMPANIES_FILE,
                self.settings.FINANCIAL_DATA_FILE,
                self.settings.INDUSTRY_DATA_FILE,
                self.settings.ANALYSIS_RESULTS_FILE
            ]
            
            for file_path in data_files:
                if os.path.exists(file_path):
                    import shutil
                    shutil.copy2(file_path, backup_dir)
            
            logger.info(f"数据已备份到: {backup_dir}")
            return True
        except Exception as e:
            logger.error(f"备份数据失败: {e}")
            return False


# 创建全局存储实例
local_storage = LocalStorage() 