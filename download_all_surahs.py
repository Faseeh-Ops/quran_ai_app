import os
import requests
import json

# Base URLs for AlQuran.cloud
base_urls = {
    "en": "https://api.alquran.cloud/v1/surah",
    "ar": "https://api.alquran.cloud/v1/surah"
}
output_folder = "data/translations"
os.makedirs(output_folder, exist_ok=True)

total_ayats = 0

# Download English and Arabic translations
for lang in ["en", "ar"]:
    lang_folder = os.path.join(output_folder, lang)
    os.makedirs(lang_folder, exist_ok=True)

    for i in range(1, 115):
        edition = "en.sahih" if lang == "en" else "ar"
        url = f"{base_urls[lang]}/{i}/{edition}"
        file_name = f"{lang}_translation_{str(i).zfill(3)}.json"
        output_path = os.path.join(lang_folder, file_name)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Validate English text
                if lang == "en":
                    verses = data.get("data", {}).get("ayahs", [])
                    for verse in verses:
                        if any(char in verse["text"] for char in "ءآأؤإءبتثجحخدذرزسشصضطظعغفقكلمنهوى"):
                            print(f"⚠️ Arabic text detected in English file: {url}")
                            break
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"✅ Downloaded: {file_name}")
                if lang == "en":
                    ayats_count = len(data["data"]["ayahs"])
                    total_ayats += ayats_count
                    print(f"Surah {i}: {ayats_count} ayats")
            else:
                print(f"❌ Failed: {url} (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching {url} → {e}")

print(f"Total ayats downloaded: {total_ayats}")