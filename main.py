from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Регистрация шрифтов
pdfmetrics.registerFont(TTFont('Helvetica', 'Helvetica.ttf'))
pdfmetrics.registerFont(TTFont('HelveticaBold', 'HelveticaBold.ttf'))
pdfmetrics.registerFontFamily('Helvetica', normal='Helvetica', bold='HelveticaBold')


def read_names_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        names = [line.strip() for line in file if line.strip()]
    return names


def create_pdf_with_table(names, filename, enable_borders=False):
    doc = SimpleDocTemplate(filename, pagesize=A4, leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm,
                            bottomMargin=10 * mm)

    style = ParagraphStyle('Style')
    style.fontName = 'Helvetica'
    style.fontSize = 16
    style.leading = 18  # Межстрочный интервал
    style.alignment = 1  # По центру
    elements = []
    data_for_table = []
    for name in names:
        first_name, last_name = name.split(maxsplit=1)
        formatted_name = f'<b>{first_name}</b><br/>{last_name}'
        data_for_table.append(Paragraph(formatted_name, style))
        if len(data_for_table) == 21:  # Когда достаточно для таблицы
            table = Table([data_for_table[i:i + 3] for i in range(0, 21, 3)], colWidths=[(A4[0] - 20 * mm) / 3] * 3,
                          rowHeights=[(A4[1] - 20 * mm) / 7] * 7)
            if enable_borders:
                table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black)]))
            elements.append(table)
            data_for_table = []

    # Добавляем оставшиеся данные, если они есть
    if data_for_table:
        rows_needed = len(data_for_table) // 3 + (1 if len(data_for_table) % 3 else 0)
        table = Table([data_for_table[i:i + 3] for i in range(0, len(data_for_table), 3)],
                              colWidths=[(A4[0] - 20 * mm) / 3] * 3, rowHeights=[(A4[1] - 20 * mm) / 7] * rows_needed)
        if enable_borders:
            table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black)]))
        elements.append(table)

    doc.build(elements)


if __name__ == '__main__':
    filename = 'names.txt'
    output_pdf = 'names_table.pdf'
    enable_borders = True
    names = read_names_from_file(filename)
    create_pdf_with_table(names, output_pdf, enable_borders)
