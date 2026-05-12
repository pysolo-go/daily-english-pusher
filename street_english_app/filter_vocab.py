import json
import csv

# Target order of categories prefixes
target_prefixes = ["12", "09", "11", "10", "14", "05", "13", "20"]

# We will load the json, categorize the words, and sort them
with open('/Users/solo/Desktop/work/trae.ai/ai/street_english_app/ielts_vocabulary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ordered_words = []

for prefix in target_prefixes:
    # Find the exact category name that starts with this prefix
    matched_category = None
    for item in data:
        if item['category'].startswith(prefix + "_"):
            matched_category = item['category']
            break
            
    if matched_category:
        for item in data:
            if item['category'] == matched_category:
                ordered_words.append({
                    "word": item["word"],
                    "pos": item["pos"],
                    "meaning": item["meaning"],
                    "sentence": item["example"] if item["example"] != "-" else "",
                    "sentence_meaning": ""
                })

# Write to vocabulary.csv
csv_path = '/Users/solo/Desktop/work/trae.ai/ai/street_english_app/vocabulary.csv'
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["word", "pos", "meaning", "sentence", "sentence_meaning"])
    writer.writeheader()
    writer.writerows(ordered_words)

print(f"Successfully filtered and saved {len(ordered_words)} words to {csv_path}")
