import pandas as pd
import os

SOURCE_FILE = "/Users/solo/Desktop/work/trae.ai/ai/pdf/数据.xlsx"
OUTPUT_FILE = "/Users/solo/Desktop/work/trae.ai/ai/pdf/数据_extracted.xlsx"
TARGET_SHEET = "公司数据"

# Target Columns from fill_financial_data.py
TARGET_COLUMNS = [
    '实际资本', '认可资产', '认可负债', '最低资本', 
    '核心偿付能力充足率', '综合偿付能力充足率', 
    '保险业务收入', '净利润', '总资产', '净资产', 
    '保险合同负债', '基本每股收益', '净资产收益率', 
    '总资产收益率', '投资收益率', '综合投资收益率', 
    '综合退保率', '股权集中度', '基本情境下流动性覆盖率LCR1', '业务结构',
    '风险综合评级'
]

def filter_data():
    print(f"Reading from {SOURCE_FILE}...")
    if not os.path.exists(SOURCE_FILE):
        print(f"File not found: {SOURCE_FILE}")
        return

    try:
        # Load the specific sheet
        df = pd.read_excel(SOURCE_FILE, sheet_name=TARGET_SHEET)
        
        # Check which of the target columns exist in df
        existing_cols = [col for col in TARGET_COLUMNS if col in df.columns]
        
        if not existing_cols:
            print("No target columns found in the Excel file.")
            # Still save the file? Or return?
            # User wants to see extracted data. If no columns, nothing extracted.
            return

        print(f"Found {len(existing_cols)} target columns in Excel.")

        # Create a condition: at least one of the target columns has a non-null, non-empty value
        condition = pd.Series([False] * len(df))
        
        for col in existing_cols:
            # Check for not NaN/None
            not_na = df[col].notna()
            
            # Check for empty strings if the column contains strings
            # We can coerce to string and check length, or just check inequality
            # Safe way:
            is_valid = not_na & (df[col].astype(str).str.strip() != "") & (df[col].astype(str).str.lower() != "nan") & (df[col].astype(str).str.lower() != "null")
            
            condition = condition | is_valid
            
        filtered_df = df[condition]
        
        print(f"Original rows: {len(df)}")
        print(f"Rows with extracted data: {len(filtered_df)}")
        
        if not filtered_df.empty:
            # Save to new Excel file
            filtered_df.to_excel(OUTPUT_FILE, index=False)
            print(f"Successfully saved filtered data to {OUTPUT_FILE}")
        else:
            print("No rows with extracted data found.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    filter_data()
