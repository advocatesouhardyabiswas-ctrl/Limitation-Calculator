import streamlit as st
from datetime import datetime, timedelta
import sqlite3
from openai import OpenAI
from docx import Document

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Alpine AI", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------------
# DATABASE
# -------------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT,
    password TEXT
)
""")
conn.commit()

# -------------------------------
# LOGIN SYSTEM
# -------------------------------
def login():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        # ADMIN BYPASS
        if email == "advocatesouhardyabiswas@gmail.com":
            st.session_state["logged_in"] = True
            st.session_state["user"] = email
            return

        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        result = c.fetchone()

        if result:
            st.session_state["logged_in"] = True
            st.session_state["user"] = email
        else:
            st.error("Invalid credentials")

def signup():
    st.title("📝 Sign Up")

    email = st.text_input("New Email")
    password = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        c.execute("INSERT INTO users VALUES (?,?)", (email, password))
        conn.commit()
        st.success("Account created")

# -------------------------------
# WORD EXPORT
# -------------------------------
def generate_word(text):
    doc = Document()
    doc.add_paragraph(text)
    file_path = "draft.docx"
    doc.save(file_path)
    return file_path

# -------------------------------
# AI DRAFTING
# -------------------------------
def generate_ai_draft(facts, relief, draft_type):
    prompt = f"""
    Draft a professional {draft_type} in Indian legal format.

    Facts:
    {facts}

    Relief:
    {relief}

    Include proper structure, headings, and legal tone.
    """

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# -------------------------------
# SESSION CHECK
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:

    option = st.selectbox("Select", ["Login", "Sign Up"])

    if option == "Login":
        login()
    else:
        signup()

else:

    # -------------------------------
    # UI
    # -------------------------------
    st.title("⚖️ Alpine AI")

    menu = st.sidebar.radio("Navigation", [
        "Dashboard",
        "Limitation",
        "Court Fees",
        "AI Drafting"
    ])

    # -------------------------------
    # DASHBOARD
    # -------------------------------
    if menu == "Dashboard":
        st.success(f"Welcome {st.session_state['user']}")

    # -------------------------------
    # LIMITATION
    # -------------------------------
    elif menu == "Limitation":

        date = st.date_input("Cause Date")
        days = st.number_input("Days", min_value=1)

        if st.button("Calculate"):
            last = date + timedelta(days=days)
            st.success(f"Last Date: {last}")

    # -------------------------------
    # COURT FEES
    # -------------------------------
    elif menu == "Court Fees":

        value = st.number_input("Suit Value")

        if st.button("Calculate Fee"):
            fee = value * 0.01
            st.success(f"₹ {fee}")

    # -------------------------------
    # AI DRAFTING
    # -------------------------------
    elif menu == "AI Drafting":

        draft_type = st.selectbox("Draft Type", [
            "Legal Notice",
            "Writ Petition",
            "Consumer Complaint"
        ])

        facts = st.text_area("Facts")
        relief = st.text_area("Relief")

        if st.button("Generate AI Draft"):

            with st.spinner("Generating..."):
                draft = generate_ai_draft(facts, relief, draft_type)

            st.text_area("Draft", draft, height=300)

            # DOWNLOAD BUTTON
            file_path = generate_word(draft)

            with open(file_path, "rb") as file:
                st.download_button(
                    label="📄 Download as Word",
                    data=file,
                    file_name="draft.docx"
                )
