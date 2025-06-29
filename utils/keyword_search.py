def search_by_keyword(query, verses):
    query = query.lower()
    results = []
    for verse in verses:
        if query in verse['text'].lower() or query in verse['arabic'].lower():
            results.append(verse)

    return results