import streamlit as st
from datetime import datetime, timedelta

st.title("Limitation Calculator")

LIMITATION_MAP = {
    "Consumer Complaint (2 years)": 730,
    "Cheque Bounce (30 days)": 30,
    "Civil Suit – Contract (3 years)": 1095,
}

cause_date = st.date_input("Cause of Action Date")

case_type = st.selectbox("Case Type", list(LIMITATION_MAP.keys()) + ["Custom"])

if case_type == "Custom":
    limitation_days = st.number_input("Enter Limitation (Days)", min_value=1)
else:
    limitation_days = LIMITATION_MAP[case_type]

if st.button("Calculate"):
    start_date = cause_date + timedelta(days=1)
    last_date = start_date + timedelta(days=limitation_days - 1)
    
    today = datetime.today().date()
    
    if today <= last_date:
        st.success(f"Within Limitation. Last Date: {last_date}")
    else:
        delay = (today - last_date).days
        st.error(f"Time-Barred by {delay} days")
