from datetime import date, timedelta
import math

import streamlit as st
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Alpine AI", page_icon="⚖️", layout="wide")

RULES = {
    "Price of goods without fixed credit":
        (3, "years", "Date goods were delivered", "Limitation Act, Article 14"),
    "Price of goods with fixed credit":
        (3, "years", "Date credit period expired", "Limitation Act, Article 15"),
    "Promissory note payable on demand":
        (3, "years", "Date of the note", "Limitation Act, Article 35"),
    "Arrears of rent":
        (3, "years", "Date each arrear became due", "Limitation Act, Article 52"),
    "Specific performance":
        (3, "years", "Fixed performance date or notice of refusal", "Limitation Act, Article 54"),
    "Breach of contract":
        (3, "years", "Date of breach", "Limitation Act, Article 55"),
    "General declaration":
        (3, "years", "Date right to sue first accrued", "Limitation Act, Article 58"),
    "Cancel instrument or decree":
        (3, "years", "Date relevant facts became known", "Limitation Act, Article 59"),
    "Possession based on title":
        (12, "years", "Date possession became adverse", "Limitation Act, Article 65"),
    "Landlord recovering possession":
        (12, "years", "Date tenancy ended", "Limitation Act, Article 67"),
    "Libel":
        (1, "years", "Date libel was published", "Limitation Act, Article 75"),
    "General civil suit":
        (3, "years", "Date right to sue accrued", "Limitation Act, Article 113"),
    "Civil appeal to High Court":
        (90, "days", "Date of decree or order", "Limitation Act, Article 116(a)"),
    "Civil appeal to another court":
        (30, "days", "Date of decree or order", "Limitation Act, Article 116(b)"),
    "Set aside ex-parte decree":
        (30, "days", "Date of decree or knowledge", "Limitation Act, Article 123"),
    "Civil revision":
        (90, "days", "Date of decree or order", "Limitation Act, Article 131"),
    "Execution of civil decree":
        (12, "years", "Date decree became enforceable", "Limitation Act, Article 136"),
    "Specific Relief dispossession suit":
        (6, "months", "Date of dispossession", "Specific Relief Act, Section 6"),
    "RERA Tribunal appeal":
        (60, "days", "Date order copy was received", "RERA Act, Section 44"),
    "RERA High Court appeal":
        (60, "days", "Date Tribunal order was communicated", "RERA Act, Section 58"),
    "Cheque dishonour notice":
        (30, "days", "Date dishonour information was received", "NI Act, Section 138(b)"),
    "Cheque drawer payment period":
        (15, "days", "Date statutory notice was received", "NI Act, Section 138(c)"),
    "Cheque dishonour complaint":
        (1, "months", "Date cause of action arose", "NI Act, Section 142"),
}

st.markdown("""
<style>
html, body, .stApp, button, input, textarea, select, label, div, span, p,
h1, h2, h3 {
    font-family: "Times New Roman", Times, serif !important;
}
[data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background: #fffdf8;
}
.hero {
    display:flex; align-items:center; gap:16px;
    padding:18px 22px; margin-bottom:16px;
    background:linear-gradient(120deg,#ffffff,#eef6f8);
    border:1px solid #dbe6ec; border-radius:14px;
}
.logo {
    width:52px; height:52px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    background:#f8fbfc; border:1px solid #8eacb8;
    color:#315c6b; font-size:25px;
    font-weight:bold; font-style:italic;
}
.result {
    padding:16px; background:#f4f9fa;
    border-left:5px solid #79a9b8; border-radius:8px;
}
</style>
<div class="hero">
    <div class="logo">al</div>
    <div>
        <h1 style="margin:0;color:#294f5d">Alpine AI</h1>
        <p style="margin:4px 0;color:#607780">
            Indian limitation and court-fee research assistant
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.warning(
    "Research aid only. Verify amendments, court holidays, exclusions, "
    "jurisdiction and current state court-fee schedules before filing."
)

limitation_tab, fee_tab, guide_tab = st.tabs(
    ["Limitation Calculator", "Court Fees", "Legal Guide"]
)

with limitation_tab:
    left, right = st.columns(2)

    with left:
        case = st.selectbox("Type of case", list(RULES))
        amount, unit, trigger_description, citation = RULES[case]

        trigger_date = st.date_input("Relevant starting date", date.today())
        excluded_days = st.number_input(
            "Legally excludable days",
            min_value=0,
            value=0,
            help="For example, certified-copy time. Enter only after verification."
        )

        court_closed = st.checkbox("Court was closed on the calculated deadline")
        reopening_date = st.date_input(
            "Court reopening date",
            trigger_date,
            disabled=not court_closed
        )

    adjusted_start = trigger_date + timedelta(days=excluded_days)

    if unit == "days":
        raw_deadline = adjusted_start + timedelta(days=amount)
    elif unit == "months":
        raw_deadline = adjusted_start + relativedelta(months=amount)
    else:
        raw_deadline = adjusted_start + relativedelta(years=amount)

    final_deadline = (
        max(raw_deadline, reopening_date)
        if court_closed else raw_deadline
    )

    remaining = (final_deadline - date.today()).days
    status = (
        "Due today" if remaining == 0
        else "Within time" if remaining > 0
        else "Apparently expired"
    )

    with right:
        st.subheader("Calculated result")
        st.markdown(
            f"""
            <div class="result">
                <b>{status}</b><br>
                <span style="font-size:28px">
                    {final_deadline.strftime("%d %B %Y")}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.metric("Days remaining", remaining)
        st.write(f"**Provision:** {citation}")
        st.write(f"**Period:** {amount} {unit}")
        st.write(f"**Time begins from:** {trigger_description}")
        st.write(f"**Original expiry:** {raw_deadline:%d %B %Y}")

with fee_tab:
    states = [
        "Select jurisdiction", "Andhra Pradesh", "Assam", "Bihar",
        "Chhattisgarh", "Delhi", "Goa", "Gujarat", "Haryana",
        "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
        "Madhya Pradesh", "Maharashtra", "Odisha", "Punjab",
        "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh",
        "Uttarakhand", "West Bengal", "Other"
    ]

    state = st.selectbox("State or Union Territory", states)
    filing = st.selectbox(
        "Type of filing",
        [
            "Money recovery or damages",
            "Declaratory suit",
            "Injunction",
            "Possession of property",
            "Specific performance",
            "Mortgage redemption",
            "Probate or administration",
            "Appeal",
            "Other"
        ]
    )

    value = st.number_input(
        "Claim or subject-matter value (₹)",
        min_value=0.0,
        value=100000.0,
        step=1000.0
    )

    method = st.selectbox(
        "Current state tariff method",
        [
            "Percentage",
            "Fee per ₹1,000 or part",
            "Fixed fee"
        ]
    )

    rate = st.number_input(
        "Rate or fixed fee",
        min_value=0.0,
        value=0.0,
        step=0.01
    )
    cap = st.number_input(
        "Maximum fee, if applicable (₹)",
        min_value=0.0,
        value=0.0
    )

    if method == "Percentage":
        fee = value * rate / 100
    elif method == "Fee per ₹1,000 or part":
        fee = math.ceil(value / 1000) * rate if value else 0
    else:
        fee = rate

    if cap:
        fee = min(fee, cap)

    st.metric("Estimated court fee", f"₹{fee:,.2f}")

    if state == "Select jurisdiction" or rate == 0:
        st.error(
            "Select the jurisdiction and enter its current statutory rate. "
            "Court fees differ by state and cannot safely be calculated "
            "from the historical central schedule alone."
        )

with guide_tab:
    st.subheader("Important checks")
    st.write("1. Identify the exact relief, forum and applicable special law.")
    st.write("2. Verify the legally relevant starting date.")
    st.write("3. Check exclusions under Sections 4–24 of the Limitation Act.")
    st.write("4. Check acknowledgment, part-payment, fraud and disability.")
    st.write("5. Verify court holidays and certified-copy exclusions.")
    st.write("6. Use the current court-fee amendment for the selected state.")
