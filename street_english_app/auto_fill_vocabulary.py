import pandas as pd
import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(override=True)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "vocabulary.csv")

# OpenAI Config
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# Initialize Client
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def generate_content(words_data):
    """
    Generate sentences and translations for a list of words.
    words_data: List of dicts [{'word': 'apple', 'meaning': 'apple_meaning'}]
    """
    
    prompt = f"""
    I have a list of English words. For each word, I need:
    1. A simple, natural English example sentence containing the word.
    2. The Chinese translation of that sentence.

    Please output a JSON array of objects, where each object has:
    - "word": The original word
    - "sentence": The English example sentence
    - "sentence_meaning": The Chinese translation

    Words to process:
    {json.dumps(words_data, ensure_ascii=False)}

    Output ONLY the JSON array.
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3", # Trying a common SiliconFlow model
            messages=[
                {"role": "system", "content": "You are a helpful English teacher."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"} 
        )
        
        content = response.choices[0].message.content
        # Sometimes models wrap JSON in markdown blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
             content = content.split("```")[1].split("```")[0]
             
        # Handle cases where the model might return a wrapped object like {"words": [...]} instead of array
        data = json.loads(content)
        if isinstance(data, dict):
            # Try to find the list inside
            for key in data:
                if isinstance(data[key], list):
                    return data[key]
            return []
        return data

    except Exception as e:
        print(f"Error generating content: {e}")
        return []

def main():
    if not API_KEY:
        print("Error: OPENAI_API_KEY not found in .env")
        return

    print(f"Loading {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)

    # Ensure columns exist
    if 'sentence' not in df.columns:
        df['sentence'] = ""
    if 'sentence_meaning' not in df.columns:
        df['sentence_meaning'] = ""

    # Find rows needing update (missing sentence OR missing translation)
    # We treat empty string or NaN as missing
    mask = (
        (df['sentence'].isna()) | (df['sentence'] == "") |
        (df['sentence_meaning'].isna()) | (df['sentence_meaning'] == "")
    )
    
    pending_df = df[mask]
    total_pending = len(pending_df)
    print(f"Found {total_pending} words needing sentences/translations.")

    if total_pending == 0:
        print("All words already have sentences and translations!")
        return

    BATCH_SIZE = 10
    
    # Process in batches
    for i in range(0, total_pending, BATCH_SIZE):
        batch_indices = pending_df.index[i : i + BATCH_SIZE]
        batch_rows = df.loc[batch_indices]
        
        words_input = []
        for _, row in batch_rows.iterrows():
            words_input.append({
                "word": row['word'],
                "meaning": row['meaning']
            })
            
        print(f"Processing batch {i//BATCH_SIZE + 1}/{(total_pending + BATCH_SIZE - 1)//BATCH_SIZE}: {[w['word'] for w in words_input]}")
        
        results = generate_content(words_input)
        
        if results:
            for item in results:
                word = item.get('word')
                sentence = item.get('sentence')
                sentence_meaning = item.get('sentence_meaning')
                
                # Update DataFrame
                # Find index for this word (handle potential duplicates by taking first match in batch indices)
                # Ideally, word is unique.
                mask_word = (df['word'] == word) & (df.index.isin(batch_indices))
                if mask_word.any():
                    df.loc[mask_word, 'sentence'] = sentence
                    df.loc[mask_word, 'sentence_meaning'] = sentence_meaning
                    
            # Save progress after each batch
            df.to_csv(CSV_PATH, index=False)
            print("  -> Saved batch results.")
        else:
            print("  -> Failed to get results for this batch.")
        
        # Rate limit pause
        time.sleep(1)

    print("Done! All words processed.")

if __name__ == "__main__":
    main()
