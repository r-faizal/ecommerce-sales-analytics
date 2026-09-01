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

st.title("E-Commerce Sales Analytics Dashboard")

st.write(
    "Explore sales performance, customer behaviour, "
    "and product trends."
)

st.write("Number of records:", len(df))