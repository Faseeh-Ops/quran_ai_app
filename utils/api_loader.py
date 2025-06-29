import requests

def fetch_quran_from_cdn(translation='eng-sahih'):
    url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{translation}.json'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()['quran']
    else:
        raise Exception(f"Failed to fetch Qur’an. Status code: {response.status_code}")
