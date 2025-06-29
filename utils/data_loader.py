import json

def load_quran_data(filepath='quran_english.json'):
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)