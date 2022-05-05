from datetime import datetime
from tabulate import tabulate
from bs4 import BeautifulSoup
import requests

start_time = datetime.now()

html_text = requests.get('https://www.finn.no/bap/forsale/search.html?category=0.93&sort=RELEVANCE').text
soup = BeautifulSoup(html_text, 'lxml')

articles = soup.find_all('article', class_="ads__unit")

table = [['TITLE', 'PRICE']]

# vi gjør det litt redundant men fikser dette etterhvert
count = 0
for product in articles:
    product_link = product.find('a', href=True)
    link = product_link['href']

    if count == 0:
        link = 'https://www.finn.no' + link
    product_code = requests.get(f'{link}').text
    soup = BeautifulSoup(product_code, 'lxml')
    sections = soup.find_all('section', class_="panel u-mb16")

    for information in sections:
        titles = information.find('h1', class_="u-t2 u-mt16")
        prices_tilSalgs = information.find('div', class_="u-t1")
        payment_type = information.find('div', class_="u-t4").text

        final_product_price = 0

        if (payment_type != "Gis bort") & (payment_type != "Ønskes kjøpt"):
            if prices_tilSalgs is None:
                # print("Denne varen har ikke pris!")
                final_product_price = "Denne varen har ikke pris!"
            else:
                # print(prices_tilSalgs.text)
                final_product_price = prices_tilSalgs.text

        elif payment_type != "Ønskes kjøpt":
            # print("Ønskes kjøpt")
            final_product_price = "Ønskes kjøpt"

        else:
            # print("0 kr")
            final_product_price = "0 kr"

        table.append( [titles.text, final_product_price] )
    count = count+1

# print(count)
print(tabulate(table))
end_time = datetime.now()
print(end_time - start_time)





