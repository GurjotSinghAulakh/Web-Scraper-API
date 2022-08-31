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


def scrape_brand_from_ad_description(div_element, brand_array):
    # handling None-pointer exception
    if div_element is None:
        return "EMPTY"
    else:
        description_text = div_element.text
        description_text_array = description_text.split(" ")
        for word in description_text_array:
            if word.lower() in brand_array:
                return word.lower()
        return ""


def scrape_type_from_add_description(div_element, type_array):
    # handling None-pointer exception
    if div_element is None:
        return "EMPTY"
    else:
        description_text = div_element.text
        description_text_array = description_text.split(" ")
        for word in description_text_array:
            if word.lower() in type_array:
                return word.lower()
        return None




filename = "Hvitevarer.xlsx"
wb = Workbook()
wb.create_sheet("Hvitevarer")
ws = wb["Hvitevarer"]
ws.append(["Varenavn", "Kategori", "Under-Kategori", "Pris", "Merke", "Lokasjon", "Finn kode"])


# this function scrapes date from each under-category
# each under-category will run scrape function in their own thread
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
            print(f"[END_OF_ADS]: Total ads from category: {under_category_title} collected is {number_of_ads_scraped}")
            wb.save(filename)
            return


        for ad in all_ads_on_page:
            # ----------------Extracting: price, finncode, title, location, ad-link from articles page ----------------

            ad_price = ad.find("div", class_="ads__unit__img__ratio__price")
            ad_finncode = ad.find("a", class_="ads__unit__link").get('id')  # kan bruke href hvis det ikke funker
            ad_title = ad.find("a", class_="ads__unit__link").text  # kanksje jeg mpå bruke h2 elementet her??
            ad_location_div = ad.find("div", class_="ads__unit__content__details")
            ad_location = ad_location_div.findAll("div")[-1].text
            ad_link = ad.find("a", class_="ads__unit__link").get("href")

            # Sponsored ad will be ignored
            sponsored_ad = ad.find('span', class_="status status--sponsored u-mb8")
            if sponsored_ad is not None:
                continue

            # ------------------------------------ Entered ad ------------------------------------
            # checking if the ads exists
            try:
                ad_html_code = requests.get(f'{ad_link}').text  # fetching the html code for each ad
            except AttributeError as err:
                print(f"[Critical] : Error trying to access html text of ad {ad_link}: ", err)
            except:
                print(f"[Critical] : Unexpected error occurred when trying to access html text of ad {ad_link}:")

            soup = BeautifulSoup(ad_html_code, 'lxml')  # making the html code compact

            # ------------------------------------ ad_description & table ------------------------------------
            # finding additional data about the ad
            table_additional_info_html_code = soup.find('table', class_="u-width-auto u-mt16")
            ad_description = soup.find('div', class_="preserve-linebreaks")

            # finding product brand and type (under-under category)
            product_brand = ""
            product_type = ""
            found_brand = False
            found_type = False

            # 1. method: finding the brand and type for the product from the ad title:
            ad_title_split = ad_title.split(" ")
            for word in ad_title_split:
                if word.lower() in brand_array:
                    product_brand = word.lower()
                    found_brand = True

                if word.lower() in type_array:
                    product_type = word.lower()
                    found_type = True

            # 2. method: finding the brand and type for the product from the ad table:
            if found_brand is False or found_type is False:
                if table_additional_info_html_code is not None:
                    table_td = (table_additional_info_html_code.find_all('td', class_="u-pl16"))
                    for td in table_td:
                        if td.text.lower() in brand_array:
                            product_brand = td.text.lower()
                            found_brand = True

                        if td.text.lower() in type_array:
                            product_type = td.text.lower()
                            found_type = True

                    # 3. method: finding the brand and type for the product from description:
                    if found_brand is False:
                        if ad_description is not None:
                            product_brand = scrape_brand_from_ad_description(ad_description, brand_array)
                        else:
                            print(f"[Warning] : This ad does not have a description element: {ad_link}")

                    if found_type is False:
                        if ad_description is not None:
                            product_type = scrape_type_from_add_description(ad_description, type_array)

                        else:
                            print(f"[Warning] : This ad does not have a description element: {ad_link}")

                # If table is empty, we go straight to scrapping the description
                elif ad_description is not None:
                    product_type = scrape_type_from_add_description(ad_description, type_array)
                    product_brand = scrape_brand_from_ad_description(ad_description, brand_array)

                else:
                    print(f"[Warning] : This ad does not have a data table and description element: {ad_link}")

            # ------------------------------------ appending to sheet -----------------------------------
            # Scraping only "Til Salgs ads" from finn.no, by the help of front-end

            # handling None-pointer exception
            if ad_price is None:
                print("[INFO] : This ad does not have a price ", ad_link)

            # Otherwise, splitting the price "kr" and adding it to the sheet
            else:
                number_of_ads_scraped += 1
                price = ad_price.text.replace(" ", "").split("kr")[0]
                ws.append(
                    [ad_title, under_category_title, product_type, price, product_brand, ad_location,
                     ad_finncode])

        # Next-page
        print(f"Page {page_number} of category {under_category_title} is done")
        page_number += 1

        # Saving file for each page that is scraped
        wb.save(filename)

# Starting the algoritm (Scrapping)
start()
