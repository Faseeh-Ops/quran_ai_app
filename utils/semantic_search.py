from sentence_transformers import SentenceTransformer, util

class SemanticQuranSearch:
    def __init__(self, verses):
        self.verses = verses
        self.texts = [v['text'] for v in verses]
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.model.encode(self.texts, convert_to_tensor=True)

    def search(self, query, top_k=5):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
        results = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
        return [(self.verses[i], float(score)) for i, score in results]
