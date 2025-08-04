
import json
import pandas as pd

def create_excel_report():
    """
    Reads data from financial_data.json and cache.json,
    and creates an Excel report with multiple sheets.
    """
    try:
        # Load financial data
        with open('/Users/jiang/Desktop/my-projects/Industry_analyze/data/financial_data.json', 'r', encoding='utf-8') as f:
            financial_data = json.load(f)

        # Process financial data
        financial_records = []
        for stock_code, reports in financial_data.items():
            for report in reports:
                record = {'stock_code': stock_code, **report}
                financial_records.append(record)
        financial_df = pd.DataFrame(financial_records)

        # Load cache data
        with open('/Users/jiang/Desktop/my-projects/Industry_analyze/data/cache.json', 'r', encoding='utf-8') as f:
            cache_data = json.load(f)

        # Create an Excel writer
        with pd.ExcelWriter('/Users/jiang/Desktop/my-projects/Industry_analyze/data/analysis_data.xlsx', engine='openpyxl') as writer:
            # Write financial data to a sheet
            financial_df.to_excel(writer, sheet_name='Financial Data', index=False)

            # Process and write cache data
            stock_cache_records = []
            for key, value in cache_data.items():
                if key.startswith('industry_cache_'):
                    industry_name = key.replace('industry_cache_', '')
                    industry_df = pd.DataFrame(value['data'])
                    industry_df.to_excel(writer, sheet_name=f'Industry - {industry_name}', index=False)
                elif key.startswith('stock_cache_'):
                    stock_cache_records.append(value['data'])

            if stock_cache_records:
                stock_cache_df = pd.DataFrame(stock_cache_records)
                stock_cache_df.to_excel(writer, sheet_name='Stock Cache', index=False)

        print("Excel report 'analysis_data.xlsx' created successfully in the 'data' directory.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_excel_report()
