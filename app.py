import streamlit as st
from utils.keyword_search import search_by_keyword
from utils.semantic_search import SemanticQuranSearch
from utils.data_loader import load_quran_data

# Cache data loading
@st.cache_data
def load_and_prepare_data():
    try:
        verses = load_quran_data('quran_english.json')
        if not verses:
            st.error("quran_english.json is empty. Please run combine_json_files.py with valid data.")
            st.stop()
        # Debug: Check the first verse's keys
        st.write(f"Sample verse keys: {list(verses[0].keys())}")
        for verse in verses:
            if 'translation' in verse:
                verse['text'] = verse.pop('translation')
            elif 'text' not in verse:
                st.error(f"Missing 'translation' or 'text' in verse: {verse}")
                st.stop()
            # Verify English text is not Arabic
            if any(char in verse['text'] for char in "ءآأؤإءبتثجحخدذرزسشصضطظعغفقكلمنهوى"):
                st.error(f"Arabic text detected in English translation for Surah {verse['surah']}:{verse['ayah']}")
                st.stop()
        return verses
    except FileNotFoundError:
        st.error("quran_english.json not found. Please run combine_json_files.py first.")
        st.stop()

# Cache semantic search engine
@st.cache_resource
def init_semantic_engine(verses):
    return SemanticQuranSearch(verses)

# Load data
verses = load_and_prepare_data()
st.write(f"Total verses loaded: {len(verses)}")

# Initialize semantic search
semantic_engine = init_semantic_engine(verses)

# Apply custom CSS
with open("static/style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Streamlit App UI
st.set_page_config(page_title="Qur’an AI", layout="centered")
st.title("📖 Qur’an AI Search (English & Arabic)")

query = st.text_input("Enter a keyword or phrase (English or Arabic)")
search_type = st.radio("Search Type", ["Semantic (BERT)", "Keyword"])

if st.button("Search"):
    if not query:
        st.warning("Please enter a search query.")
    elif search_type == "Keyword":
        results = search_by_keyword(query, verses)
        if results:
            for r in results:
                st.markdown(f"**{r['surah_name']} ({r['surah']}:{r['ayah']})** — *{r['text']}*")
                st.markdown(f"<div class='arabic'>**{r['surah_name_arabic']}**: {r['arabic']}</div>", unsafe_allow_html=True)
        else:
            st.info("No matching verses found.")
    else:
        results = semantic_engine.search(query)
        if results:
            for verse, score in results:
                st.markdown(f"**{verse['surah_name']} ({verse['surah']}:{verse['ayah']})** — *{verse['text']}*")
                st.markdown(f"<div class='arabic'>**{verse['surah_name_arabic']}**: {verse['arabic']}</div>", unsafe_allow_html=True)
                st.caption(f"Semantic Match Score: {score:.4f}")
        else:
            st.info("No semantically similar verses found.")