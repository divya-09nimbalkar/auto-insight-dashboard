import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auto Insight Dashboard", layout="wide")

st.title("📊 Auto Insight – Smart Data Analyzer")

uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())