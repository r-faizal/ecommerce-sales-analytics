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

# Top 10 Products by Revenue

st.subheader("Top 10 Products by Revenue")

top_products = (
    filtered_df
    .groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

st.bar_chart(top_products)

# Top 10 Products by quantity sold

st.subheader("Top 10 Products by Quantity Sold")

top_products_quantity = (
    filtered_df
    .groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

st.bar_chart(top_products_quantity)

# Top 10 customers by revenue

st.subheader("Top 10 Customers by Revenue")

top_customers = (
    filtered_df
    .groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

st.bar_chart(top_customers)

# Customer purchase frequency

st.subheader("Customer Purchase Frequency")

customer_orders = (
    filtered_df
    .groupby("CustomerID")["InvoiceNo"]
    .nunique()
)

one_time_customers = (customer_orders == 1).sum()
repeat_customers = (customer_orders > 1).sum()

customer_frequency = pd.Series(
    {
        "One-time Customers": one_time_customers,
        "Repeat Customers": repeat_customers
    }
)

st.bar_chart(customer_frequency)

# Top 10 countries by revenue

st.subheader("Top 10 Countries by Revenue")

top_countries = (
    filtered_df
    .groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

st.bar_chart(top_countries)