import streamlit as st
from datetime import datetime, timedelta

# -------------------------------
# CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Alpine AI",
    layout="wide",
    page_icon="⚖️"
)

# -------------------------------
# STYLING (Blue, White, Professional)
# -------------------------------
st.markdown("""
<style>
    /* Font and Background */
    body { font-family: 'Times New Roman', serif; background-color: #f8f9fa; }
    
    /* Headers */
    h1, h2, h3 { color: #004a99; }
    
    /* Cards */
    .card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #004a99;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #004a99;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover { background-color: #003366; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
col1, col2 = st.columns([1, 10])
with col1:
    # Ensure "Alpine monogram.png" is in your repo folder
    st.image("Alpine monogram.png", width=70)
with col2:
    st.title("Alpine AI")
    st.subheader("Legal Intelligence Suite")

# -------------------------------
# NAVIGATION
# -------------------------------
menu = st.sidebar.radio("Navigation", ["Dashboard", "Limitation", "Court Fees", "Drafting"])

# -------------------------------
# PAGES
# -------------------------------
if menu == "Dashboard":
    st.markdown("### Welcome, Advocate.")
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="card">📅 **Limitation Calculator**</div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="card">💰 **Court Fee Calculator**</div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="card">📝 **Drafting Assistant**</div>', unsafe_allow_html=True)

elif menu == "Limitation":
    st.header("📅 Limitation Calculator")
    c1, c2 = st.columns(2)
    with c1: cause_date = st.date_input("Cause of Action Date")
    with c2: lim_days = st.number_input("Limitation Period (Days)", min_value=1, value=30)
    
    if st.button("Calculate"):
        start_date = cause_date + timedelta(days=1)
        last_date = start_date + timedelta(days=lim_days - 1)
        today = datetime.today().date()
        
        st.metric("Last Date to File", last_date.strftime("%d-%m-%Y"))
        if today <= last_date:
            st.success("Within Limitation (Sec. 3)")
        else:
            st.error(f"Delay of {(today - last_date).days} days — Sec. 5 condonation required.")

elif menu == "Court Fees":
    st.header("💰 Court Fee Calculator")
    s_type = st.selectbox("Suit Type", ["Money Suit", "Injunction", "Declaration"])
    val = st.number_input("Suit Value (₹)", min_value=0)
    
    if st.button("Calculate Fee"):
        fee = (val * 0.01) if s_type == "Money Suit" else (500 if s_type == "Injunction" else 1000)
        st.metric("Estimated Court Fee", f"₹ {int(fee):,}")

elif menu == "Drafting":
    st.header("📝 Drafting Assistant")
    d_type = st.selectbox("Draft Type", ["Legal Notice", "Writ Petition", "Cheque Bounce (Sec 138)"])
    facts = st.text_area("Facts", height=150)
    relief = st.text_area("Relief", height=100)
    
    if st.button("Generate Draft"):
        draft = f"--- {d_type.upper()} ---\n\nFacts:\n{facts}\n\nRelief:\n{relief}\n\nFiled before appropriate authority."
        st.text_area("Draft Output", draft, height=300)
