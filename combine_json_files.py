import os
import json

# Input and output paths
input_folders = {
    "en": "data/translations/en",
    "ar": "data/translations/ar"
}
output_file = "quran_english.json"

# Initialize list to store all verses
all_verses = []

# Loop through all 114 surahs
for i in range(1, 115):
    en_file = os.path.join(input_folders["en"], f"en_translation_{str(i).zfill(3)}.json")
    ar_file = os.path.join(input_folders["ar"], f"ar_translation_{str(i).zfill(3)}.json")

    if os.path.exists(en_file) and os.path.exists(ar_file):
        with open(en_file, "r", encoding="utf-8") as f_en, open(ar_file, "r", encoding="utf-8") as f_ar:
            en_data = json.load(f_en)
            ar_data = json.load(f_ar)
            surah_id = en_data["data"]["number"]
            surah_name = en_data["data"]["englishName"]
            surah_name_arabic = ar_data["data"]["name"]
            en_verses = en_data["data"]["ayahs"]
            ar_verses = ar_data["data"]["ayahs"]

            # Ensure both files have the same number of verses
            if len(en_verses) != len(ar_verses):
                print(
                    f"⚠️ Mismatch in verse count for Surah {surah_id}: English ({len(en_verses)}) vs Arabic ({len(ar_verses)})")
                continue

            for en_verse, ar_verse in zip(en_verses, ar_verses):
                # Verify English text is not Arabic
                if any(char in en_verse["text"] for char in "ءآأؤإءبتثجحخدذرزسشصضطظعغفقكلمنهوى"):
                    print(
                        f"⚠️ Arabic text detected in English translation for Surah {surah_id}:{en_verse['numberInSurah']}")
                    continue
                verse_entry = {
                    "surah": surah_id,
                    "ayah": en_verse["numberInSurah"],
                    "translation": en_verse["text"],
                    "arabic": ar_verse["text"],
                    "surah_name": surah_name,
                    "surah_name_arabic": surah_name_arabic
                }
                all_verses.append(verse_entry)
    else:
        print(f"⚠️ File missing: {en_file} or {ar_file}")

# Save combined data to quran_english.json
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_verses, f, ensure_ascii=False, indent=2)

print(f"✅ Created {output_file} with {len(all_verses)} verses")