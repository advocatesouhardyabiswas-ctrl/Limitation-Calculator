import streamlit as st
from datetime import datetime, timedelta

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(
    page_title="LawGrid AI",
    layout="wide",
    page_icon="⚖️"
)

# -------------------------------
# STYLING
# -------------------------------
st.markdown("""
<style>
body { background-color: #0e1117; }
h1, h2, h3 { color: white; }

.stButton>button {
    width: 100%;
    border-radius: 8px;
    height: 3em;
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}

.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("⚖️ LawGrid AI")

menu = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Limitation Calculator",
    "Court Fee Calculator",
    "Drafting Assistant"
])

# -------------------------------
# DASHBOARD
# -------------------------------
if menu == "Dashboard":
    st.title("⚖️ LawGrid AI")
    st.markdown("### Legal Productivity Suite")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">📅 Limitation Calculator</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">💰 Court Fee Calculator</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">📝 Drafting Assistant</div>', unsafe_allow_html=True)

# -------------------------------
# LIMITATION CALCULATOR
# -------------------------------
elif menu == "Limitation Calculator":
    st.title("📅 Limitation Calculator")

    cause_date = st.date_input("Cause of Action Date")

    case_type = st.selectbox("Case Type", [
        "Consumer Complaint (2 years)",
        "Cheque Bounce (30 days)",
        "Civil Suit (3 years)",
        "Custom"
    ])

    if case_type == "Custom":
        limitation_days = st.number_input("Enter Days", min_value=1)
    else:
        mapping = {
            "Consumer Complaint (2 years)": 730,
            "Cheque Bounce (30 days)": 30,
            "Civil Suit (3 years)": 1095
        }
        limitation_days = mapping[case_type]

    if st.button("Calculate Limitation"):

        start_date = cause_date + timedelta(days=1)
        last_date = start_date + timedelta(days=limitation_days - 1)

        today = datetime.today().date()

        st.metric("Last Date to File", last_date.strftime("%d-%m-%Y"))

        if today <= last_date:
            st.success("Within Limitation ✅")
        else:
            delay = (today - last_date).days
            st.error(f"Delayed by {delay} days ❌")

# -------------------------------
# COURT FEE CALCULATOR
# -------------------------------
elif menu == "Court Fee Calculator":
    st.title("💰 Court Fee Calculator")

    suit_type = st.selectbox("Suit Type", [
        "Money Suit",
        "Partition Suit",
        "Injunction",
        "Declaration"
    ])

    amount = st.number_input("Enter Amount (₹)", min_value=0)

    if st.button("Calculate Court Fee"):

        if suit_type == "Money Suit":
            fee = amount * 0.01
        elif suit_type == "Partition Suit":
            fee = amount * 0.005
        elif suit_type == "Injunction":
            fee = 500
        else:
            fee = 1000

        st.metric("Estimated Court Fee", f"₹ {int(fee)}")

# -------------------------------
# DRAFTING ASSISTANT
# -------------------------------
elif menu == "Drafting Assistant":
    st.title("📝 Drafting Assistant")

    draft_type = st.selectbox("Draft Type", [
        "Legal Notice",
        "Writ Petition",
        "Consumer Complaint"
    ])

    facts = st.text_area("Enter Facts")
    relief = st.text_area("Enter Relief")

    if st.button("Generate Draft"):

        draft = f"""
{draft_type.upper()}

Facts:
{facts}

Relief:
{relief}

Filed before appropriate authority.
"""

        st.text_area("Draft Output", draft, height=300)
