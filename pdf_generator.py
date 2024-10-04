import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

def generate_report(order):
    # Создаем папку для документов, если она не существует
    documents_dir = "documents"
    if not os.path.exists(documents_dir):
        os.makedirs(documents_dir)

    # Имя файла PDF с фамилией и именем клиента и номером заказа
    client_name = f"{order['surname']}_{order['first_name']}"
    pdf_filename = f"{documents_dir}/{client_name}_order_{order['id']}.pdf"

    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Регистрация шрифта для кириллицы
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

    # Припы и стили
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    normal_style.fontName = 'Arial'
    normal_style.fontSize = 12

    elements = []

    # Добавляем заголовок компании с заступом
    header = Paragraph("Технический центр <<ТехноПрогресс>>", ParagraphStyle(name='HeaderStyle', fontSize=16, fontName='Arial', alignment=1))
    elements.append(header)
    elements.append(Paragraph("<br/><br/>", normal_style)) # Разделитель

    # Адрес компании
    elements.append(Paragraph("Адрес: ул. Примерная, 1, Москва, Россия", normal_style))
    elements.append(Paragraph("Телефон: +7 (123) 456-7890", normal_style))
    elements.append(Paragraph("Email: info@techno-progress.ru", normal_style))
    elements.append(Paragraph(f"<br/>Дата: {datetime.today().strftime('%d-%m-%Y')}", normal_style)) #Доmо
    elements.append(Paragraph("<br/><br/>", normal_style)) # Разделитель

    # Добавляем данные о заказе PDF
    elements.append(Paragraph(f"Заказ #{order['id']}", normal_style))
    elements.append(Paragraph(f"Фамилия: {order['surname']}", normal_style))
    elements.append(Paragraph(f"Имя: {order['first_name']}", normal_style))
    elements.append(Paragraph(f"Отчество: {order['patronymic']}", normal_style))
    elements.append(Paragraph(f"Комплектующие: {', '.join(order['components'])}", normal_style))

    # Добавляем таблицу с компонентами
    data = [["№", "Компонент", "Цена", "Количество"]]
    for index, item in enumerate(order['components'], start=1):
        component_name, price, quantity = item
        data.append([str(index), component_name, f"{price} py6.", str(quantity)])
    table = Table(data, colWidths=[30, 200, 80, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#d3d3d3'),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('FONT', (0, 0), (-1, -1), 'Arial', 10),
        ('BACKGROUND', (-1, -1), (-1, -1), '#f2f2f2'),
    ]))
    elements.append(table)

    # Добавляем подписи
    elements.append(Paragraph("<br/><br/>", normal_style)) # Разделитель
    # Добавляем данные о заявке 6 PDF
    elements.append(Paragraph(f"Заявка #{order['id']}", normal_style))
    elements.append(Paragraph(f"Фамилия: {order['surname']}", normal_style))
    elements.append(Paragraph(f"Имя: {order['first_name']}", normal_style))
    elements.append(Paragraph(f"Отчество: {order['patronymic']}", normal_style))
    elements.append(Paragraph(f"Комплектующие: {order['components']}", normal_style))
    elements.append(Paragraph(f"Описание проблемы: {order['problem_description']}", normal_style))
    elements.append(Paragraph(f"Телефон: {order['phone']}", normal_style))
    elements.append(Paragraph(f"Email: {order['email']}", normal_style))
    elements.append(Paragraph(f"Ожидаемая дата вавершения: {order['expected_completion_date']}", normal_style))
    elements.append(Paragraph(f"Статус: {order['status']}", normal_style))
    # Добавляем место для подписей
    elements.append(Paragraph("<br/><br/>", normal_style)) # Разделитель
    signature_table = Table([["Подпись менеджера:", "Подпись клиента:"], ["Менеджер по продажам", "Клиент"]], colWidths=[250, 250])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (-1, -1), 'Arial', 12)
    ]))
    elements.append(signature_table)
    # Добавляем юридическую информацию
    elements.append(Paragraph("<br/><br/>", normal_style)) # Разделитель
    elements.append(Paragraph("Юридическая информация:", normal_style))
    elements.append(Paragraph("Общество с ограниченной ответственностью <<ТехноПрогресс>>", normal_style))
    elements.append(Paragraph("ИНН: 1234567890", normal_style))
    elements.append(Paragraph("КПП: 0987654321", normal_style))
    elements.append(Paragraph("ОГРН: 1234567890123", normal_style))
    elements.append(Paragraph("Юридический адрес: ул. Примерная, 1, Москва, Россия", normal_style))

    doc.build(elements)
    print(f"Документ для заказа {order['id']} создан: {pdf_filename}")

