import requests
import json

def fetch_quran_from_cdn():
    verses = []
    base_url = "https://api.alquran.cloud/v1/surah"
    for i in range(1, 115):
        try:
            en_response = requests.get(f"{base_url}/{i}/en.sahih", timeout=10)
            ar_response = requests.get(f"{base_url}/{i}/ar", timeout=10)
            if en_response.status_code == 200 and ar_response.status_code == 200:
                en_data = en_response.json()
                ar_data = ar_response.json()
                surah_id = en_data["data"]["number"]
                surah_name = en_data["data"]["englishName"]
                surah_name_arabic = ar_data["data"]["name"]
                en_verses = en_data["data"]["ayahs"]
                ar_verses = ar_data["data"]["ayahs"]
                if len(en_verses) != len(ar_verses):
                    print(f"⚠️ Mismatch in verse count for Surah {surah_id}")
                    continue
                for en_verse, ar_verse in zip(en_verses, ar_verses):
                    if any(char in en_verse["text"] for char in "ءآأؤإءبتثجحخدذرزسشصضطظعغفقكلمنهوى"):
                        print(f"⚠️ Arabic text in English translation for Surah {surah_id}:{en_verse['numberInSurah']}")
                        continue
                    verse_entry = {
                        "surah": surah_id,
                        "ayah": en_verse["numberInSurah"],
                        "translation": en_verse["text"],
                        "arabic": ar_verse["text"],
                        "surah_name": surah_name,
                        "surah_name_arabic": surah_name_arabic
                    }
                    verses.append(verse_entry)
            else:
                print(f"⚠️ Failed to fetch Surah {i}: English ({en_response.status_code}), Arabic ({ar_response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching Surah {i}: {e}")
    return verses