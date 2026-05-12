import urllib.request
import json
import re

url = 'https://raw.githubusercontent.com/hefengxian/my-ielts/master/src/pages/vocabulary/vocabulary.js'
req = urllib.request.Request(url)
print("Downloading vocabulary.js...")
with urllib.request.urlopen(req) as response:
    content = response.read().decode('utf-8')

# Extract JSON from JS file
match = re.search(r'const\s+vocabulary\s*=\s*(\{.*?\});?\s*export\s+default', content, re.DOTALL)
if match:
    json_str = match.group(1)
else:
    print("Could not find 'const vocabulary = {...}' in the file.")
    exit(1)

try:
    data = json.loads(json_str)
    print("Successfully parsed JSON data.")
except Exception as e:
    print("Failed to parse JSON:", e)
    exit(1)

all_words = []
md_content = "# 雅思词汇全集\n\n"

for category_key, category_data in data.items():
    label = category_data.get('label', category_key)
    md_content += f"## {label}\n\n"
    md_content += "| 单词 | 词性 | 含义 | 例句 | 补充 |\n"
    md_content += "|---|---|---|---|---|\n"
    
    words_groups = category_data.get('words', [])
    for group in words_groups:
        for item in group:
            word_str = ", ".join(item.get('word', []))
            pos = item.get('pos', '')
            meaning = item.get('meaning', '')
            example = item.get('example', '')
            extra = item.get('extra', '')
            
            # Clean up newlines for markdown table
            example = example.replace('\n', ' ') if example else '-'
            extra = extra.replace('\n', ' ') if extra else '-'
            
            md_content += f"| {word_str} | {pos} | {meaning} | {example} | {extra} |\n"
            
            all_words.append({
                "category": label,
                "word": word_str,
                "pos": pos,
                "meaning": meaning,
                "example": example,
                "extra": extra
            })
    md_content += "\n"

# Save to JSON
with open('/Users/solo/Desktop/work/trae.ai/ai/ielts_vocabulary.json', 'w', encoding='utf-8') as f:
    json.dump(all_words, f, ensure_ascii=False, indent=2)

# Save to Markdown
with open('/Users/solo/Desktop/work/trae.ai/ai/ielts_vocabulary.md', 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"Successfully saved {len(all_words)} words to ielts_vocabulary.json and ielts_vocabulary.md")
