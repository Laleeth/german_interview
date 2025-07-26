import streamlit as st
import os
from dotenv import load_dotenv
from openrouter_api import call_openrouter_api

# Load environment variables securely
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY", "")
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")

# === Styling and Theming ===
st.set_page_config(page_title="🇩🇪 German Interview Generator", layout="wide")

st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: white;
            font-family: 'Manrope', sans-serif;
        }
        h1 {
            text-align: center;
            font-size: 2.8rem;
            color: #1f4e79;
        }
        .answer-box {
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #1f4e79;
            margin: 20px 0;
        }
        .question-text {
            font-weight: bold;
            margin-top: 1rem;
        }
        .bookmark-box {
            border: 1px dashed #1f4e79;
            padding: 1rem;
            border-radius: 10px;
            background-color: #fefefe;
            margin-bottom: 10px;
        }
        .bookmark-box:hover {
            background-color: #f0f8ff;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# === Session State Setup ===
if "bookmarks" not in st.session_state:
    st.session_state["bookmarks"] = []

# === Behavioral Questions: 50+ ===
BEHAVIORAL_QUESTIONS = [
    "Erzählen Sie mir etwas über sich.",
    "Was motiviert Sie?",
    "Wie gehen Sie mit Stress um?",
    "Beschreiben Sie eine schwierige berufliche Situation, die Sie gemeistert haben.",
    "Was sind Ihre Stärken?",
    "Was ist Ihre größte Schwäche?",
    "Warum möchten Sie diesen Job?",
    "Wie gehen Sie mit Konflikten um?",
    "Was war Ihr größter beruflicher Erfolg?",
    "Wie organisieren Sie Ihren Arbeitsalltag?",
    "Was bedeutet Teamarbeit für Sie?",
    "Wie würden Ihre Kollegen Sie beschreiben?",
    "Was haben Sie aus einem Fehler gelernt?",
    "Was tun Sie, wenn Sie ein Ziel nicht erreichen?",
    "Wie motivieren Sie andere?",
    "Erzählen Sie von einem Projekt, auf das Sie besonders stolz sind.",
    "Wie gehen Sie mit Veränderungen um?",
    "Welche Werte sind Ihnen im Beruf wichtig?",
    "Wie priorisieren Sie Aufgaben unter Zeitdruck?",
    "Was erwarten Sie von Ihrem Vorgesetzten?",
    "Wie gehen Sie mit Feedback um?",
    "Wie bleiben Sie organisiert?",
    "Wie gehen Sie mit monotoner Arbeit um?",
    "Wie handeln Sie unter Druck?",
    "Was ist Ihr Arbeitsstil?",
    "Was war Ihre größte Herausforderung im letzten Job?",
    "Wie entwickeln Sie sich beruflich weiter?",
    "Erzählen Sie von einer Führungsrolle, die Sie übernommen haben.",
    "Was würden Sie in Ihrer Karriere anders machen?",
    "Wie reagieren Sie auf Kritik?",
    "Wie reagieren Sie auf Rückschläge?",
    "Was war Ihr erster Job und was haben Sie gelernt?",
    "Erzählen Sie von einem Misserfolg und wie Sie damit umgingen.",
    "Wie gehen Sie mit einem schwierigen Teammitglied um?",
    "Was bedeutet Erfolg für Sie?",
    "Wie würden Sie jemanden motivieren, der die Motivation verliert?",
    "Wie passen Sie sich neuen Technologien an?",
    "Wie gehen Sie mit mehreren Deadlines gleichzeitig um?",
    "Was ist Ihre größte berufliche Leidenschaft?",
    "Was würden Sie tun, wenn Sie sich mit Ihrer Führungskraft nicht einig sind?",
    "Wie bleiben Sie über Entwicklungen in Ihrer Branche informiert?",
    "Was schätzen Sie an Teamarbeit?",
    "Was war das wichtigste Feedback, das Sie je erhalten haben?",
    "Wie zeigen Sie Initiative?",
    "Wie gehen Sie mit Ungewissheit oder Risiko um?",
    "Wie treffen Sie wichtige Entscheidungen?",
    "Was macht einen guten Teamleiter aus?",
    "Wie lösen Sie komplexe Probleme?",
    "Wie integrieren Sie neue Mitarbeiter ins Team?",
    "Was unterscheidet Sie von anderen Bewerbern?"
]

QUESTION_BANK = {
    "Behavioral": BEHAVIORAL_QUESTIONS
}

MODEL_LIST = [
    
    "meta-llama/llama-3.3-70b-instruct:free"
]

# === Title ===
st.markdown("<h1>🇩🇪 AI German Interview Answer Generator</h1>", unsafe_allow_html=True)

# === API Key check ===
if not API_KEY:
    st.error("API key not found in .env file. Please add `OPENROUTER_API_KEY=your_key`.")
    st.stop()

# === Inputs ===
st.subheader("🎯 Choose a Question or Write Your Own")

category = st.selectbox("Select Category", list(QUESTION_BANK.keys()))
question = st.selectbox("Choose a predefined question", QUESTION_BANK[category])
custom_prompt = st.text_area("Or enter a custom question", placeholder="Ask an interview question in German...")

st.markdown("⚠️ Non-interview prompts will return a fun quote instead/ If Error Pops re-load or Generate again.")

# === Generation ===
if st.button("🚀 Generate Answer"):
    user_prompt = custom_prompt.strip() if custom_prompt.strip() else question

    if any(x in user_prompt.lower() for x in ["joke", "weather", "food", "poem", "song", "sport", "love"]):
        st.warning("🚫 That's not an interview question.")
        st.info("💡 'Keep calm and conjugate!' – Try a job-related question instead.")
    else:
        with st.spinner("Generating answer..."):
            response = call_openrouter_api(user_prompt, category, API_KEY, DEFAULT_MODEL)

        st.markdown('<div class="answer-box">', unsafe_allow_html=True)
        st.markdown("### 💬 AI-Generated Interview Answer")
        st.markdown(response, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Bookmark feature
        if st.button("⭐ Bookmark this Answer"):
            st.session_state["bookmarks"].append((user_prompt, response))
            st.success("Answer bookmarked!")

# === Show Bookmarks ===
if st.session_state["bookmarks"]:
    st.subheader("📌 Bookmarked Answers")
    for i, (q, a) in enumerate(st.session_state["bookmarks"]):
        st.markdown(f'<div class="bookmark-box"><b>{i+1}. {q}</b><br>{a}</div>', unsafe_allow_html=True)
