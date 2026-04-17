import streamlit as st
from utils import extract_text, match_skills, generate_summary, create_pdf, recommend_jobs
from skills import ROLES

import requests
from streamlit_lottie import st_lottie

# 🎬 Load animation
def load_lottie(url):
    return requests.get(url).json()

lottie = load_lottie("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# 🎨 Premium CSS
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.box {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    margin: 10px 0;
}
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 12px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# 🎬 Header
col1, col2 = st.columns([2,1])

with col1:
    st.title("🚀 AI Resume Analyzer Pro")
    st.write("Smart hiring powered by AI")

with col2:
    st_lottie(lottie, height=150)

# 📌 Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Analyzer", "About"])

if page == "About":
    st.title("About")
    st.write("AI Resume Analyzer for recruiter-level evaluation")
    st.stop()

# 📂 Upload
uploaded_file = st.file_uploader("📄 Upload Resume")

role = st.selectbox("🎯 Select Role", list(ROLES.keys()))

if uploaded_file:
    text = extract_text(uploaded_file)
    skills = ROLES[role]

    found, score = match_skills(text, skills)
    missing = list(set(skills) - set(found))

    # 📊 Score
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.subheader("📊 Match Score")
    st.progress(int(score))
    st.write(f"{score:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)

    # ✅ Found
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.subheader("✅ Skills Found")
    st.write(found)
    st.markdown('</div>', unsafe_allow_html=True)

    # ❌ Missing
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.subheader("❌ Missing Skills")
    st.write(missing)
    st.markdown('</div>', unsafe_allow_html=True)

    # 📈 Suggestions
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.subheader("📈 Improvement Suggestions")
    for skill in missing:
        st.write(f"👉 Learn {skill}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 💼 Jobs
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.subheader("💼 Recommended Jobs")
    jobs = recommend_jobs(role, score)
    for job in jobs:
        st.write(f"👉 {job}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 📄 Summary + PDF
    if st.button("Generate Summary"):
        summary = generate_summary(text)

        st.markdown('<div class="box">', unsafe_allow_html=True)
        st.subheader("📄 Resume Summary")
        st.write(summary)
        st.markdown('</div>', unsafe_allow_html=True)

        pdf = create_pdf(score, found, missing, summary)
        with open(pdf, "rb") as f:
            st.download_button("📥 Download Report", f)