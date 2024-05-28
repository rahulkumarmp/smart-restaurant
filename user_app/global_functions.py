import os
from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from admin_app.models import Invoice
import os
from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

def generate_invoice_pdf(table, cart_items):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Invoice ID and Date
    invoice_id = table.id  # Using table ID as invoice ID for simplicity
    date = table.created_at.strftime('%Y-%m-%d')

    elements.append(Paragraph(f"Invoice ID: {invoice_id}", styles['Title']))
    elements.append(Paragraph(f"Date: {date}", styles['Title']))
    elements.append(Spacer(1, 12))

    # Item Details with Total Amount
    item_data = [["Item", "Quantity", "Price (INR)"]]
    total_amount = 0
    for item in cart_items:
        item_total = item.total_price * item.quantity
        item_data.append([item.menu.name, item.quantity, f"{item_total}"])
        total_amount += item_total

    item_data.append(["", "Total Amount", f"{total_amount}"])

    item_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    item_table = Table(item_data, colWidths=[200, 100, 100])
    item_table.setStyle(item_style)
    elements.append(item_table)

    # Build PDF
    doc.build(elements)

    pdf_file = ContentFile(buffer.getvalue())
    buffer.close()

    invoice = Invoice.objects.create(table=table)
    invoice.file.save(f'invoice_{table.id}.pdf', pdf_file)

    return invoice
