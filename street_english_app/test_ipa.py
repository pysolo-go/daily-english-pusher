import eng_to_ipa as ipa
words = ["granite", "gust", "breeze"]
for w in words:
    print(f"{w}: {ipa.convert(w)}")
