from openpyxl import Workbook, load_workbook  # To create excel sheets

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

for i in range(2, 9200):
    duplikat = False
    cell1 = f'A{i}'
    verdi1 = ws1[cell1].value

    pris_cell1 = f'D{i}'
    pris1 = ws1[pris_cell1].value

    for b in range(2, 9200):
        cell2 = f'A{b}'
        pris_cell2 = f'D{b}'

        verdi2 = ws2[cell2].value
        pris2 = ws2[pris_cell2].value

        if verdi1 == verdi2 and pris1 == pris2:
            duplikat = True
            break

    if duplikat is False:
        ws.append([ws1[f'A{i}'].value, ws1[f'B{i}'].value, ws1[f'C{i}'].value, ws1[f'D{i}'].value, ws1[f'E{i}'].value,
                   ws1[f'F{i}'].value, ws1[f'G{i}'].value])


wb.save("Hvitevarer-14Juni.xlsx")
