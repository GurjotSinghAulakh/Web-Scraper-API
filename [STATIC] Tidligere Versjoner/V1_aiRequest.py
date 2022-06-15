# VERSION 1

from datetime import datetime   # for å regne tiden til programmet
from tabulate import tabulate   # for å lage tabell i python
from bs4 import BeautifulSoup   # for å gjøre html-koden kompakt
import requests                 # for å gjøre request (html-request)

start_time = datetime.now()     # starter tid

category = input()                          # input link for which category to collect data from
html_text = requests.get(category).text     # extracting the html code from website
soup = BeautifulSoup(html_text, 'lxml')     # making the html-code compact

# start of the algorime:
all_ads_on_site = soup.find_all('article', class_="ads__unit")     # finding all ads in the category

table = [['TITLE', 'PRICE']]                # declaring a array which will be used to create a table

count = 0
for ad in all_ads_on_site:
    # extracting link for all the ads on the site
    product_link_code = ad.find('a', href=True)
    ad_link = product_link_code['href']

    # !! we have an error which we havent figured out a fix for just yet, where the first "ad_link" will not have
    # the full link, and wil only contain the words after "https://www.finn.no", so this is a temporary fix for that !!
    if count == 0:
        pass
        # ad_link = 'https://www.finn.no' + ad_link

    # now we are inside each individual ad, here we will collect data

    ad_html_code = requests.get(f'{ad_link}').text      # fetching the html code for each ad
    soup = BeautifulSoup(ad_html_code, 'lxml')          # making the html code compact

    # each ad inn "finn.no" has a section with class_name "panel u-mb16"
    sections = soup.find_all('section', class_="panel u-mb16")

    # collecting information by using class_names
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

print(count)
print(tabulate(table))
end_time = datetime.now()
print(end_time - start_time)





