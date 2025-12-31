import os
import json
import time
import base64
import pandas as pd
import fitz  # PyMuPDF
from openai import OpenAI
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# Load API key
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")

if not API_KEY:
    print("Error: OPENAI_API_KEY not found in .env file.")
    exit(1)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

MODEL_NAME = "Qwen/Qwen2-VL-72B-Instruct"

EXCEL_PATH = "/Users/solo/Desktop/work/trae.ai/ai/pdf/数据.xlsx"
TARGET_SHEET = "公司数据"

# Target Columns to extract
TARGET_COLUMNS = [
    '实际资本', '认可资产', '认可负债', '最低资本', 
    '核心偿付能力充足率', '综合偿付能力充足率', 
    '保险业务收入', '净利润', '总资产', '净资产', 
    '保险合同负债', '基本每股收益', '净资产收益率', 
    '总资产收益率', '投资收益率', '综合投资收益率', 
    '综合退保率', '股权集中度', '基本情境下流动性覆盖率LCR1', '业务结构',
    '风险综合评级'
]

def find_relevant_pages(doc, keywords=None):
    if keywords is None:
        keywords = {
            "main": ["主要指标", "Main Indicators", "Core Solvency Adequacy Ratio"],
            "specific": ["风险综合评级", "流动性覆盖率", "投资收益率", "综合退保率", "股权", "业务结构"]
        }
    
    relevant_indices = set()
    for i, page in enumerate(doc):
        text = page.get_text()
        
        # Check main keywords (often tables spanning pages)
        if any(k in text for k in keywords["main"]):
            relevant_indices.add(i)
            if i + 1 < len(doc):
                relevant_indices.add(i + 1)
        
        # Check specific keywords
        if any(k in text for k in keywords["specific"]):
            relevant_indices.add(i)
    
    # Always include first 2 pages for basic info (Company, Time)
    relevant_indices.add(0)
    relevant_indices.add(1)
            
    # If not found, default to first 5 pages
    if not relevant_indices:
        return list(range(min(len(doc), 5)))
        
    return sorted(list(relevant_indices))

def pdf_pages_to_base64(pdf_path):
    """Converts relevant PDF pages to a list of base64 images."""
    images = []
    try:
        doc = fitz.open(pdf_path)
        indices = find_relevant_pages(doc)
        print(f"DEBUG: Extracting pages {indices} for {os.path.basename(pdf_path)}")
        
        for i in indices:
            page = doc.load_page(i)
            # Higher resolution for better OCR
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_data = pix.tobytes("png")
            base64_str = base64.b64encode(img_data).decode("utf-8")
            images.append(base64_str)
        doc.close()
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return images

def extract_financial_data(pdf_path):
    print(f"Extracting data from: {os.path.basename(pdf_path)}...")
    images = pdf_pages_to_base64(pdf_path)
    
    if not images:
        return None

    # Batch processing to avoid 500 errors and rate limits
    BATCH_SIZE = 3
    merged_data = {col: None for col in ["公司名称", "时间"] + TARGET_COLUMNS}
    
    for i in range(0, len(images), BATCH_SIZE):
        batch_images = images[i : i + BATCH_SIZE]
        print(f"DEBUG: Processing batch {i//BATCH_SIZE + 1} ({len(batch_images)} images)...")
        
        # Construct Prompt
        columns_str = ", ".join(TARGET_COLUMNS)
        prompt = f"""
        你是一个专业的金融数据分析师。请仔细阅读这份偿付能力报告（图片片段）。
        请提取以下字段的信息，如果报告中没有明确提到某字段，请填 null。
        
        需要提取的字段:
        1. 公司名称 (Company Name) - 请提取完整的中文名称
        2. 时间 (Time) - 格式为 YYYYQx (例如 2016Q1, 2023Q3)。通常在标题或报告期中提及。
        3. {columns_str}
        
        特别说明:
        - **股权集中度**: 请提取**第一大股东持股比例**（例如 "45.00%"）。如果报告中列出了股东持股情况，请找到持股比例最高的股东，并提取其百分比。如果表格中为空，请仔细阅读表格下方的注脚或段落文本。
        - **风险综合评级**: 请留意文本描述或表格。结果通常为字母等级（如 A, B, BB, C, D 等）。例如文中提到“本季度风险综合评级结果为BB”，请提取“BB”。该信息经常出现在“风险管理能力”或“主要指标”章节的文字描述中，请仔细查找。
        - **空值处理**: 请尽力查找。只有在全文（包括所有提取的图片）都找不到相关信息时，才填 null。

        输出要求:
        - 直接返回一个 JSON 对象。
        - 键名必须与上述字段名完全一致（中文）。
        - 数值请保留原格式（带百分号的保留百分号，单位如果是万元/亿元请统一转换为**元**，或者直接提取原始数字并在备注中说明单位，为了简单起见，请**提取原始数值字符串**，不要自己换算，保持原样）。
        - 示例格式:
        {{
            "公司名称": "某某人寿保险股份有限公司",
            "时间": "2016Q1",
            "实际资本": "12345.67万元",
            "核心偿付能力充足率": "150%",
            "股权集中度": "45.00%"
            ...
        }}
        """

        content_blocks = [{"type": "text", "text": prompt}]
        for img in batch_images:
            content_blocks.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{img}"}
            })

        # Retry logic for API calls
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": content_blocks}],
                    temperature=0.1,
                    max_tokens=4096,
                )
                content = response.choices[0].message.content.strip()
                
                # Clean markdown
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                    
                batch_data = json.loads(content.strip())
                print(f"DEBUG: Batch Result keys: {list(batch_data.keys())}")
                
                # Merge data
                for key, val in batch_data.items():
                    if val is not None and val != "null" and val != "":
                        if merged_data.get(key) is None:
                            merged_data[key] = val
                        # If both exist, keep the one that looks "better" (e.g. longer string for text)
                        elif isinstance(val, str) and merged_data.get(key) and len(val) > len(str(merged_data[key])):
                             merged_data[key] = val
                break # Success, exit retry loop
                    
            except Exception as e:
                print(f"AI Extraction Error in batch (Attempt {attempt+1}): {e}")
                if "429" in str(e) or "rate limit" in str(e).lower():
                    wait_time = (attempt + 1) * 20
                    print(f"Rate limit hit. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    time.sleep(5)
            
        # Add sleep between batches to respect rate limits
        print("Sleeping for 20 seconds between batches...")
        time.sleep(20)
            
    print(f"DEBUG: Final Merged Data Sample: {str(merged_data)[:200]}...") 
    return merged_data

def clean_company_name(name):
    """
    Cleans company name for matching.
    1. Removes common suffixes.
    2. Removes common prefixes like "中国".
    Example: "中国平安人寿保险股份有限公司" -> "平安人寿"
    """
    if not name:
        return ""
    
    cleaned = name.strip()
    
    # Common suffixes to remove (longest first)
    suffixes = [
        "保险股份有限公司",
        "保险有限责任公司",
        "保险有限公司",
        "股份有限公司",
        "有限责任公司",
        "保险公司", 
        "有限公司",
    ]
    
    for suffix in suffixes:
        if cleaned.endswith(suffix):
            cleaned = cleaned[:-len(suffix)]
            break 
            
    # Remove common prefixes
    prefixes = ["中国"]
    for prefix in prefixes:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]
            
    return cleaned.strip()

def find_matching_row(df, pdf_company, pdf_time):
    """
    Finds the matching row index in the DataFrame.
    Strategy:
    1. Filter by Time (Time must match exactly).
    2. Check if Excel Company Name is a substring of PDF Company Name (or cleaned version).
       e.g. Excel: "平安人寿" is in PDF: "中国平安人寿" -> Match!
    """
    
    # Pre-clean PDF company name
    cleaned_pdf_company = clean_company_name(pdf_company)
    
    for idx, row in df.iterrows():
        row_company = str(row['公司名称']).strip()
        row_time = str(row['时间']).strip()
        
        # Skip header/alias rows
        if row_company in ['Company', '公司名称', 'nan', 'None']:
            continue
            
        # 1. Time Match (Exact)
        if row_time != pdf_time:
            continue
            
        # 2. Company Match (Loose/Containment)
        # Strategy:
        # A. Exact Match (cleaned vs row)
        if row_company == cleaned_pdf_company:
            return idx, row_company
            
        # B. Containment Match (User Request)
        # If PDF name contains Excel name (e.g. "中国人寿养老保险" contains "中国人寿")
        # Or Excel name contains PDF name
        if row_company in pdf_company or pdf_company in row_company:
             return idx, row_company
             
        # C. Cleaned Containment Match (Backup)
        if row_company in cleaned_pdf_company or cleaned_pdf_company in row_company:
             return idx, row_company
             
    return None, None

def update_excel(pdf_paths):
    # Load Excel
    try:
        # Load all sheets to preserve them
        xls = pd.ExcelFile(EXCEL_PATH)
        sheets = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
        
        df = sheets[TARGET_SHEET]
        
        # Ensure all target columns exist
        for col in TARGET_COLUMNS:
            if col not in df.columns:
                print(f"Adding missing column: {col}")
                df[col] = None
                
    except Exception as e:
        print(f"Error loading Excel: {e}")
        return

    # Process PDFs
    for pdf_path in pdf_paths:
        data = extract_financial_data(pdf_path)
        if not data:
            continue
        
        company_name = data.get("公司名称", "")
        time_period = data.get("时间", "")
        
        if not company_name or not time_period:
            print(f"Skipping {pdf_path}: Missing Company Name or Time.")
            continue
            
        print(f"Extracted: {company_name} - {time_period}")
        
        # Find matching row using helper function
        match_idx, match_name = find_matching_row(df, company_name, time_period)
        
        if match_idx is not None:
            print(f"  -> Matched with Excel row {match_idx}: {match_name}")
            # Update values
            for col in TARGET_COLUMNS:
                val = data.get(col)
                if val is not None and val != "null":
                    # Clear old data first? User said "删除之前提取到的数据" (delete previously extracted data)
                    # "重新提取" (re-extract). 
                    # So we should overwrite.
                    print(f"    Updating {col}: {val}")
                    df.at[match_idx, col] = val
        else:
            print(f"  -> No matching row found for {company_name} {time_period}. Skipping (No new rows allowed).")

    # Save back to Excel
    try:
        with pd.ExcelWriter(EXCEL_PATH, engine='openpyxl') as writer:
            for sheet_name, sheet_df in sheets.items():
                if sheet_name == TARGET_SHEET:
                    sheet_df = df # Use updated DF
                sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Successfully updated {EXCEL_PATH}")
    except Exception as e:
        print(f"Error saving Excel: {e}")

if __name__ == "__main__":
    data_dir = "/Users/solo/Desktop/work/trae.ai/ai/pdf/data"
    all_pdfs = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.lower().endswith('.pdf')]
    # Sort to ensure deterministic order (optional)
    all_pdfs.sort()
    
    # Process first 10 PDFs
    target_pdfs = all_pdfs[:10]
    print(f"Found {len(all_pdfs)} PDFs. Processing first {len(target_pdfs)}...")
    
    update_excel(target_pdfs)
