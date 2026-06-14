import streamlit as st
from datetime import datetime, timedelta

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Alpine AI",
    layout="wide",
    page_icon="⚖️"
)

# ----------------------------------
# GLOBAL STYLING (LIGHT + TIMES NEW ROMAN)
# ----------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Times New Roman', serif;
    background-color: #f7f9fc;
}

h1, h2, h3 {
    color: #1a1a1a;
}

.block-container {
    padding-top: 2rem;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    background-color: #1e88e5;
    color: white;
    font-weight: bold;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# HEADER WITH LOGO
# ----------------------------------
col1, col2 = st.columns([1,6])

with col1:
    try:
        st.image("Alpine monogram.png", width=80)
    except:
        pass

with col2:
    st.title("Alpine AI")
    st.markdown("### Legal Intelligence Suite")

# ----------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------
menu = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Limitation Calculator",
    "Court Fee Calculator",
    "Drafting Assistant"
])

# ----------------------------------
# DASHBOARD
# ----------------------------------
if menu == "Dashboard":

    st.markdown("## Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">📅<br><b>Limitation Calculator</b><br>Compute deadlines instantly</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">💰<br><b>Court Fee Calculator</b><br>Estimate fees quickly</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">📝<br><b>Drafting Assistant</b><br>Generate legal drafts</div>', unsafe_allow_html=True)

# ----------------------------------
# LIMITATION CALCULATOR
# ----------------------------------
elif menu == "Limitation Calculator":

    st.header("📅 Limitation Calculator")

    col1, col2 = st.columns(2)

    with col1:
        cause_date = st.date_input("Cause of Action Date")

    with col2:
        limitation_days = st.number_input("Limitation Period (Days)", min_value=1)

    if st.button("Calculate Limitation"):

        # Section 12 logic → exclude first day
        start_date = cause_date + timedelta(days=1)

        last_date = start_date + timedelta(days=limitation_days - 1)

        today = datetime.today().date()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Last Date to File", last_date.strftime("%d-%m-%Y"))

        with col2:
            if today <= last_date:
                st.success("Within Limitation (Sec. 3)")
            else:
                delay = (today - last_date).days
                st.error(f"Delay: {delay} days (Sec. 5 required)")

# ----------------------------------
# COURT FEE CALCULATOR
# ----------------------------------
elif menu == "Court Fee Calculator":

    st.header("💰 Court Fee Calculator")

    col1, col2 = st.columns(2)

    with col1:
        suit_type = st.selectbox("Suit Type", [
            "Money Suit",
            "Injunction",
            "Declaration"
        ])

    with col2:
        amount = st.number_input("Suit Value (₹)", min_value=0)

    if st.button("Calculate Court Fee"):

        if suit_type == "Money Suit":
            fee = amount * 0.01  # Ad valorem principle
        elif suit_type == "Injunction":
            fee = 500
        else:
            fee = 1000

        st.metric("Estimated Court Fee", f"₹ {int(fee)}")

        st.info("Calculated on basic Court Fees Act principles (ad valorem / fixed fee)")

# ----------------------------------
# DRAFTING ASSISTANT
# ----------------------------------
elif menu == "Drafting Assistant":

    st.header("📝 Drafting Assistant")

    draft_type = st.selectbox("Draft Type", [
        "Legal Notice",
        "Writ Petition",
        "Cheque Bounce (Sec 138 NI Act)"
    ])

    facts = st.text_area("Enter Facts", height=150)
    relief = st.text_area("Enter Relief", height=100)

    if st.button("Generate Draft"):

        if draft_type == "Cheque Bounce (Sec 138 NI Act)":

            draft = f"""
LEGAL NOTICE UNDER SECTION 138 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881

Facts:
{facts}

The cheque issued by you has been dishonoured due to insufficiency of funds.

You are hereby called upon to make the payment within 15 days from receipt of this notice.

Failing which, appropriate legal proceedings shall be initiated.

Relief:
{relief}
"""

        elif draft_type == "Writ Petition":

            draft = f"""
IN THE HIGH COURT

Facts:
{facts}

GROUNDS:
- Violation of fundamental rights
- Arbitrary action

PRAYER:
{relief}
"""

        else:

            draft = f"""
LEGAL NOTICE

Facts:
{facts}

You are hereby called upon to comply within 15 days.

Failing which legal action shall be initiated.

Relief:
{relief}
"""

        st.text_area("Generated Draft", draft, height=300)
