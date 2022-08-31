'''
    [static] script will scrape category sofa
    and all its undecategories
'''

# todo: legge til flere farger, merker, evt under_under_kategorier "type" i dictionary

import threading                # to enable threading
from datetime import datetime   # to keep track of which day file was scraped

import requests                 # to make request (html-request)
from bs4 import BeautifulSoup   # to make the html code compact
from openpyxl import Workbook   # to create excel sheets

# brand array
all_sofa_brands = ["ikea", "møbelringen", "ekornes", "stordal", "bohus", "milano",
              "tiki"]

ikea_sofa_models = ["angby", "backamo", "ekeskog", "ektorp", "goteborg", "harnosand", "hovas", "karlanda", "karlstad",
                    "kivik", "kramfors", "lillberg", "nikkala", "sandby", "stockholm", "stromstad", "tomelilla",
                    "tylosand", "klobo", "gronlid", "farlov", "soderhamn", "norsborg", "friheten", "vimle", "strandmon",
                    "söderhamn"]

bolia_sofa_models = ["scandinavia", "elton", "lomi", "paste", "north", "cloud", "sepia", "hannah", "madison", "grace",
                     "fuuga", "noora", "cosima", "casia", "cosy", "angel", "jerome", "mr. big", "aya", "orlando",
                     "recover"]

all_sofa_models = ["angby", "backamo", "ekeskog", "ektorp", "goteborg", "harnosand", "hovas", "karlanda", "karlstad",
                    "kivik", "kramfors", "lillberg", "nikkala", "sandby", "stockholm", "stromstad", "tomelilla",
                    "tylosand", "klobo", "gronlid", "farlov", "soderhamn","norsborg", "friheten", "vimle", "scandinavia",
                    "elton", "lomi", "paste", "north", "cloud", "sepia", "hannah", "madison", "grace", "fuuga",
                    "noora", "cosima", "casia", "cosy", "angel", "jerome", "mr. big", "aya", "orlando",
                    "recover", "orlando outdoor", "strandmon", "söderhamn"]

sofa_brand_and_model = [{"brand": "ikea", "model": ikea_sofa_models},
                        {"brand": "bolia", "model": bolia_sofa_models},
                        {"brand": "ekornes", "model": [None]},
                        {"brand": "stordal", "model": [None]},
                        ]

# under categries
# sofa_under_categories = ["2-seter", "3-seter", "hjørnesofaer", "lenestoler", "puffer", "sofagrupper", "sovesofaer"]

# dictionary
sofa_dictionary = [
    # The links have filtes:
    # privat, til-salgs, kjøp
    # and are sorted by the most recent ad

    # type is used if an undercategory have also an undercategory
    # f.exp. undercategory: kjøleskap, has type: kombiskap, side-by-side and so on

    {
        "category": "2-seter",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.204&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": all_sofa_brands,
        "type": [None]
    },
    {
        "category": "3-seter",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.205&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": all_sofa_brands,
        "type": [None]
    },
    {
        "category": "hjørnesofaer",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.207&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": all_sofa_brands,
        "type": [None]
    },
    {
        "category": "lenestoler",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.210&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": all_sofa_brands,
        "type": ["stressless"]
    },
    {
        "category": "puffer",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.209&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": all_sofa_brands,
        "type": [None]
    },
    {
        "category": "sofagrupper",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.208&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": all_sofa_brands,
        "type": [None]
    },
    {
        "category": "sovesofaer",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.206&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": all_sofa_brands,
        "type": [None]
    },
]


# Start threads
def start():
    # Each under category will be scraped on its own thread
    for dictionary_element in sofa_dictionary:
        # args only accepts tuple element, therefore we have to include (,)
        thread = threading.Thread(target=scrape, args=(dictionary_element,))
        thread.start()
    print(f"All categories are running on each thread, total threads are {threading.active_count()}")


def scrape_from_ad_description(ad_description_div, array):
    # handling None-pointer exception
    if ad_description_div is None:
        print("[Warning]: ad_desciption div is empty")
        return
    else:
        description_text = ad_description_div.text
        description_text_array = description_text.split(" ")
        for word in description_text_array:
            if word.lower() in array:
                return word.lower()
        return


# Creating excel file
wb = Workbook()
# Creating work sheet
wb.create_sheet("Sofa")
# Selecting work sheet
ws = wb["Sofa"]
# Adding headers for the sheet "Sofa"
ws.append(["Varenavn", "Kategori", "Pris", "Merke", "Modell", "Lokasjon", "Finn kode"])

# Naming the output excel file:
filename = "sofa.xlsx"


# this function scrapes date from each under-category
# each under-category will run scrape function in their own thread
def scrape(under_category_object):
    global ad_html_code
    under_category_title = under_category_object["category"]
    category_link = under_category_object["link"]

    number_of_ads_scraped = 0   # used to count number of ads scraped from an under-category
    page_number = 1             # used for counting number of pages scraped and to move to next ad-page

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

            # Checking for sponsored ad on the page, the sponsored ad will be ignored because,
            # the non-sponsored version of the ad will be scraped, so we avoid duplicate ads
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


            # ------------------------------------ ad_description  ------------------------------------
            # finding brand and under-category form ad_description
            ad_description_div_element = soup.find('div', class_="preserve-linebreaks")

            product_brand = ""
            product_model = ""
            found_brand = False
            found_model = False

            # 1. method: finding the brand and model from the ad title:
            ad_title_split = ad_title.split(" ")
            for word in ad_title_split:
                for sofa in sofa_brand_and_model:
                # ===================== 1 =====================
                    # found the sofa brand
                    if sofa["brand"] == word.lower():
                        product_brand = word.lower()
                        found_brand = True

                        # searching for the model, for that brand
                        for word_2 in ad_title_split:
                            if word_2.lower() in sofa["model"]:
                                product_model = word_2
                                found_model = True
                                break

                # ===================== 2 =====================
                if found_model is False:
                    if word.lower() in all_sofa_models:
                        product_model = word.lower()
                        found_model = True

                        # ===================== 3 =====================
                        # using the model to find the brand
                        if found_brand is False:
                            for sofa in sofa_brand_and_model:
                                if product_model in sofa["model"]:
                                    product_brand = sofa["brand"]
                                    found_brand = True


            # 2. method: finding the brand and/or model from the ad_description:
            if found_brand is False or found_model is False:
                if ad_description_div_element is not None:
                    # if the product model or product brand is not found, we can use the div element to find it
                    if found_brand is False and found_model is False:
                        # ===================== 3 =====================
                        # we dont have the brand nor do we have the
                        product_brand = scrape_from_ad_description(ad_description_div_element, all_sofa_brands)
                        if product_brand is not None:
                            found_brand = True
                            for sofa in sofa_brand_and_model:
                                # found the sofa brand, now finding the model
                                if sofa["brand"] == product_brand:
                                    product_model = scrape_from_ad_description(ad_description_div_element, sofa["model"])
                                    if product_model is not None:
                                        found_model = True
                        else:
                            product_model = scrape_from_ad_description(ad_description_div_element, all_sofa_models)
                            if product_model is not None:
                                found_model = True
                                for sofa in sofa_brand_and_model:
                                    # found the sofa brand, now finding the model
                                    if product_model in sofa["model"]:
                                        product_brand = sofa["brand"]
                                        found_brand = True


                    elif found_brand is True and found_model is False:
                        # ===================== 2 =====================
                        product_model = scrape_from_ad_description(ad_description_div_element, all_sofa_models)
                        if product_model is not None:
                            found_model = True

                    else:
                        for sofa in sofa_brand_and_model:
                            # found the sofa brand, now finding the model
                            if product_model in sofa["model"]:
                                product_brand = sofa["brand"]
                                found_brand = True

                else:
                    print(f"[Info] : This ad does not have a table nor a description element: {ad_link}")


            # ------------------------------------ appending to sheet ------------------------------------
            # Scraping only "Til Salgs" ads from private sellers, which have a price
            if ad_price is None:
                print("[INFO] : This ad does not have a price ", ad_link)
                # Otherwise, splitting the price "kr" and adding it to the sheet
            else:
                number_of_ads_scraped += 1
                price = ad_price.text.replace(" ", "").split("kr")[0]
                ws.append(
                    [ad_title, under_category_title, price,
                     product_brand, product_model, ad_location, ad_finncode])
            # ------------------------------------ Page n of undergategory x is done ----------------------------------

        # ------------------------------------ next page & save sheet ------------------------------------
        # next page
        print(f"Page {page_number} of category {under_category_title} is done")
        page_number += 1

        # Saving file for each page that is scraped
        wb.save(filename)


# starting the algorithme
start()