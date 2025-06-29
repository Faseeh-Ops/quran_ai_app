def search_by_keyword(keyword, verses):
    keyword = keyword.lower()
    return [v for v in verses if keyword in v['translation'].lower()]