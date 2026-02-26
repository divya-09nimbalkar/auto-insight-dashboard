import matplotlib.pyplot as plt
import seaborn as sns

def plot_numeric(df, column):
    fig, ax = plt.subplots()
    sns.histplot(df[column], kde=True, ax=ax)
    ax.set_title(f"{column} Distribution")
    return fig

def plot_categorical(df, column):
    fig, ax = plt.subplots()
    df[column].value_counts().head(10).plot(kind='bar', ax=ax)
    ax.set_title(f"{column} Top Categories")
    return fig

def plot_correlation(df, numeric_cols):
    fig, ax = plt.subplots(figsize=(8,6))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap")
    return fig