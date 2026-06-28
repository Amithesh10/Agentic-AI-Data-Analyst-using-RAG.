from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_pdf_report(eda, kpis):
    file_path = "ai_data_analyst_report.pdf"

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 50

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "Agentic AI Data Analyst Report")

    y -= 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "EDA Summary")

    y -= 25

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Rows: {eda['rows']}")
    y -= 18
    c.drawString(50, y, f"Columns: {eda['columns']}")
    y -= 18
    c.drawString(50, y, f"Missing Values: {eda['missing_values']}")
    y -= 18
    c.drawString(50, y, f"Duplicate Rows: {eda['duplicate_rows']}")

    y -= 35

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "KPI Summary")

    y -= 25

    c.setFont("Helvetica", 10)

    for col, values in kpis.items():
        if y < 100:
            c.showPage()
            y = height - 50

        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, f"Column: {col}")
        y -= 18

        c.setFont("Helvetica", 10)

        for key, value in values.items():
            c.drawString(70, y, f"{key}: {value}")
            y -= 15

        y -= 10

    c.save()

    return file_path