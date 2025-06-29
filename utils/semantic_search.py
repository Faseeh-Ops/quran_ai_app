from sentence_transformers import SentenceTransformer, util

class SemanticQuranSearch:
    def __init__(self, verses):
        self.verses = verses
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

        self.verse_texts = [verse['text'] for verse in verses]
        self.verse_embeddings = self.model.encode(self.verse_texts, convert_to_tensor=True)

    def search(self, query, top_k=5):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, self.verse_embeddings)[0]
        top_k = min(top_k, len(self.verses))
        top_results = scores.topk(k=top_k)
        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            verse = self.verses[int(idx)]
            results.append((verse, float(score)))
        return results