import streamlit as st
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed_bank_data.csv"

df = pd.read_csv(DATA_FILE)
# Title
st.title("Customer Engagement & Product Utilization Analytics")

st.markdown("""
This dashboard evaluates customer retention through engagement,
product utilization, and relationship strength.
""")

# Sidebar Filters

# Sidebar Filters
st.sidebar.header("Filters")

balance_filter = st.sidebar.slider(
    "Minimum Balance",
    0,
    int(df["Balance"].max()),
    0
)

salary_filter = st.sidebar.slider(
    "Minimum Salary",
    0,
    int(df["EstimatedSalary"].max()),
    0
)

product_filter = st.sidebar.slider(
    "Minimum Products",
    1,
    int(df["NumOfProducts"].max()),
    1
)

engagement_filter = st.sidebar.selectbox(
    "Engagement Status",
    ["All", "Active", "Inactive"]
)



filtered_df = df[
    (df["Balance"] >= balance_filter) &
    (df["EstimatedSalary"] >= salary_filter) &
    (df["NumOfProducts"] >= product_filter)
]

# Apply engagement filter
if engagement_filter == "Active":
    filtered_df = filtered_df[
        filtered_df["IsActiveMember"] == 1
    ]

elif engagement_filter == "Inactive":
    filtered_df = filtered_df[
        filtered_df["IsActiveMember"] == 0
    ]




# KPIs
st.header("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Customers",
    len(filtered_df)
)

col2.metric(
    "Churn Rate",
    f"{filtered_df['Exited'].mean()*100:.2f}%"
)

col3.metric(
    "Average RSI",
    f"{filtered_df['RSI'].mean():.2f}"
)

col4.metric(
    "Average Products",
    f"{filtered_df['NumOfProducts'].mean():.2f}"
)

# Engagement vs Churn
st.header("Engagement vs Churn")

fig1 = px.histogram(
    filtered_df,
    x="IsActiveMember",
    color="Exited",
    barmode="group"
)

st.plotly_chart(fig1, use_container_width=True)

# Product Utilization
st.header("Product Utilization Analysis")

product_churn = (
    filtered_df
    .groupby("NumOfProducts")["Exited"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    product_churn,
    x="NumOfProducts",
    y="Exited",
    title="Churn Rate by Product Count"
)

st.plotly_chart(fig2, use_container_width=True)

# Engagement Profile
st.header("Engagement Profiles")

profile_counts = (
    filtered_df["EngagementProfile"]
    .value_counts()
    .reset_index()
)

profile_counts.columns = [
    "Profile",
    "Count"
]

fig3 = px.pie(
    profile_counts,
    names="Profile",
    values="Count"
)

st.plotly_chart(fig3, use_container_width=True)

# RSI Distribution
st.header("Relationship Strength")

fig4 = px.histogram(
    filtered_df,
    x="RSI",
    nbins=20
)

st.plotly_chart(fig4, use_container_width=True)

# At Risk Customers
st.header("At-Risk Premium Customers")

risk_df = filtered_df[
    filtered_df["AtRiskPremium"] == 1
]

st.dataframe(
    risk_df[
        [
            "CustomerId",
            "Balance",
            "EstimatedSalary",
            "NumOfProducts",
            "RSI"
        ]
    ]
)

# Geography Analysis
st.header("Geographic Distribution")

geo = (
    filtered_df["Geography"]
    .value_counts()
    .reset_index()
)

geo.columns = ["Country","Count"]

fig5 = px.bar(
    geo,
    x="Country",
    y="Count"
)

st.plotly_chart(fig5, use_container_width=True)
