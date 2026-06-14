import streamlit as st
import os
from datetime import datetime, timedelta
from openai import OpenAI
from docx import Document

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Alpine AI", layout="wide", page_icon="al")

# Ensure API key is configured in your Streamlit secrets
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

# -------------------------------
# STYLING
# -------------------------------
st.markdown("""
<style>
    body { font-family: 'Times New Roman', serif; background-color: #f8f9fa; }
    h1, h2, h3 { color: #004a99; }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #004a99;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #004a99;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
col1, col2 = st.columns([1, 10])
if os.path.exists("monogram.png"):
    col1.image("monogram.png", width=70)
col2.title("Alpine AI")
col2.markdown("### Legal Intelligence Suite")

# -------------------------------
# NAVIGATION
# -------------------------------
menu = st.sidebar.radio("Navigation", ["Dashboard", "Limitation", "Court Fees", "AI Drafting"])

# -------------------------------
# DASHBOARD
# -------------------------------
if menu == "Dashboard":
    st.markdown("### Welcome, Advocate.")
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card">📅 **Limitation Calculator**</div>', unsafe_allow_html=True)
    c2.markdown('<div class="card">💰 **Court Fee Calculator**</div>', unsafe_allow_html=True)
    c3.markdown('<div class="card">📝 **AI Drafting Assistant**</div>', unsafe_allow_html=True)

# -------------------------------
# LIMITATION
# -------------------------------
elif menu == "Limitation":
    st.header("📅 Limitation Calculator")
    d1, d2 = st.columns(2)
    cause_date = d1.date_input("Cause of Action Date")
    days = d2.number_input("Limitation Period (Days)", min_value=1, value=30)
    
    if st.button("Calculate"):
        last_date = cause_date + timedelta(days=days)
        st.metric("Last Date to File", last_date.strftime("%d-%m-%Y"))
        if datetime.today().date() <= last_date:
            st.success("Within Limitation (Sec. 3)")
        else:
            st.error(f"Expired by {(datetime.today().date() - last_date).days} days")

# -------------------------------
# COURT FEES
# -------------------------------
elif menu == "Court Fees":
    st.header("💰 Court Fee Calculator")
    val = st.number_input("Suit Value (₹)", min_value=0)
    if st.button("Calculate Fee"):
        st.success(f"Estimated Fee: ₹ {int(val * 0.01):,}")

# -------------------------------
# AI DRAFTING
# -------------------------------
elif menu == "AI Drafting":
    st.header("📝 AI Drafting Assistant")
    d_type = st.selectbox("Draft Type", ["Legal Notice", "Writ Petition", "Consumer Complaint"])
    facts = st.text_area("Facts", height=150)
    relief = st.text_area("Relief", height=100)

    if st.button("Generate AI Draft"):
        if not client.api_key:
            st.error("API Key not set.")
        else:
            with st.spinner("Alpine AI is working..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Draft a {d_type}. Facts: {facts}. Relief: {relief}."}]
                )
                draft = response.choices[0].message.content
                st.text_area("Draft Output", draft, height=300)
                
                # Export
                doc = Document()
                doc.add_paragraph(draft)
                doc.save("draft.docx")
                with open("draft.docx", "rb") as f:
                    st.download_button("📄 Download as Word", f, "draft.docx")
