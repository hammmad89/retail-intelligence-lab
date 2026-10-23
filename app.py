
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Retail Intelligence Lab",
    page_icon="📊",
    layout="wide"
)

# ---------- THEME ----------
st.markdown("""
<style>
.stApp {
    background: #0B1220;
    color: #F1F5F9;
}
[data-testid="stMetric"] {
    background: #142235;
    border: 1px solid #263B50;
    padding: 16px;
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

# ---------- HEADER ----------
st.title("RETAIL INTELLIGENCE LAB")
st.caption("E-Commerce Sales & Customer Behavior Analytics")
st.divider()

# ---------- LOAD DATA ----------
@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )
    df["Quantity"] = pd.to_numeric(
        df["Quantity"], errors="coerce"
    )
    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"], errors="coerce"
    )
    df["CustomerID"] = df["CustomerID"].astype("string")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]
    return df

possible_files = [
    Path("Online Retail.xlsx"),
    Path("data/Online Retail.xlsx")
]

data_path = next((p for p in possible_files if p.exists()), None)

if data_path is None:
    st.error("Dataset not found. Upload Online Retail.xlsx to the repository root.")
    st.stop()

try:
    df = load_data(str(data_path))
except Exception as e:
    st.error(f"Could not load the dataset: {e}")
    st.stop()

required = {
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country", "Sales"
}
if not required.issubset(df.columns):
    st.error("The dataset does not contain all expected Online Retail columns.")
    st.stop()

# ---------- FILTERS ----------
st.sidebar.header("Dashboard Filters")

valid_dates = df["InvoiceDate"].dropna()
if valid_dates.empty:
    st.error("No valid invoice dates were found.")
    st.stop()

min_date = valid_dates.min().date()
max_date = valid_dates.max().date()

date_range = st.sidebar.date_input(
    "Invoice date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

countries = sorted(df["Country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Countries",
    options=countries,
    default=["United Kingdom"] if "United Kingdom" in countries else countries[:1]
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

mask = (
    df["InvoiceDate"].dt.date.between(start_date, end_date)
    & df["Country"].isin(selected_countries)
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
    & (~df["InvoiceNo"].astype(str).str.startswith("C"))
)

sales_df = df.loc[mask].copy()

if sales_df.empty:
    st.warning("No transactions match the selected filters. Adjust the filters.")
    st.stop()

# ---------- KPI CARDS ----------
total_sales = sales_df["Sales"].sum()
invoice_count = sales_df["InvoiceNo"].nunique()
customer_count = sales_df["CustomerID"].nunique()
product_count = sales_df["StockCode"].nunique()
avg_invoice = total_sales / invoice_count if invoice_count else 0

st.subheader("Executive Overview")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Sales Value", f"£{total_sales:,.0f}")
c2.metric("Invoices", f"{invoice_count:,}")
c3.metric("Customers", f"{customer_count:,}")
c4.metric("Products", f"{product_count:,}")
c5.metric("Avg. Invoice Value", f"£{avg_invoice:,.2f}")

st.caption(
    "Sales value is Quantity × UnitPrice, not profit. "
    "Customer counts exclude missing customer IDs."
)

# ---------- MONTHLY SALES ----------
st.divider()
st.subheader("Sales Performance")

sales_df["Month"] = sales_df["InvoiceDate"].dt.to_period("M").astype(str)
monthly = (
    sales_df.groupby("Month", as_index=False)["Sales"]
    .sum()
    .sort_values("Month")
)

fig_month = px.line(
    monthly, x="Month", y="Sales",
    markers=True, title="Monthly Sales Trend",
    template="plotly_dark"
)
fig_month.update_traces(line_color="#45D6C5")
fig_month.update_layout(
    paper_bgcolor="#0B1220",
    plot_bgcolor="#0B1220"
)
st.plotly_chart(fig_month, use_container_width=True)

# ---------- COUNTRY AND PRODUCT ----------
left, right = st.columns(2)

country_sales = (
    sales_df.groupby("Country", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=True)
    .tail(10)
)

with left:
    fig_country = px.bar(
        country_sales, x="Sales", y="Country",
        orientation="h",
        title="Top Countries by Sales",
        template="plotly_dark"
    )
    fig_country.update_traces(marker_color="#45D6C5")
    fig_country.update_layout(
        paper_bgcolor="#0B1220",
        plot_bgcolor="#0B1220"
    )
    st.plotly_chart(fig_country, use_container_width=True)

product_sales = (
    sales_df.groupby("Description", as_index=False)
    .agg(Sales=("Sales", "sum"), Units=("Quantity", "sum"))
    .sort_values("Sales", ascending=False)
    .head(10)
)

with right:
    fig_products = px.bar(
        product_sales.sort_values("Sales"),
        x="Sales", y="Description",
        orientation="h",
        title="Top 10 Products by Sales",
        template="plotly_dark"
    )
    fig_products.update_traces(marker_color="#F5B544")
    fig_products.update_layout(
        paper_bgcolor="#0B1220",
        plot_bgcolor="#0B1220",
        yaxis_title=""
    )
    st.plotly_chart(fig_products, use_container_width=True)

# ---------- CUSTOMER INTELLIGENCE ----------
st.divider()
st.subheader("Customer Intelligence")

identified = sales_df.dropna(subset=["CustomerID"]).copy()

if not identified.empty:
    orders = (
        identified.groupby("CustomerID")["InvoiceNo"]
        .nunique()
        .rename("Orders")
        .reset_index()
    )
    orders["Segment"] = orders["Orders"].apply(
        lambda n: "One-time" if n == 1
        else ("Occasional" if n <= 5 else "Frequent")
    )

    segment_counts = (
        orders["Segment"].value_counts()
        .reindex(["One-time", "Occasional", "Frequent"], fill_value=0)
        .rename_axis("Segment")
        .reset_index(name="Customers")
    )

    a, b = st.columns(2)

    with a:
        fig_segments = px.bar(
            segment_counts, x="Segment", y="Customers",
            title="Customer Purchase Frequency",
            template="plotly_dark",
            color="Segment",
            color_discrete_map={
                "One-time": "#64748B",
                "Occasional": "#45D6C5",
                "Frequent": "#F5B544"
            }
        )
        fig_segments.update_layout(
            paper_bgcolor="#0B1220",
            plot_bgcolor="#0B1220",
            showlegend=False
        )
        st.plotly_chart(fig_segments, use_container_width=True)

    top_customers = (
        identified.groupby("CustomerID", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )
    top_customers["CustomerID"] = top_customers["CustomerID"].astype(str)

    with b:
        fig_customers = px.bar(
            top_customers.sort_values("Sales"),
            x="Sales", y="CustomerID",
            orientation="h",
            title="Top 10 Customers by Sales",
            template="plotly_dark"
        )
        fig_customers.update_traces(marker_color="#F5B544")
        fig_customers.update_layout(
            paper_bgcolor="#0B1220",
            plot_bgcolor="#0B1220",
            yaxis_title=""
        )
        st.plotly_chart(fig_customers, use_container_width=True)
else:
    st.info("No identified customers are available for this selection.")

# ---------- DATA TABLE ----------
with st.expander("Explore filtered transaction data"):
    st.dataframe(
        sales_df[
            ["InvoiceNo", "InvoiceDate", "Description",
             "Quantity", "UnitPrice", "Sales", "Country", "CustomerID"]
        ].head(500),
        use_container_width=True
    )

st.divider()
st.caption(
    "Retail Intelligence Lab | Python • Streamlit • Pandas • Plotly | "
    "Historical data analysis"
)
