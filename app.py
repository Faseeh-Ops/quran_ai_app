from utils.api_loader import fetch_quran_from_cdn
from utils.keyword_search import search_by_keyword
from utils.semantic_search import SemanticQuranSearch
import streamlit as st

# Load full Qur’an from API
verses = fetch_quran_from_cdn('eng-sahih')
semantic_engine = SemanticQuranSearch(verses)

st.set_page_config(page_title="Qur’an AI", layout="centered")
st.title("📖 Qur’an AI Search")

query = st.text_input("Enter a keyword or phrase")
search_type = st.radio("Search Type", ["Semantic (BERT)", "Keyword"])

if st.button("Search"):
    if search_type == "Keyword":
        results = search_by_keyword(query, verses)
        for r in results:
            st.markdown(f"**Surah {r['surah']}:{r['ayah']}** — *{r['text']}*")
    else:
        results = semantic_engine.search(query)
        for verse, score in results:
            st.markdown(f"**Surah {verse['surah']}:{verse['ayah']}** — *{verse['text']}*")
