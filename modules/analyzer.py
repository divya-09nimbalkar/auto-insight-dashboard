def dataset_summary(df):

    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "duplicates": df.duplicated().sum(),
        "missing_values": df.isnull().sum()
    }

    return summary