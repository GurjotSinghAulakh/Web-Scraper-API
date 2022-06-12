# import threading
# from openpyxl import Workbook, load_workbook  # To create excel sheets
#
# wb = Workbook()
# wb.create_sheet("Hvitevarer")
# ws = wb["Hvitevarer"]
# ws.append(["Varenavn", "Under kategori", "Kategori (type)", "Pris", "Merke", "Postnummer"])
#
# def funk(data):
#     for i in range(6):
#         ws.append([data])
#         wb.save("test.xlsx")
#
#
# thread1 = threading.Thread(target=funk, args=("T1",))
# thread2 = threading.Thread(target=funk, args=("T2",))
# thread1.start()
# thread2.start()
#
# print("DONE")

# array = ["tang", "hsjdahs", "ooo"]
# array.insert(0, "hei")
# array.insert(0,"ahsjkdhakjsdhkjashdjkashkjhjdsa")
# while len(array) > 4:
#     array.pop()
#
# if "hei" in array:
#     print(array)
#     print("dublikat")
# from datetime import date
#
# today = date.today()
# name = str(today) + ".xlsx"
# file_name = name
#
# print(file_name)
from datetime import datetime, timedelta

n = 5
current_time = datetime.now()
future_time = current_time + timedelta(minutes=n)

print(future_time)