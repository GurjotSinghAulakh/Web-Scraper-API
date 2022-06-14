import threading
import time
from datetime import datetime, date   # to measure the speed of the the algorithm
from threading import Timer

import requests  # to make request (html-request)
from bs4 import BeautifulSoup  # to make the html code compact
from openpyxl import Workbook  # To create excel sheets
wb = Workbook()
wb.create_sheet("Hvitevarer")
ws = wb["Hvitevarer"]
ws.append(["Varenavn", "Under kategori", "Kategori (type)", "Pris", "Merke", "Postnummer"])


def save(i):
    wb.save(f"{i}.xlsx")

threads = []

for i in range(4):
    t = threading.Thread(target=save, args=(1,))
    t.daemon = True
    threads.append(t)

for i in range(4):
    threads[i].start()
    time.sleep(2)

for i in range(4):
    threads[i].join()
