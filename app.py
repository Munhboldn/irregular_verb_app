import streamlit as st
import random
from logic.verb_data import verb_dict

# Mobile styling
st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stApp {
            padding: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
for key in ["favorites", "quiz_score", "quiz_history", "quiz_verb", "mastered_verbs"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key != "quiz_score" else 0

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Search Verbs", "💖 My Favorites", "🧠 Quiz Me"])

# --- Tab 1: Search ---
with tab1:
    st.title("✨ Irregular Verb Form Finder ✨")
    search_term = st.text_input("Search for a verb:")
    verb_list = [v for v in verb_dict.keys() if search_term.lower() in v]

    if not verb_list:
        st.warning("No matching verbs found. Try a different search term.")
    else:
        verb = st.selectbox("Choose a verb:", verb_list)
        if verb:
            forms = verb_dict[verb]
            st.table({"Base Form": [verb], "Past Tense": [forms["past"]], "Past Participle": [forms["participle"]]})
            if st.button("💖 Add to Favorites"):
                if verb not in st.session_state.favorites:
                    st.session_state.favorites.append(verb)

# --- Tab 2: Favorites ---
with tab2:
    st.header("Your Favorite Verbs")
    for i, fav in enumerate(st.session_state.favorites):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"- {fav.capitalize()}")
        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.favorites.pop(i)
                st.experimental_rerun()

    if st.session_state.favorites:
        if st.button("📥 Export Favorites"):
            fav_data = {v: verb_dict[v] for v in st.session_state.favorites}
            st.download_button("Download JSON", data=str(fav_data), file_name="favorites.json")

# --- Tab 3: Quiz ---
with tab3:
    st.header("🎲 Verb Quiz")
    if st.button("New Quiz Question") or "quiz_verb" not in st.session_state:
        st.session_state.quiz_verb = random.choice(list(verb_dict.keys()))

    quiz_verb = st.session_state.quiz_verb
    st.write(f"What are the past and past participle of **{quiz_verb}**?")
    past_input = st.text_input("Past Tense:", key="past")
    part_input = st.text_input("Past Participle:", key="part")

    if st.button("Submit Answer"):
        past_correct = past_input.lower().strip() in verb_dict[quiz_verb]['past'].lower().split("/")
        part_correct = part_input.lower().strip() in verb_dict[quiz_verb]['participle'].lower().split("/")
        if past_correct and part_correct:
            st.success("✅ Both answers are correct!")
            st.session_state.quiz_score += 1
            st.session_state.mastered_verbs.append(quiz_verb)
        else:
            if not past_correct:
                st.error(f"❌ Incorrect Past Tense. Correct: {verb_dict[quiz_verb]['past']}")
            if not part_correct:
                st.error(f"❌ Incorrect Past Participle. Correct: {verb_dict[quiz_verb]['participle']}")

        st.session_state.quiz_history.append({"verb": quiz_verb, "past": past_input, "part": part_input})

    st.write(f"✅ Score: {st.session_state.quiz_score} | Mastered: {len(set(st.session_state.mastered_verbs))}")



import json

with open("data/verb_dict.json", "r") as f:
    verb_dict = json.load(f)
