from openpyxl import Workbook  # To create excel sheets

wb = Workbook()
ws = wb.active
ws.title = "Changed Sheet"

wb.save(filename = 'sample_book.xlsx')