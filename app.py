import streamlit as st
import os
from datetime import datetime, timedelta

# -------------------------------
# CONFIGURATION
# -------------------------------
st.set_page_config(page_title="Alpine AI", layout="wide", page_icon="⚖️")

# -------------------------------
# STYLING (Blue & White Professional)
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

# Using 'monogram.png' - change this if your file name is different
img_path = "monogram.png"

with col1:
    if os.path.exists(img_path):
        st.image(img_path, width=70)
    else:
        st.write("❄️") # Fallback icon if image missing

with col2:
    st.title("Alpine AI")
    st.markdown("### Legal Intelligence Suite")

# -------------------------------
# NAVIGATION
# -------------------------------
menu = st.sidebar.radio("Navigation", ["Dashboard", "Limitation", "Court Fees", "Drafting"])

# -------------------------------
# LOGIC
# -------------------------------
if menu == "Dashboard":
    st.markdown("### Welcome, Advocate.")
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card">📅 Limitation Calculator</div>', unsafe_allow_html=True)
    c2.markdown('<div class="card">💰 Court Fee Calculator</div>', unsafe_allow_html=True)
    c3.markdown('<div class="card">📝 Drafting Assistant</div>', unsafe_allow_html=True)

elif menu == "Limitation":
    st.header("📅 Limitation Calculator")
    c1, c2 = st.columns(2)
    cause_date = c1.date_input("Cause of Action Date")
    lim_days = c2.number_input("Days", min_value=1, value=30)
    
    if st.button("Calculate"):
        last_date = cause_date + timedelta(days=lim_days)
        st.metric("Last Date", last_date.strftime("%d-%m-%Y"))
        if datetime.today().date() <= last_date:
            st.success("Within Limitation")
        else:
            st.error("Limitation Expired")

elif menu == "Court Fees":
    st.header("💰 Court Fee Calculator")
    val = st.number_input("Suit Value (₹)", min_value=0)
    if st.button("Calculate"):
        st.metric("Estimated Fee", f"₹ {int(val * 0.01):,}")

elif menu == "Drafting":
    st.header("📝 Drafting Assistant")
    facts = st.text_area("Facts")
    if st.button("Generate"):
        st.text_area("Result", f"LEGAL DRAFT\n\n{facts}", height=200)
