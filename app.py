import streamlit as st
from datetime import datetime, timedelta

# Expanded Limitation Map
LIMITATION_MAP = {
    "Consumer Complaint": {"days": 730, "desc": "Standard limitation under Consumer Protection Act."},
    "Cheque Bounce": {"days": 30, "desc": "From the date of receipt of notice of dishonour."},
    "Civil Suit (Contract/Breach)": {"days": 1095, "desc": "General limitation for breach of contract."},
    "Recovery of Possession": {"days": 4380, "desc": "12 years from the date the possession becomes adverse."},
    "Suit for Declaration": {"days": 1095, "desc": "3 years from the date when the right to sue first accrues."},
    "Execution of Decree": {"days": 4380, "desc": "12 years for decree of any Civil Court."},
    "Libel or Slander": {"days": 365, "desc": "1 year from the date the libel is published."},
    "Wages/Salary Suit": {"days": 1095, "desc": "3 years from the date the wages accrue due."}
}

st.set_page_config(page_title="Limitation Calculator", page_icon="⚖️")
st.title("⚖️ Legal Limitation Calculator")

cause_date = st.date_input("Date of Cause of Action")
case_type = st.selectbox("Select Case Type", list(LIMITATION_MAP.keys()) + ["Custom"])

if case_type == "Custom":
    limitation_days = st.number_input("Enter Limitation Period (Days)", min_value=1)
else:
    limitation_days = LIMITATION_MAP[case_type]["days"]
    st.info(LIMITATION_MAP[case_type]["desc"])

if st.button("Calculate Deadline"):
    last_date = cause_date + timedelta(days=limitation_days)
    
    st.divider()
    st.subheader(f"Deadline: {last_date.strftime('%B %d, %Y')}")
    
    today = datetime.today().date()
    if today <= last_date:
        days_remaining = (last_date - today).days
        st.success(f"Within Limitation. You have {days_remaining} days left.")
    else:
        delay = (today - last_date).days
        st.error(f"Time-Barred by {delay} days.")
