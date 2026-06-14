from datetime import date, timedelta
from pathlib import Path

import streamlit as st
from dateutil.relativedelta import relativedelta


# ---------------------------------------------------------
# APPLICATION CONFIGURATION
# ---------------------------------------------------------

APP_DIR = Path(__file__).parent
LOGO_PATH = APP_DIR / "assets" / "alpine-legal-logo.png"

st.set_page_config(
    page_title="Alpine AI™ | Limitation Calculator",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "AL",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# LIMITATION RULES
# ---------------------------------------------------------

LIMITATION_RULES = {
    "Accounts": {
        "Mutual, open and current account": {
            "amount": 3,
            "unit": "years",
            "trigger": (
                "Close of the year in which the last admitted or proved "
                "item was entered in the account."
            ),
            "citation": "Limitation Act, 1963 — Article 1",
            "note": "The account must involve reciprocal demands.",
        },
    },

    "Contracts and Money Claims": {
        "Price of goods sold without fixed credit": {
            "amount": 3,
            "unit": "years",
            "trigger": "Date on which the goods were delivered.",
            "citation": "Limitation Act, 1963 — Article 14",
            "note": "",
        },
        "Price of goods sold with fixed credit": {
            "amount": 3,
            "unit": "years",
            "trigger": "Date on which the agreed credit period expired.",
            "citation": "Limitation Act, 1963 — Article 15",
            "note": "",
        },
        "Money lent under an agreement payable on demand": {
            "amount": 3,
            "unit": "years",
            "trigger": "Date on which the loan was made.",
            "citation": "Limitation Act, 1963 — Article 21",
            "note": "",
        },
        "Promissory note payable on demand": {
            "amount": 3,
            "unit": "years",
            "trigger": "Date of the promissory note.",
            "citation": "Limitation Act, 1963 — Article 35",
            "note": (
                "Check the instrument, acknowledgment and part-payment "
                "provisions before relying on this calculation."
            ),
        },
        "Arrears of rent": {
            "amount": 3,
            "unit": "years",
            "trigger": "Date on which each instalment of rent became due.",
            "citation": "Limitation Act, 1963 — Article 52",
            "note": "Each arrear may require a separate calculation.",
        },
        "Specific performance of contract": {
            "amount": 3,
            "unit": "years",
            "trigger": (
                "Date fixed for performance or, where no date was fixed, "
                "the date on which refusal became known."
            ),
            "citation": "Limitation Act, 1963 — Article 54",
            "note": "",
        },
        "Compensation for breach of contract": {
            "amount": 3,
            "unit": "years",
            "trigger": (
                "Date of breach, relevant successive breach, or cessation "
                "of a continuing breach."
            ),
            "citation": "Limitation Act, 1963 — Article 55",
            "note": "",
        },
    },

    "Declarations and Instruments": {
        "General declaratory suit": {
            "amount": 3,
            "unit": "years",
            "trigger": "Date on which the right to sue first accrued.",
            "citation": "Limitation Act, 1963 — Article 58",
            "note": "",
        },
        "Cancellation of instrument or decree": {
            "amount": 3,
            "unit": "years",
            "trigger": (
                "Date on which the facts entitling the claimant to "
                "cancellation first became known."
            ),
            "citation": "Limitation Act, 1963 — Article 59",
            "note": "Fraud or concealment may affect the calculation.",
        },
    },

    "Immovable Property": {
        "Redeem or recover mortgaged property": {
            "amount": 30,
            "unit": "years",
            "trigger": "Date on which the right to redeem or recover accrued.",
            "citation": "Limitation Act, 1963 — Article 61(a)",
            "note": "",
        },
        "Enforce money secured by mortgage or charge": {
            "amount": 12,
            "unit": "years",
            "trigger": "Date on which the secured money became due.",
            "citation": "Limitation Act, 1963 — Article 62",
            "note": "",
        },
        "Possession following dispossession": {
            "amount": 12,
            "unit": "years",
            "trigger": "Date of dispossession.",
            "citation": "Limitation Act, 1963 — Article 64",
            "note": "This article concerns a claim based on previous possession.",
        },
        "Possession based on title": {
            "amount": 12,
            "unit": "years",
            "trigger": (
                "Date on which the defendant's possession became adverse "
                "to the plaintiff."
            ),
            "citation": "Limitation Act, 1963 — Article 65",
            "note": "The date of adverse possession may be legally disputed.",
        },
        "Landlord recovering possession from tenant": {
            "amount": 12,
            "unit": "years",
            "trigger": "Date on which the tenancy was determined.",
            "citation": "Limitation Act, 1963 — Article 67",
            "note": "",
        },
    },

    "Torts": {
        "False imprisonment": {
            "amount": 1,
            "unit": "years",
            "trigger": "Date on which the imprisonment ended.",
            "citation": "Limitation Act, 1963 — Article 73",
            "note": "",
        },
        "Malicious prosecution": {
            "amount": 1,
            "unit": "years",
            "trigger": (
                "Date of acquittal or other termination of the prosecution."
            ),
            "citation": "Limitation Act, 1963 — Article 74",
            "note": "",
        },
        "Libel": {
            "amount": 1,
            "unit": "years",
            "trigger": "Date on which the libel was published.",
            "citation": "Limitation Act, 1963 — Article 75",
            "note": "",
        },
        "Trespass to immovable property": {
            "amount": 3,
            "unit": "years",
            "trigger": "Date of the trespass.",
            "citation": "Limitation Act, 1963 — Article 87",
            "note": "",
        },
    },

    "Appeals and Applications": {
        "Civil appeal to High Court": {
            "amount": 90,
            "unit": "days",
            "trigger": "Date of the decree or order.",
            "citation": "Limitation Act, 1963 — Article 116(a)",
            "note": "Qualifying certified-copy time may be excluded under Section 12.",
        },
        "Civil appeal to another court": {
            "amount": 30,
            "unit": "days",
            "trigger": "Date of the decree or order.",
            "citation": "Limitation Act, 1963 — Article 116(b)",
            "note": "Qualifying certified-copy time may be excluded under Section 12.",
        },
        "Leave to defend summary suit": {
            "amount": 10,
            "unit": "days",
            "trigger": "Date on which the summons was served.",
            "citation": "Limitation Act, 1963 — Article 118",
            "note": "",
        },
        "Substitution of legal representative": {
            "amount": 90,
            "unit": "days",
            "trigger": "Date of death of the relevant party.",
            "citation": "Limitation Act, 1963 — Article 120",
            "note": "",
        },
        "Set aside abatement": {
            "amount": 60,
            "unit": "days",
            "trigger": "Date of abatement.",
            "citation": "Limitation Act, 1963 — Article 121",
            "note": "",
        },
        "Restore proceeding dismissed for default": {
            "amount": 30,
            "unit": "days",
            "trigger": "Date of dismissal.",
            "citation": "Limitation Act, 1963 — Article 122",
            "note": "",
        },
        "Set aside ex parte decree": {
            "amount": 30,
            "unit": "days",
            "trigger": (
                "Date of decree or, where summons was not duly served, "
                "the date of knowledge."
            ),
            "citation": "Limitation Act, 1963 — Article 123",
            "note": "",
        },
        "Review by court other than Supreme Court": {
            "amount": 30,
            "unit": "days",
            "trigger": "Date of the decree or order.",
            "citation": "Limitation Act, 1963 — Article 124",
            "note": "",
        },
        "Civil revision": {
            "amount": 90,
            "unit": "days",
            "trigger": "Date of the decree or order sought to be revised.",
            "citation": "Limitation Act, 1963 — Article 131",
            "note": "",
        },
    },

    "Execution": {
        "Execution of civil decree or order": {
            "amount": 12,
            "unit": "years",
            "trigger": (
                "Date on which the decree became enforceable or the relevant "
                "default occurred."
            ),
            "citation": "Limitation Act, 1963 — Article 136",
            "note": (
                "Applications to enforce perpetual injunctions are treated "
                "differently under Article 136."
            ),
        },
        "Mandatory injunction decree": {
            "amount": 3,
            "unit": "years",
            "trigger": "Date of decree or the date fixed for performance.",
            "citation": "Limitation Act, 1963 — Article 135",
            "note": "",
        },
    },

    "Specific Relief": {
        "Summary suit following dispossession": {
            "amount": 6,
            "unit": "months",
            "trigger": "Date of dispossession.",
            "citation": "Specific Relief Act, 1963 — Section 6(2)",
            "note": "This is the special summary remedy under Section 6.",
        },
    },

    "Negotiable Instruments": {
        "Cheque dishonour demand notice": {
            "amount": 30,
            "unit": "days",
            "trigger": (
                "Date on which information of dishonour was received "
                "from the bank."
            ),
            "citation": "Negotiable Instruments Act, 1881 — Section 138(b)",
            "note": "The notice must contain a legally sufficient demand.",
        },
        "Drawer's payment period after notice": {
            "amount": 15,
            "unit": "days",
            "trigger": "Date on which the drawer received the statutory notice.",
            "citation": "Negotiable Instruments Act, 1881 — Section 138(c)",
            "note": "",
        },
        "Cheque dishonour complaint": {
            "amount": 1,
            "unit": "months",
            "trigger": (
                "Date on which the cause of action arose following expiry "
                "of the payment period."
            ),
            "citation": "Negotiable Instruments Act, 1881 — Section 142(1)(b)",
            "note": "Delay may be condoned where sufficient cause is established.",
        },
    },

    "RERA": {
        "Appeal to RERA Appellate Tribunal": {
            "amount": 60,
            "unit": "days",
            "trigger": (
                "Date on which a copy of the direction, decision or order "
                "was received."
            ),
            "citation": "RERA Act, 2016 — Section 44(2)",
            "note": "The Tribunal may entertain delay for sufficient cause.",
        },
        "RERA appeal to High Court": {
            "amount": 60,
            "unit": "days",
            "trigger": (
                "Date on which the Appellate Tribunal's decision or order "
                "was communicated."
            ),
            "citation": "RERA Act, 2016 — Section 58",
            "note": "",
        },
    },

    "General": {
        "Suit not otherwise specifically provided for": {
            "amount": 3,
            "unit": "years",
            "trigger": "Date on which the right to sue accrued.",
            "citation": "Limitation Act, 1963 — Article 113",
            "note": "Use only after confirming that no specific article applies.",
        },
        "Application not otherwise provided for": {
            "amount": 3,
            "unit": "years",
            "trigger": "Date on which the right to apply accrued.",
            "citation": "Limitation Act, 1963 — Article 137",
            "note": "Use only after confirming that no specific article applies.",
        },
    },
}


# ---------------------------------------------------------
# CALCULATION FUNCTIONS
# ---------------------------------------------------------

def add_limitation_period(start_date, amount, unit):
    """Add the selected calendar limitation period."""

    if unit == "days":
        return start_date + timedelta(days=amount)

    if unit == "months":
        return start_date + relativedelta(months=amount)

    if unit == "years":
        return start_date + relativedelta(years=amount)

    raise ValueError(f"Unsupported period unit: {unit}")


def describe_period(amount, unit):
    """Return a human-readable period."""

    if amount == 1:
        return f"1 {unit.rstrip('s')}"

    return f"{amount} {unit}"


def calculate_status(deadline, status_date):
    """Compare the calculated deadline with the selected status date."""

    days_remaining = (deadline - status_date).days

    if days_remaining > 0:
        return "Within the calculated period", "status-valid", days_remaining

    if days_remaining == 0:
        return "Calculated deadline is today", "status-today", days_remaining

    return "Calculated period has apparently expired", "status-expired", days_remaining


# ---------------------------------------------------------
# COLOUR SCHEME AND TYPOGRAPHY
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    :root {
        --alpine-navy: #001333;
        --alpine-cyan: #03A9C5;
        --alpine-blue: #0657F9;
        --alpine-white: #FFFFFF;
        --alpine-cream: #FBFCFE;
        --alpine-pale-blue: #F0F7FB;
        --alpine-text: #17243B;
        --alpine-muted: #68758A;
        --alpine-border: #D6E2EB;
        --alpine-success: #216345;
        --alpine-danger: #933737;
        --alpine-warning: #8A6116;
    }

    html, body, .stApp, button, input, textarea, select, label,
    div, span, p, h1, h2, h3, h4 {
        font-family: "Times New Roman", Times, serif !important;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background: var(--alpine-cream);
    }

    [data-testid="stSidebar"] {
        background: #F4F8FC;
        border-right: 1px solid var(--alpine-border);
    }

    .brand-panel {
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        background: var(--alpine-white);
        border: 1px solid var(--alpine-border);
        border-top: 4px solid var(--alpine-cyan);
        border-radius: 12px;
        box-shadow: 0 5px 18px rgba(0, 19, 51, 0.07);
    }

    .brand-panel h1 {
        margin: 0;
        color: var(--alpine-navy);
        font-size: 2.35rem;
        font-weight: 600;
    }

    .trademark {
        position: relative;
        top: -0.8rem;
        margin-left: 0.15rem;
        color: var(--alpine-navy);
        font-size: 0.72rem;
    }

    .brand-subtitle {
        margin-top: 0.15rem;
        color: var(--alpine-cyan);
        font-size: 1.08rem;
        letter-spacing: 0.02em;
    }

    .brand-description {
        margin: 0.45rem 0 0;
        color: var(--alpine-muted);
    }

    .deadline-card {
        padding: 1.2rem 1.4rem;
        margin: 0.5rem 0 1rem;
        background: var(--alpine-white);
        border: 1px solid var(--alpine-border);
        border-left: 6px solid var(--alpine-blue);
        border-radius: 10px;
    }

    .deadline-label {
        color: var(--alpine-muted);
        font-size: 0.9rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .deadline-date {
        margin: 0.3rem 0;
        color: var(--alpine-navy);
        font-size: 2.15rem;
        font-weight: 600;
    }

    .status-valid {
        color: var(--alpine-success);
        font-weight: 700;
    }

    .status-today {
        color: var(--alpine-warning);
        font-weight: 700;
    }

    .status-expired {
        color: var(--alpine-danger);
        font-weight: 700;
    }

    [data-testid="stMetric"] {
        padding: 0.85rem;
        background: var(--alpine-white);
        border: 1px solid var(--alpine-border);
        border-radius: 10px;
    }

    .method-note {
        color: var(--alpine-muted);
        font-size: 0.92rem;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

logo_column, heading_column = st.columns(
    [1.6, 5],
    vertical_alignment="center",
)

with logo_column:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    else:
        st.error("Logo missing: assets/alpine-legal-logo.png")

with heading_column:
    st.markdown(
        """
        <div class="brand-panel">
            <h1>
                Alpine AI<span class="trademark">™</span>
            </h1>

            <div class="brand-subtitle">
                by Alpine Legal Solutions™
            </div>

            <p class="brand-description">
                Indian legal limitation-period research and deadline calculator
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.warning(
    "This calculator is a legal research aid and not legal advice. "
    "Every result must be verified against the current law, the exact "
    "relief claimed, the applicable forum, relevant facts and court rules."
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)

    st.markdown("### Alpine AI™")
    st.caption("by Alpine Legal Solutions™")

    st.divider()

    status_date = st.date_input(
        "Calculate status as on",
        value=date.today(),
        help=(
            "This date changes the days-remaining status. "
            "It does not change the prescribed limitation period."
        ),
    )

    st.markdown("#### Mandatory legal checks")

    st.markdown(
        """
        - Identify the exact proceeding and relief.
        - Confirm the legally relevant starting date.
        - Check whether a special or local law applies.
        - Review Sections 4–24 of the Limitation Act.
        - Verify acknowledgment and part-payment requirements.
        - Verify the competent court's holiday calendar.
        - Confirm the current procedural and filing rules.
        """
    )


# ---------------------------------------------------------
# PROCEEDING SELECTION
# ---------------------------------------------------------

st.subheader("1. Select the proceeding")

selection_left, selection_right = st.columns(2)

with selection_left:
    category = st.selectbox(
        "Case category",
        options=list(LIMITATION_RULES.keys()),
    )

with selection_right:
    proceeding = st.selectbox(
        "Proceeding or relief",
        options=list(LIMITATION_RULES[category].keys()),
    )

rule = LIMITATION_RULES[category][proceeding]

period_amount = rule["amount"]
period_unit = rule["unit"]
period_text = describe_period(period_amount, period_unit)

citation_column, period_column = st.columns(2)

citation_column.info(
    f"**Source provision:** {rule['citation']}"
)

period_column.info(
    f"**Prescribed period:** {period_text}"
)


# ---------------------------------------------------------
# DATE INPUTS
# ---------------------------------------------------------

st.subheader("2. Enter the relevant dates")

date_left, date_right = st.columns(2)

with date_left:
    trigger_date = st.date_input(
        "Legally relevant starting date",
        value=date.today(),
        help=rule["trigger"],
    )

    st.caption(f"Time begins from: {rule['trigger']}")

with date_right:
    excluded_days = st.number_input(
        "Additional legally excludable days",
        min_value=0,
        max_value=10000,
        value=0,
        step=1,
        help=(
            "Enter only a period that is legally excludable after verification, "
            "such as qualifying certified-copy time under Section 12."
        ),
    )


# ---------------------------------------------------------
# ADVANCED ADJUSTMENTS
# ---------------------------------------------------------

with st.expander("Advanced legal adjustments"):
    st.write(
        "Use these inputs only after examining the relevant documents, "
        "statute, procedural rules and evidence."
    )

    fresh_start_enabled = st.checkbox(
        "Use a verified acknowledgment or part-payment date as a fresh start",
        help=(
            "Sections 18 and 19 contain strict requirements. "
            "This calculator does not determine whether they are satisfied."
        ),
    )

    fresh_start_date = st.date_input(
        "Verified fresh starting date",
        value=trigger_date,
        disabled=not fresh_start_enabled,
    )

    court_closed = st.checkbox(
        "The nominal deadline fell on a day when the court was closed",
        help=(
            "Section 4 may permit filing on the day the court reopens. "
            "Confirm the official court calendar."
        ),
    )

    reopening_date = st.date_input(
        "Court reopening date",
        value=trigger_date,
        disabled=not court_closed,
    )


# ---------------------------------------------------------
# CALCULATION
# ---------------------------------------------------------

effective_start = (
    fresh_start_date
    if fresh_start_enabled
    else trigger_date
)

adjusted_start = effective_start + timedelta(
    days=int(excluded_days)
)

nominal_deadline = add_limitation_period(
    adjusted_start,
    period_amount,
    period_unit,
)

if court_closed and reopening_date > nominal_deadline:
    final_deadline = reopening_date
else:
    final_deadline = nominal_deadline

status_text, status_css, days_remaining = calculate_status(
    final_deadline,
    status_date,
)


# ---------------------------------------------------------
# RESULT
# ---------------------------------------------------------

st.subheader("3. Calculated result")

st.markdown(
    f"""
    <div class="deadline-card">
        <div class="deadline-label">Calculated last date</div>

        <div class="deadline-date">
            {final_deadline.strftime("%d %B %Y")}
        </div>

        <div class="{status_css}">
            {status_text}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_one, metric_two, metric_three = st.columns(3)

metric_one.metric(
    "Days remaining",
    days_remaining,
)

metric_two.metric(
    "Prescribed period",
    period_text,
)

metric_three.metric(
    "Excluded days entered",
    int(excluded_days),
)


# ---------------------------------------------------------
# CALCULATION RECORD
# ---------------------------------------------------------

record_left, record_right = st.columns([1.2, 0.8])

with record_left:
    st.markdown("#### Calculation record")

    calculation_record = [
        {
            "Item": "Case category",
            "Value": category,
        },
        {
            "Item": "Proceeding",
            "Value": proceeding,
        },
        {
            "Item": "Source provision",
            "Value": rule["citation"],
        },
        {
            "Item": "Original trigger date",
            "Value": trigger_date.strftime("%d %B %Y"),
        },
        {
            "Item": "Effective starting date",
            "Value": effective_start.strftime("%d %B %Y"),
        },
        {
            "Item": "Excluded days entered",
            "Value": str(int(excluded_days)),
        },
        {
            "Item": "Adjusted calculation start",
            "Value": adjusted_start.strftime("%d %B %Y"),
        },
        {
            "Item": "Nominal deadline",
            "Value": nominal_deadline.strftime("%d %B %Y"),
        },
        {
            "Item": "Final calculated deadline",
            "Value": final_deadline.strftime("%d %B %Y"),
        },
        {
            "Item": "Status calculated as on",
            "Value": status_date.strftime("%d %B %Y"),
        },
    ]

    st.dataframe(
        calculation_record,
        hide_index=True,
        use_container_width=True,
    )

with record_right:
    st.markdown("#### Legal guidance")

    st.write(f"**Time begins from:** {rule['trigger']}")

    if rule["note"]:
        st.info(rule["note"])

    st.write(
        "The result is a rules-based estimate. It does not decide "
        "disputed facts, maintainability, condonation, sufficient cause "
        "or whether an exclusion legally applies."
    )


# ---------------------------------------------------------
# URGENT WARNINGS
# ---------------------------------------------------------

if days_remaining < 0:
    st.error(
        "The selected inputs produce an apparently expired date. "
        "Do not assume that the matter is barred or capable of condonation "
        "without examining the governing law and complete facts."
    )

elif days_remaining <= 7:
    st.error(
        "The calculated deadline is within seven days. Immediately verify "
        "the deadline, filing hours, holidays, scrutiny requirements and "
        "technical filing procedure."
    )

elif days_remaining <= 30:
    st.warning(
        "The calculated deadline is within 30 days. "
        "Prompt independent legal verification is advisable."
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.markdown(
    """
    <div class="method-note">
        <strong>Calculation method:</strong> Alpine AI™ adds the period
        prescribed by the selected provision to the legally relevant date
        entered by the user. It applies only the exclusion days and advanced
        adjustments expressly entered by the user.

        <br><br>

        Section 5 condonation is not automatically added because it depends
        on the nature of the proceeding, sufficient cause and judicial
        determination. Suits, appeals and applications may be treated
        differently.

        <br><br>

        <strong>Alpine AI™ by Alpine Legal Solutions™.</strong>
        All trademarks belong to their respective proprietor.
    </div>
    """,
    unsafe_allow_html=True,
)
