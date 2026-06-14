import streamlit as st
from datetime import datetime, timedelta
from openai import OpenAI
from docx import Document

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Alpine AI", layout="centered", page_icon="⚖️")

# OpenAI Client Setup (Ensure key is in your Streamlit secrets)
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

# -------------------------------
# APP HEADER
# -------------------------------
st.title("Alpine AI")
st.caption("Legal Intelligence Suite")
st.markdown("---")

# -------------------------------
# NAVIGATION
# -------------------------------
menu = st.sidebar.radio("Navigation", ["Dashboard", "Limitation", "Court Fees", "AI Drafting"])

# -------------------------------
# DASHBOARD
# -------------------------------
if menu == "Dashboard":
    st.subheader("Welcome")
    st.write("Select a tool from the sidebar to begin.")

# -------------------------------
# LIMITATION CALCULATOR
# -------------------------------
elif menu == "Limitation":
    st.header("📅 Limitation Calculator")
    
    col1, col2 = st.columns(2)
    cause_date = col1.date_input("Cause of Action Date")
    lim_days = col2.number_input("Limitation Period (Days)", min_value=1, value=30)
    
    if st.button("Calculate", type="primary"):
        last_date = cause_date + timedelta(days=lim_days)
        st.write(f"### Last Date to File: **{last_date.strftime('%d-%m-%Y')}**")
        
        if datetime.today().date() <= last_date:
            st.success("Within Limitation")
        else:
            st.error("Limitation Expired")

# -------------------------------
# COURT FEES
# -------------------------------
elif menu == "Court Fees":
    st.header("💰 Court Fee Calculator")
    val = st.number_input("Suit Value (₹)", min_value=0)
    if st.button("Calculate", type="primary"):
        st.write(f"### Estimated Fee: **₹ {int(val * 0.01):,}**")

# -------------------------------
# AI DRAFTING
# -------------------------------
elif menu == "AI Drafting":
    st.header("📝 AI Drafting Assistant")
    d_type = st.selectbox("Draft Type", ["Legal Notice", "Writ Petition", "Consumer Complaint"])
    facts = st.text_area("Facts", height=120)
    relief = st.text_area("Relief", height=80)

    if st.button("Generate Draft", type="primary"):
        with st.spinner("Generating..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Draft a {d_type} for: {facts}. Relief: {relief}."}]
                )
                draft = response.choices[0].message.content
                st.text_area("Draft Output", draft, height=250)
                
                # Word Export
                doc = Document()
                doc.add_paragraph(draft)
                doc.save("draft.docx")
                with open("draft.docx", "rb") as f:
                    st.download_button("📄 Download as Word", f, "draft.docx")
            except Exception as e:
                st.error("Could not generate draft. Please check your API key.")
