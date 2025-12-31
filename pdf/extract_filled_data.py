import pandas as pd
import os

EXCEL_PATH = "/Users/solo/Desktop/work/trae.ai/ai/pdf/数据.xlsx"
OUTPUT_PATH = "/Users/solo/Desktop/work/trae.ai/ai/pdf/已提取数据.xlsx"
TARGET_SHEET = "公司数据"

# Target Columns that indicate data has been extracted
# We'll check if any of these are non-empty
CHECK_COLUMNS = [
    '实际资本', '认可资产', '认可负债', '最低资本', 
    '核心偿付能力充足率', '综合偿付能力充足率', 
    '保险业务收入', '净利润'
]

def extract_filled_rows():
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: {EXCEL_PATH} does not exist.")
        return

    try:
        # Load the Excel file
        df = pd.read_excel(EXCEL_PATH, sheet_name=TARGET_SHEET)
        
        print(f"Total rows in original file: {len(df)}")
        
        # Filter rows where at least one of the CHECK_COLUMNS is not null/empty
        # We assume if '实际资本' or others are filled, it's a valid extracted row
        # Some rows might be manually filled or pre-filled, so we check for non-null
        
        # Create a mask for non-null values in check columns
        mask = df[CHECK_COLUMNS].notna().any(axis=1)
        
        # Apply mask
        filled_df = df[mask]
        
        print(f"Rows with data: {len(filled_df)}")
        
        if len(filled_df) > 0:
            filled_df.to_excel(OUTPUT_PATH, index=False)
            print(f"Successfully saved filled data to: {OUTPUT_PATH}")
            
            # Print first few rows to verify
            print("\nPreview of extracted data:")
            print(filled_df[['公司名称', '时间', '实际资本', '风险综合评级']].head().to_string())
        else:
            print("No rows with data found.")

    except Exception as e:
        print(f"Error processing Excel: {e}")

if __name__ == "__main__":
    extract_filled_rows()
