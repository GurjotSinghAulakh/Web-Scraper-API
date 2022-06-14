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
# from datetime import datetime, timedelta
#
# n = 5
# current_time = datetime.now()
# future_time = current_time + timedelta(minutes=n)
#
# print(future_time)

# filename = "Hei"
# print("./Scrapped Data/" + filename)


# from datetime import datetime, timedelta
# from threading import Timer
#
# x = datetime.today()
# kl00 = x.replace(day=x.day, hour=0, minute=0, second=0, microsecond=0)
# y = kl00 + timedelta(days=1)
# delta_t = y - kl00
#
# secs = delta_t.total_seconds()
#
# print(secs)
#
# def hello_world():
#     print("hello world")
#     #...
#
# t = Timer(secs, hello_world)
# t.start()

# import logging
# logging.basicConfig(level=logging.INFO, filename='sample.log')
#
# def hypotenuse(a, b):
#     """Compute the hypotenuse"""
#     return (a**2 + b**2)**0.5
#
# kwargs = {'a':3, 'b':4, 'c':hypotenuse(3, 4)}
#
# logging.debug("a = {a}, b = {b}".format(**kwargs))
# logging.info("Hypotenuse of {a}, {b} is {c}".format(**kwargs))
# logging.warning("a={a} and b={b} are equal".format(**kwargs))
# logging.error("a={a} and b={b} cannot be negative".format(**kwargs))
# logging.critical("Hypotenuse of {a}, {b} is {c}".format(**kwargs))
#
# #> WARNING:root:a=3 and b=3 are equal
# #> ERROR:root:a=-1 and b=4 cannot be negative
# #> CRITICAL:root:Hypotenuse of a, b is 5.0


hei = "hei"
print(hei.split(" "))