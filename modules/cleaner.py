import pandas as pd
import numpy as np

def clean_data(df):

    df = df.copy()

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Replace string None / null values
    df.replace(["None", "none", "null", "NULL", ""], np.nan, inplace=True)

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    # Replace infinite values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # -------- Numeric Handling --------
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns

    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

        # IQR outlier capping
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        df[col] = np.where(df[col] < lower, lower, df[col])
        df[col] = np.where(df[col] > upper, upper, df[col])

    # -------- Categorical Handling --------
    cat_cols = df.select_dtypes(include=["object"]).columns

    for col in cat_cols:
        df[col] = df[col].str.strip().str.lower()
        df[col] = df[col].fillna(df[col].mode()[0])

    return df