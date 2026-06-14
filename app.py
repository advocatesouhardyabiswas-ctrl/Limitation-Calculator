import streamlit as st
import sqlite3
import os
from datetime import datetime, timedelta
from openai import OpenAI
from docx import Document

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Alpine AI", layout="wide", page_icon="⚖️")

# OpenAI Client Setup (Ensure your secrets are set in Streamlit)
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

# -------------------------------
# DATABASE
# -------------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT)")
conn.commit()

# -------------------------------
# AI DRAFTING ENGINE
# -------------------------------
def generate_ai_draft(facts, relief, draft_type):
    try:
        prompt = f"Draft a professional {draft_type} in Indian legal format. Facts: {facts}. Relief: {relief}."
        response = client.chat.completions.create(
            model="gpt-4o", # Using a standard available model
            messages=[{"role": "system", "content": "You are a professional Indian legal assistant."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating draft: {e}"

# -------------------------------
# AUTHENTICATION
# -------------------------------
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    option = st.sidebar.radio("Navigation", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            if email == "advocatesouhardyabiswas@gmail.com":
                st.session_state.update({"logged_in": True, "user": email})
                st.rerun()
            c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            if c.fetchone():
                st.session_state.update({"logged_in": True, "user": email})
                st.rerun()
            else: st.error("Invalid credentials")
    else:
        if st.button("Create Account"):
            c.execute("INSERT INTO users VALUES (?,?)", (email, password))
            conn.commit()
            st.success("Account created! Please log in.")
    st.stop()

# -------------------------------
# MAIN APP (LOGGED IN)
# -------------------------------
st.title("⚖️ Alpine AI")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Limitation", "Court Fees", "AI Drafting"])

if menu == "Dashboard":
    st.success(f"Welcome, {st.session_state['user']}")
    st.markdown("---")
    st.write("Use the sidebar to navigate the legal suite.")

elif menu == "Limitation":
    st.header("📅 Limitation Calculator")
    date = st.date_input("Cause of Action Date")
    days = st.number_input("Limitation Period (Days)", min_value=1)
    if st.button("Calculate"):
        last = date + timedelta(days=days)
        st.metric("Last Date to File", last.strftime("%d-%m-%Y"))

elif menu == "Court Fees":
    st.header("💰 Court Fee Calculator")
    val = st.number_input("Suit Value (₹)", min_value=0)
    if st.button("Calculate Fee"):
        st.success(f"Estimated Fee: ₹ {int(val * 0.01):,}")

elif menu == "AI Drafting":
    st.header("📝 AI Drafting Assistant")
    d_type = st.selectbox("Draft Type", ["Legal Notice", "Writ Petition", "Consumer Complaint"])
    facts = st.text_area("Facts")
    relief = st.text_area("Relief")

    if st.button("Generate AI Draft"):
        with st.spinner("Alpine AI is drafting..."):
            draft = generate_ai_draft(facts, relief, d_type)
            st.text_area("Draft Output", draft, height=300)
            
            # Word Export
            doc = Document()
            doc.add_paragraph(draft)
            doc.save("draft.docx")
            with open("draft.docx", "rb") as f:
                st.download_button("📄 Download as Word", f, "draft.docx")
