
import streamlit as st

st.set_page_config(
    page_title="Retail Intelligence Lab",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0B1220;
    color: #F1F5F9;
}
[data-testid="stMetric"] {
    background-color: #142235;
    border: 1px solid #263B50;
    padding: 20px;
    border-radius: 12px;
}
[data-testid="stMetricLabel"] {
    color: #94A3B8;
}
[data-testid="stMetricValue"] {
    color: #45D6C5;
}
h1, h2, h3 {
    color: #F8FAFC;
}
</style>
""", unsafe_allow_html=True)

st.title("RETAIL INTELLIGENCE LAB")
st.caption("E-Commerce Sales & Customer Behavior Analytics")

st.divider()

st.subheader("Executive Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales Value", "Load dataset next")
col2.metric("Sales Invoices", "—")
col3.metric("Identified Customers", "—")
col4.metric("Products", "—")

st.info(
    "Dashboard foundation created. "
    "In the next steps, we will connect the retail dataset "
    "and replace these placeholders with calculated KPIs."
)

st.subheader("Dashboard Modules")

left, right = st.columns(2)

with left:
    st.markdown("### Sales Performance")
    st.write("Monthly trends, country performance, and top products.")

with right:
    st.markdown("### Customer Intelligence")
    st.write("Purchase frequency, high-value customers, and segmentation.")

st.divider()
st.caption("Built with Python • Streamlit • Pandas • SQL")
