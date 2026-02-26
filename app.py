import streamlit as st
import pandas as pd
from report_generator import generate_pdf_report
from modules.loader import load_file
from modules.cleaner import clean_data
from modules.analyzer import dataset_summary
from modules.visualizer import (
    plot_numeric,
    plot_categorical,
    plot_correlation
)
from modules.insights import generate_insights

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Auto Insight Dashboard",
    layout="wide"
)

st.title("📊 Auto Insight – Smart Data Analyzer")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload your dataset (CSV or Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file:

    # ================= LOAD DATA =================
    try:
        df = load_file(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    # ================= DATASET SUMMARY =================
    summary = dataset_summary(df)

    st.subheader("📌 Dataset Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", summary["rows"])
    col2.metric("Columns", summary["columns"])
    col3.metric("Duplicate Rows", summary["duplicates"])

    missing_data = summary["missing_values"]
    missing_filtered = missing_data[missing_data > 0]

    if not missing_filtered.empty:
        st.write("### Missing Values")
        st.dataframe(missing_filtered)

    st.write("### Raw Data Preview")
    st.dataframe(df.head())

    # ================= CLEAN DATA =================
    cleaned_df = clean_data(df)

    st.subheader("🧹 Cleaned Data Preview")
    st.dataframe(cleaned_df.head())

    st.download_button(
        label="Download Cleaned Dataset",
        data=cleaned_df.to_csv(index=False),
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

    # ================= INSIGHT ENGINE =================
    st.subheader("🧠 Smart Data Insights")

    quality_score, insights = generate_insights(cleaned_df)

    st.metric("Dataset Quality Score", f"{quality_score}/100")

    if insights:
        for insight in insights:
            st.write(insight)
    else:
        st.success("Dataset looks clean and well structured.")

    # ================= VISUALIZATION =================
    st.subheader("📊 Automated Visual Analysis")

    numeric_cols = cleaned_df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    categorical_cols = cleaned_df.select_dtypes(
        include=["object"]
    ).columns

    if len(numeric_cols) > 0:
        st.write("### Numeric Distributions")
        for col in numeric_cols:
            fig = plot_numeric(cleaned_df, col)
            st.pyplot(fig)

    if len(categorical_cols) > 0:
        st.write("### Categorical Analysis")
        for col in categorical_cols:
            fig = plot_categorical(cleaned_df, col)
            st.pyplot(fig)

    if len(numeric_cols) > 1:
        st.write("### Correlation Heatmap")
        fig = plot_correlation(cleaned_df, numeric_cols)
        st.pyplot(fig)

    # ================= PDF REPORT GENERATION =================
    st.subheader("📄 Export Professional Report")

    duplicate_count = summary["duplicates"]
    missing_values = summary["missing_values"]

    if st.button("Generate PDF Report"):
        pdf_file = generate_pdf_report(
            cleaned_df,
            quality_score,
            duplicate_count,
            missing_values
        )

        st.download_button(
            label="⬇ Download Report",
            data=pdf_file,
            file_name="Auto_Insight_Report.pdf",
            mime="application/pdf"
        )

    st.success("Analysis Completed Successfully 🚀")