# from openpyxl import Workbook
#
# wb = Workbook()
#
# hei = input()
# wb.create_sheet(hei)
# ws = "ws_"
# ws_brand = ws + hei
# ws_sheet = wb[ws_brand]
# ws_brand = ws_sheet
#
# print(ws_brand)


pris = "10 000 kr"
prisstrip = pris.replace(" ", "").split("kr")[0]
print(prisstrip)