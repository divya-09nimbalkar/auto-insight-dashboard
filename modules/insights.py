import numpy as np

def generate_insights(df):

    insights = []
    score = 100

    # Missing values penalty
    missing_percent = (df.isnull().sum() / len(df)) * 100
    high_missing = missing_percent[missing_percent > 20]

    if len(high_missing) > 0:
        score -= 15
        insights.append("⚠ Some columns have more than 20% missing values.")

    # Duplicate penalty
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        score -= 10
        insights.append(f"⚠ Dataset contains {duplicates} duplicate rows.")

    # Skewness check
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns
    for col in numeric_cols:
        skew = df[col].skew()
        if abs(skew) > 1:
            insights.append(f"📈 Column '{col}' is highly skewed.")

    # Correlation check
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr().abs()
        high_corr = (corr_matrix > 0.8) & (corr_matrix < 1.0)

        if high_corr.sum().sum() > 0:
            score -= 10
            insights.append("🔗 Strong correlations detected between numeric variables.")

    # Final score adjustment
    if score < 0:
        score = 0

    return score, insights