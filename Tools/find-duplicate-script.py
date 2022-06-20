# from openpyxl import Workbook, load_workbook  # To create excel sheets
#
# wb = load_workbook('/Users/mortaza/Downloads/2022-06-08.xlsx')
# ws = wb["Hvitevarer"]
#
# andre_hvitevarer = 0
# frysere = 0
# innbyggingsovner = 0
# kjøleskap = 0
# komfyrer = 0
# mikrobølgeovner = 0
# oppvaskmaskiner = 0
# platetopper = 0
# tørketromler = 0
# vaskemaskiner = 0
# ventilatorer = 0
#
# for i in range(2, 9101):
#     cell = f'B{i}'
#     verdi = ws[cell].value
#     if verdi == "andre hvitevarer":
#         andre_hvitevarer += 1
#     elif verdi == "frysere":
#         frysere += 1
#     elif verdi == "innbyggingsovner":
#         innbyggingsovner += 1
#     elif verdi == "kjøleskap":
#         kjøleskap += 1
#     elif verdi == "komfyrer":
#         komfyrer += 1
#     elif verdi == "mikrobølgeovner":
#         mikrobølgeovner += 1
#     elif verdi == "oppvaskmaskiner":
#         oppvaskmaskiner += 1
#     elif verdi == "platetopper":
#         platetopper += 1
#     elif verdi == "tørketromler":
#         tørketromler += 1
#     elif verdi == "vaskemaskiner":
#         vaskemaskiner += 1
#     elif verdi == "ventilatorer":
#         ventilatorer += 1
#     else:
#         print(f"HVA FAEN {verdi}")
#
# print(andre_hvitevarer)
# print(frysere)
# print(innbyggingsovner)
# print(kjøleskap)
# print(komfyrer)
# print(mikrobølgeovner)
# print(oppvaskmaskiner)
# print(platetopper)
# print(tørketromler)
# print(vaskemaskiner)
# print(ventilatorer)
#


from openpyxl import Workbook, load_workbook  # To create excel sheets
from datetime import datetime

wb1 = load_workbook(
    '/Scrapped Data Static/Hvitevarer.xlsx')
ws1 = wb1["Hvitevarer"]

wb2 = load_workbook(
    '/2022-06-08.xlsx')
ws2 = wb2["Hvitevarer"]

wb = Workbook()
wb.create_sheet("Hvitevarer")
ws = wb["Hvitevarer"]
ws.append(["Varenavn", "Under kategori", "Kategori (type)", "Pris", "Merke", "Postnummer", "Lokasjon"])

for i in range(2, 10_000):
    duplicate = False
    cell1 = f'H{i}'
    finn_kode1 = ws1[cell1].value

    for k in range(2, 10_000):
        cell2 = f'H{k}'
        finn_kode2 = ws2[cell2].value

        if finn_kode1 == finn_kode2:
            duplicate = True
            break

    if duplicate is False:
        ws.append([ws1[f'A{i}'].value, ws1[f'B{i}'].value, ws1[f'C{i}'].value,
                   ws1[f'D{i}'].value, ws1[f'E{i}'].value,
                   ws1[f'F{i}'].value, ws1[f'G{i}'].value])

wb.save("Hvitevarer-uten-duplikat.xlsx")
