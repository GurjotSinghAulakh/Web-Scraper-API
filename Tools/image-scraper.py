'''
    In this version we will scrape the category "Hvitevarer",
    and all its under categories, with threading enabled.
    They will all be saved on the file Hvitevarer.xlsx
'''
from datetime import datetime
import threading  # enables threading, making the program run faster

import requests  # to make request (html-request)
from bs4 import BeautifulSoup  # to make the html code compact
from openpyxl import Workbook  # To create excel sheets

# Creating brand arrays:
appliances_brand = ["samsung", "bosch", "miele", "whirlpool", "electrolux", "grundig", "siemens", "zanussi",
                    "bauknecht",
                    "upo", "point", "gram", "ikea", "lg", "gorenje", "candy", "aeg",
                    "husqvarna", "kenwood", "matsui", "scandomestic", "senz"]

# used for sorting the ads which does not have specified what under-category it belongs to
appliance_under_category = ["frysere", "innbyggingsovner", "kjøleskap", "komfyrer", "mikrobølgeovner",
                            "oppvaskmaskiner",
                            "platetopper", "tørketromler", "vaskemaskiner", "ventilatorer"]

# Dictionary contains information about each product we can scrape,
# links have the filters: "Til salgs", "Privat" and "Brukt" applied to them
appliances_dictionary = [
    {
        "category": "andre hvitevarer",
        "link": "https://www.finn.no/bap/forsale/search.html?condition=4&product_category=2.93.3907.305&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": appliances_brand,
        "type": appliance_under_category
    },
    {
        "category": "frysere",
        "link": "https://www.finn.no/bap/forsale/search.html?condition=4&product_category=2.93.3907.72&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": appliances_brand,
        "type": ["fryseboks", "fryseskap", "fryser"]
    },
    {
        "category": "innbyggingsovner",
        "link": "https://www.finn.no/bap/forsale/search.html?condition=4&product_category=2.93.3907.74&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": appliances_brand,
        "type": ["stekeovn", "dampovn", "med platetopp"]  ## Sendere ta med platetopp, sjekk for mer data på finn
    },
    {
        "category": "kjøleskap",
        "link": "https://www.finn.no/bap/forsale/search.html?condition=4&product_category=2.93.3907.292&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": appliances_brand,
        "type": ["kombiskap", "fryser", "side by side"]
    },
    {
        "category": "komfyrer",
        "link": "https://www.finn.no/bap/forsale/search.html?condition=4&product_category=2.93.3907.73&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": appliances_brand,
        "type": ["med keramisk", "gasskomfyr"]
    },
    {
        "category": "mikrobølgeovner",
        "link": "https://www.finn.no/bap/forsale/search.html?condition=4&product_category=2.93.3907.77&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": appliances_brand,
        "type": [None]
    },
    {
        "category": "oppvaskmaskiner",
        "link": "https://www.finn.no/bap/forsale/search.html?condition=4&product_category=2.93.3907.78&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": appliances_brand,
        "type": [None]
    },
    {
        "category": "platetopper",
        "link": "https://www.finn.no/bap/forsale/search.html?condition=4&product_category=2.93.3907.75&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": appliances_brand,
        "type": ["induksjon", "keramisk"]
    },
    {
        "category": "tørketromler",
        "link": "https://www.finn.no/bap/forsale/search.html?condition=4&product_category=2.93.3907.80&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": appliances_brand,
        "type": [None]
    },
    {
        "category": "vaskemaskiner",
        "link": "https://www.finn.no/bap/forsale/search.html?condition=4&product_category=2.93.3907.79&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": appliances_brand,
        "type": ["tørketrommel"]
    },
    {
        "category": "ventilatorer",
        "link": "https://www.finn.no/bap/forsale/search.html?condition=4&product_category=2.93.3907.76&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": appliances_brand,
        "type": [None]
    }
]


def start():
    # Each under category will be scraped on its own thread
    for dictionary_element in appliances_dictionary:
        # args only accepts tuple element, therefore we have to include (,)
        thread = threading.Thread(target=scrape, args=(dictionary_element,))
        thread.start()
    print(f"All categories are running on each thread, total threads are {threading.active_count()}")


def scrape(under_category_object):
    global ad_html_code

    under_category_title = under_category_object["category"]
    category_link = under_category_object["link"]
    brand_array = under_category_object["brand"]
    type_array = under_category_object["type"]


    number_of_ads_scraped = 0       # used to count number of ads scraped from an under-category
    page_number = 1                 # used for counting number of pages scraped and to move to next ad-page

    while True:
        page_link = category_link + "&page=" + str(page_number)     # creating page link for each page
        page_html_code = requests.get(page_link).text               # extracting the html code from website
        soup = BeautifulSoup(page_html_code, 'lxml')                # making the html-code compact

        all_ads_on_page = soup.find_all('article', class_="ads__unit")  # finding all ads on the page

        # ------------------------------------ Save & exit ------------------------------------
        # Ending the script for "this" under-category, if there are no more ads to be scraped
        if len(all_ads_on_page) <= 1:
            print("All images from all categories have been scraped, please check for bad/wrong images")
            return


        for ad in all_ads_on_page:
            # ----------------Extracting: price, finncode, title, location, ad-link from articles page ----------------
            ad_price = ad.find("div", class_="ads__unit__img__ratio__price")
            ad_finncode = ad.find("a", class_="ads__unit__link").get('id')  # kan bruke href hvis det ikke funker
            ad_title = ad.find("a", class_="ads__unit__link").text  # kanksje jeg mpå bruke h2 elementet her??
            ad_location_div = ad.find("div", class_="ads__unit__content__details")
            ad_location = ad_location_div.findAll("div")[-1].text
            ad_link = ad.find("a", class_="ads__unit__link").get("href")
            ad_image =

            # Sponsored ad will be ignored
            sponsored_ad = ad.find('span', class_="status status--sponsored u-mb8")
            if sponsored_ad is not None:
                continue



        # Next-page
        print(f"Page {page_number} of category {under_category_title} is done")
        page_number += 1


# Starting the algoritm (Scrapping)
start()
