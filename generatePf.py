from fpdf import FPDF


pdf = FPDF()

def generate_pdf(txt, filename):
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, txt=txt, align='C')
    pdf.output(f"reciepts/{filename}")

# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet


# def generate_pdf(payment, filename):
#     doc = SimpleDocTemplate(f"receipts/{filename}", pagesize=A4)
#     styles = getSampleStyleSheet()

#     elements = []

#     # Title
#     title = Paragraph("<b>PAYMENT RECEIPT</b>", styles["Title"])
#     elements.append(title)
#     elements.append(Spacer(1, 20))

#     # Company name (customize this)
#     company = Paragraph("<b>Hewstech Computers Solutions Ltd</b>", styles["Normal"])
#     elements.append(company)
#     elements.append(Spacer(1, 20))

#     # Table data
#     data = [
#         ["Transaction Code", payment.transaction_code],
#         ["Amount Paid", f"KES {payment.amount}"],
#         ["Phone Number", payment.phone_paid],
#         ["Status", payment.status],
#     ]

#     table = Table(data, colWidths=[150, 250])
#     table.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
#         ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),

#         ("GRID", (0, 0), (-1, -1), 1, colors.black),
#         ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

#         ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
#         ("PADDING", (0, 0), (-1, -1), 10),
#     ]))

#     elements.append(table)
#     elements.append(Spacer(1, 30))

#     # Footer
#     footer = Paragraph("Thank you for your payment!", styles["Italic"])
#     elements.append(footer)

#     doc.build(elements)