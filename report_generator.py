from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile


def generate_pdf_report(df, quality_score, duplicate_count, missing_values):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
    elements = []
    styles = getSampleStyleSheet()

    # ================= TITLE =================
    elements.append(Paragraph("Auto Insight - Data Analysis Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    date_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elements.append(Paragraph(date_text, styles["Normal"]))
    elements.append(Spacer(1, 0.4 * inch))

    # ================= DATASET SUMMARY =================
    elements.append(Paragraph("Dataset Summary", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    summary_data = [
        ["Metric", "Value"],
        ["Total Rows", len(df)],
        ["Total Columns", len(df.columns)],
        ["Duplicate Rows", duplicate_count],
        ["Quality Score", f"{quality_score}/100"]
    ]

    summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 0.4 * inch))

    # ================= MISSING VALUES =================
    elements.append(Paragraph("Missing Values Breakdown", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    missing_filtered = missing_values[missing_values > 0]

    if not missing_filtered.empty:
        table_data = [["Column Name", "Missing Count"]]
        for col, val in missing_filtered.items():
            table_data.append([col, str(int(val))])

        missing_table = Table(table_data, colWidths=[3 * inch, 2 * inch])
        missing_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ]))

        elements.append(missing_table)
    else:
        elements.append(Paragraph("No missing values detected.", styles["Normal"]))

    elements.append(Spacer(1, 0.5 * inch))

    # ================= VISUAL ANALYSIS =================
    elements.append(Paragraph("Visual Analysis", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * inch))

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    # -------- NUMERIC BOXPLOTS --------
    if len(numeric_cols) > 0:
        elements.append(Paragraph("Numeric Distributions", styles["Heading3"]))
        elements.append(Spacer(1, 0.2 * inch))

        for col in numeric_cols:
            plt.figure()
            df[col].plot(kind="box")
            plt.title(f"{col} Distribution")

            tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            plt.savefig(tmpfile.name, bbox_inches="tight")
            plt.close()

            img = Image(tmpfile.name, width=4 * inch, height=3 * inch)
            elements.append(img)
            elements.append(Spacer(1, 0.3 * inch))

    # -------- CATEGORICAL BAR CHARTS --------
    if len(categorical_cols) > 0:
        elements.append(Paragraph("Categorical Analysis", styles["Heading3"]))
        elements.append(Spacer(1, 0.2 * inch))

        for col in categorical_cols:
            plt.figure()
            df[col].value_counts().head(10).plot(kind="bar")
            plt.title(f"{col} Distribution")
            plt.xticks(rotation=45)

            tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            plt.savefig(tmpfile.name, bbox_inches="tight")
            plt.close()

            img = Image(tmpfile.name, width=4 * inch, height=3 * inch)
            elements.append(img)
            elements.append(Spacer(1, 0.3 * inch))

    # -------- CORRELATION HEATMAP --------
    if len(numeric_cols) > 1:
        elements.append(Paragraph("Correlation Heatmap", styles["Heading3"]))
        elements.append(Spacer(1, 0.2 * inch))

        plt.figure(figsize=(6, 4))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")

        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        plt.savefig(tmpfile.name, bbox_inches="tight")
        plt.close()

        img = Image(tmpfile.name, width=5 * inch, height=4 * inch)
        elements.append(img)
        elements.append(Spacer(1, 0.4 * inch))

    # ================= BUILD PDF =================
    doc.build(elements)
    buffer.seek(0)

    return buffer.getvalue()