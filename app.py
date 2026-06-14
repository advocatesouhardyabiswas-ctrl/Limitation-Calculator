from datetime import date, timedelta
from pathlib import Path

import streamlit as st
from dateutil.relativedelta import relativedelta


# Files
APP_FOLDER = Path(__file__).parent
LOGO = APP_FOLDER / "assets" / "alpine-legal-solutions.png"


# Common limitation periods from the supplied bare acts.
# Always verify the selected provision before filing.
RULES = {
    "Money and contract claims": {
        "Price of goods sold without fixed credit": (
            3, "years", "Date the goods were delivered", "Limitation Act, Article 14"
        ),
        "Price of goods sold with fixed credit": (
            3, "years", "Date the credit period expired", "Limitation Act, Article 15"
        ),
        "Money lent, payable on demand": (
            3, "years", "Date the loan was made", "Limitation Act, Article 21"
        ),
        "Promissory note payable on demand": (
            3, "years", "Date of the promissory note", "Limitation Act, Article 35"
        ),
        "Arrears of rent": (
            3, "years", "Date each arrear became due", "Limitation Act, Article 52"
        ),
        "Specific performance of contract": (
            3,
            "years",
            "Date fixed for performance, or date refusal became known",
            "Limitation Act, Article 54",
        ),
        "Compensation for breach of contract": (
            3, "years", "Date the contract was broken", "Limitation Act, Article 55"
        ),
    },
    "Declarations and documents": {
        "General declaration": (
            3, "years", "Date the right to sue first accrued", "Limitation Act, Article 58"
        ),
        "Cancel an instrument or decree": (
            3,
            "years",
            "Date the relevant facts first became known",
            "Limitation Act, Article 59",
        ),
    },
    "Property claims": {
        "Redeem or recover mortgaged property": (
            30,
            "years",
            "Date the right to redeem or recover accrued",
            "Limitation Act, Article 61(a)",
        ),
        "Enforce money secured by mortgage": (
            12, "years", "Date the secured money became due", "Limitation Act, Article 62"
        ),
        "Possession after dispossession": (
            12, "years", "Date of dispossession", "Limitation Act, Article 64"
        ),
        "Possession based on title": (
            12,
            "years",
            "Date the defendant's possession became adverse",
            "Limitation Act, Article 65",
        ),
        "Landlord recovering possession from tenant": (
            12, "years", "Date the tenancy ended", "Limitation Act, Article 67"
        ),
    },
    "Appeals and applications": {
        "Civil appeal to High Court": (
            90, "days", "Date of the decree or order", "Limitation Act, Article 116(a)"
        ),
        "Civil appeal to another court": (
            30, "days", "Date of the decree or order", "Limitation Act, Article 116(b)"
        ),
        "Leave to defend a summary suit": (
            10, "days", "Date summons was served", "Limitation Act, Article 118"
        ),
        "Substitute legal representative": (
            90, "days", "Date of death", "Limitation Act, Article 120"
        ),
        "Set aside abatement": (
            60, "days", "Date of abatement", "Limitation Act, Article 121"
        ),
        "Restore matter dismissed for default": (
            30, "days", "Date of dismissal", "Limitation Act, Article 122"
        ),
        "Set aside ex parte decree": (
            30,
            "days",
            "Date of decree, or date of knowledge if summons was not duly served",
            "Limitation Act, Article 123",
        ),
        "Review of judgment": (
            30, "days", "Date of decree or order", "Limitation Act, Article 124"
        ),
        "Civil revision": (
            90, "days", "Date of decree or order", "Limitation Act, Article 131"
        ),
    },
    "Execution": {
        "Execute civil decree or order": (
            12,
            "years",
            "Date the decree became enforceable",
            "Limitation Act, Article 136",
        ),
    },
    "Specific Relief Act": {
        "Summary suit after dispossession": (
            6, "months", "Date of dispossession", "Specific Relief Act, Section 6(2)"
        ),
    },
    "Cheque dishonour": {
        "Send demand notice": (
            30,
            "days",
            "Date bank information of dishonour was received",
            "Negotiable Instruments Act, Section 138(b)",
        ),
        "Drawer's payment period": (
            15,
            "days",
            "Date the drawer received the notice",
            "Negotiable Instruments Act, Section 138(c)",
        ),
        "File cheque dishonour complaint": (
            1,
            "months",
            "Date the cause of action arose after the payment period",
            "Negotiable Instruments Act, Section 142(1)(b)",
        ),
    },
    "RERA": {
        "Appeal to Appellate Tribunal": (
            60,
            "days",
            "Date the copy of the order was received",
            "RERA Act, Section 44(2)",
        ),
        "Appeal to High Court": (
            60,
            "days",
            "Date the Tribunal order was communicated",
            "RERA Act, Section 58",
        ),
    },
    "General": {
        "Suit not otherwise provided for": (
            3, "years", "Date the right to sue accrued", "Limitation Act, Article 113"
        ),
        "Application not otherwise provided for": (
            3, "years", "Date the right to apply accrued", "Limitation Act, Article 137"
        ),
    },
}


def calculate_deadline(start, amount, unit, excluded_days):
    """Return the estimated deadline after adding the selected period."""
    adjusted_start = start + timedelta(days=excluded_days)

    if unit == "days":
        return adjusted_start + timedelta(days=amount)
    if unit == "months":
        return adjusted_start + relativedelta(months=amount)
    return adjusted_start + relativedelta(years=amount)


st.set_page_config(
    page_title="Alpine AI - Limitation Calculator",
    page_icon=str(LOGO) if LOGO.exists() else "AL",
    layout="centered",
)


# Colours taken from the supplied Alpine Legal Solutions logo.
st.markdown(
    """
    <style>
    html, body, .stApp, button, input, label, div, span, p, h1, h2, h3 {
        font-family: "Times New Roman", Times, serif !important;
    }
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: #ffffff;
    }
    .title {
        color: #001333;
        text-align: center;
        margin: 0;
        font-size: 2.4rem;
    }
    .subtitle {
        color: #03a9c5;
        text-align: center;
        margin: 0.2rem 0 1.2rem;
        font-size: 1.05rem;
    }
    .tm {
        font-size: 0.65rem;
        vertical-align: super;
        margin-left: 0.12rem;
    }
    .result {
        background: #f2f8fc;
        border: 1px solid #d6e4ef;
        border-left: 6px solid #0657f9;
        border-radius: 10px;
        padding: 1.2rem;
        margin-top: 1rem;
    }
    .result-date {
        color: #001333;
        font-size: 2rem;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if LOGO.exists():
    st.image(str(LOGO), use_container_width=True)

st.markdown(
    '<h1 class="title">Alpine AI<span class="tm">&trade;</span></h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">by Alpine Legal Solutions<span class="tm">&trade;</span></div>',
    unsafe_allow_html=True,
)

st.info(
    "This is an estimate for legal research. Verify the provision, starting date, "
    "exclusions, special law, and court holidays before filing."
)


category = st.selectbox("Case category", list(RULES.keys()))
proceeding = st.selectbox("Proceeding", list(RULES[category].keys()))

amount, unit, trigger_help, citation = RULES[category][proceeding]

start_date = st.date_input(
    "Relevant starting date",
    value=date.today(),
    help=trigger_help,
)
st.caption(f"Use: {trigger_help}")

excluded_days = st.number_input(
    "Legally excludable days, if verified",
    min_value=0,
    value=0,
    step=1,
)

submitted = st.button(
    "Calculate limitation date",
    use_container_width=True,
    type="primary",
)


if submitted:
    deadline = calculate_deadline(start_date, amount, unit, excluded_days)
    days_left = (deadline - date.today()).days

    if days_left > 0:
        status = f"{days_left} day(s) remaining"
    elif days_left == 0:
        status = "The estimated deadline is today"
    else:
        status = f"Apparently expired by {abs(days_left)} day(s)"

    st.markdown(
        f"""
        <div class="result">
            <div>Estimated last date</div>
            <div class="result-date">{deadline.strftime('%d %B %Y')}</div>
            <strong>{status}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(f"**Provision:** {citation}")
    st.write(f"**Prescribed period:** {amount} {unit}")
    st.write(f"**Time begins from:** {trigger_help}")

    if days_left <= 7:
        st.error("Urgent: independently verify the deadline before relying on it.")


st.divider()
st.caption(
    "Alpine AI(TM) by Alpine Legal Solutions(TM). Informational tool only; not legal advice."
)
