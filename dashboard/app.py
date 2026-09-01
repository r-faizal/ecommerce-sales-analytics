import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="E-commerce Sales Analytics",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv(
    "data/processed/cleaned_data.csv",
    parse_dates=["InvoiceDate"]
)


st.sidebar.header("Filters")

# Date filter

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Country filter

countries = sorted(df["Country"].dropna().unique())

selected_countries = st.sidebar.multiselect(
    "Country",
    options=countries,
    default=countries
)

# Apply filters

filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["InvoiceDate"].dt.date >= start_date)
        & (filtered_df["InvoiceDate"].dt.date <= end_date)
    ]

if selected_countries:
    filtered_df = filtered_df[
        filtered_df["Country"].isin(selected_countries)
    ]



# Dashboard Title

st.title("E-Commerce Sales Analytics Dashboard")

st.write(
    "Explore sales performance, customer behaviour, "
    "and product trends."
)

# Calculate KPIs

total_revenue = filtered_df["Revenue"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
total_customers = filtered_df["CustomerID"].nunique()

if total_orders > 0:
    average_order_value = total_revenue / total_orders
else:
    average_order_value = 0


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"£{total_revenue:,.2f}"
)

col2.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Customers",
    f"{total_customers:,}"
)

col4.metric(
    "Average Order Value",
    f"£{average_order_value:,.2f}"
)

# Revenue over time

st.subheader("Revenue Over Time")

daily_revenue = (
    filtered_df
    .groupby(filtered_df["InvoiceDate"].dt.date)["Revenue"]
    .sum()
    .reset_index()
)

daily_revenue.columns = ["Date", "Revenue"]

st.line_chart(
    daily_revenue,
    x="Date",
    y="Revenue"
)