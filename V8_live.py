'''
    In this version we will scrape the category "Hvitevarer",
    and all its under categories, with threading enabled.
    They will all be saved on the file Hvitevarer.xlsx
'''

import threading  # enables threading, making the program run faster
from datetime import datetime  # to measure the speed of the the algorithme

import requests  # to make request (html-request)
from bs4 import BeautifulSoup  # to make the html code compact
from openpyxl import Workbook  # To create excel sheets

start_time = datetime.now()

# TODO: Add more categories, such as electronics

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
# as of now we have only implemented it for the appliance
appliances_dictionary = [
    {
        "category": "andre hvitevarer",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.305&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": appliance_under_category,
        "finnkode": []
    },
    {
        "category": "frysere",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.72&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": ["fryseboks", "fryseskap", "fryser"],
        "finnkode": []
    },
    {
        "category": "innbyggingsovner",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.74&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": ["stekeovn", "dampovn", "med platetopp"],  ## Sendere ta med platetopp, sjekk for mer data på finn
        "finnkode": []
    },
    {
        "category": "kjøleskap",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&product_category=2.93.3907.292&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": ["kombiskap", "fryser", "side by side"],
        "finnkode": []

    },
    {
        "category": "komfyrer",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.73&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": ["med keramisk", "gasskomfyr"],
        "finnkode": []
    },
    {
        "category": "mikrobølgeovner",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.77&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": [None],
        "finnkode": []
    },
    {
        "category": "oppvaskmaskiner",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.78&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": [None],
        "finnkode": []
    },
    {
        "category": "platetopper",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.75&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": ["induksjon", "keramisk"],
        "finnkode": []
    },
    {
        "category": "tørketromler",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.80&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": [None],
        "finnkode": []
    },
    {
        "category": "vaskemaskiner",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.79&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": ["tørketrommel"],
        "finnkode": []
    },
    {
        "category": "ventilatorer",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.76&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": [None],
        "finnkode": []
    }
]


def start():
    for dictionary_element in appliances_dictionary:
        thread = threading.Thread(target=scrape, args=(dictionary_element,))
        thread.start()
    print(f"All categories are running on each thread, total threads are {threading.active_count()}")


def scrape_brand_from_add_description(div_element, brand_array):
    # handling None-pointer exception
    if div_element is None:
        return "EMPTY"
    else:
        description_text = div_element.text
        description_text_array = description_text.split(" ")
        for word in description_text_array:
            if word.lower() in brand_array:
                return word.lower()
        return "Annet merke"


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


# This part of the code is hard coded for the category "hvitevarer"
# TODO: make this part of the code dynamic!
wb = Workbook()
wb.create_sheet("Hvitevarer")
ws = wb["Hvitevarer"]
ws.append(["Varenavn", "Under kategori", "Kategori (type)", "Pris", "Merke", "Postnummer"])

todays_date = "multisavetest.xlsx"

# this function scrapes date from each under-category
def scrape(under_category_object):
    under_category_title = under_category_object["category"]
    category_link = under_category_object["link"]
    finn_code_array = under_category_object["finnkode"]
    brand_array = under_category_object["brand"]
    type_array = under_category_object["type"]

    # defining a work excel book
    ws = wb["Hvitevarer"]


    while True:
        page_link = category_link + "&page=1"  # creating page link for each page
        page_html_code = requests.get(page_link).text  # extracting the html code from website
        soup = BeautifulSoup(page_html_code, 'lxml')  # making the html-code compact

        all_ads_on_site = soup.find_all('article', class_="ads__unit")  # finding all ads in the category

        # Ending the script for "this" undercategory, if there are no more ads to be scraped
        if len(all_ads_on_site) <= 1:
            # print(f"[END_OF_ADS]: Total ads from category: {under_category_title} collected is {number_of_ads_scraped}")
            # today = date.today()
            # todays_date = str(today) + ".xlsx"
            wb.save(todays_date)
            return

        # entring each ad...
        for ad in all_ads_on_site:
            ad_link_code = ad.find('a', href=True)  # fetching the ad_link
            ad_link = ad_link_code['href']  # fetching the ad_link

            # checking if there are any sponsored ads on this category/site
            sponsored_ad = ad.find('span', class_="status status--sponsored u-mb8")
            if sponsored_ad is not None:
                ad_link = "https://www.finn.no" + ad_link
                # if there are any duplicate, we will print them out to the terminal
                # and move on to the next ad
                if ad_link in finn_code_array:
                    print(f"Duplicate sponsored ad, from under-category {under_category_title} with link: {ad_link}")
                    continue
                else:
                    finn_code_array.append(ad_link)

            ad_html_code = requests.get(f'{ad_link}').text  # fetching the html code for each ad
            soup = BeautifulSoup(ad_html_code, 'lxml')  # making the html code compact

            # each ad inn "finn.no" has a section with class_name "panel u-mb16"
            # section has information about ad-title, ad-payment-type and ad-price
            section = soup.find('section', class_="panel u-mb16")

            # handling None-pointer exception
            if section is None:
                print(f"Denne annonsen har ikke section element : {ad_link}")

            ad_title = (section.find('h1', class_="u-t2 u-mt16")).text
            ad_payment_type = (section.find('div', class_="u-t4")).text
            ad_price = section.find('div', class_="u-t1")

            # finding the postnr for the ads
            ad_location_div = soup.find('div', class_="panel u-mt32")
            ad_location = ad_location_div.find('h3')

            # There are two types of address used in finn.no
            # 1. 0231 Oslo
            # 2. Gule gata 4, 3487 Kongsberg
            # We will handle both here, and extract the post number
            comma = ","
            if ad_location.text is not None and comma in ad_location.text:
                postnr_og_postadreese = ad_location.text.split(",")[-1]
                ad_postnr = postnr_og_postadreese.strip().split(" ")[0]
            else:
                ad_postnr = ad_location.text.strip().split(" ")[0]

            # finding additional data about the ad
            table_additional_info_html_code = soup.find('table', class_="u-width-auto u-mt16")
            ad_info_text_html_code = soup.find('div', class_="preserve-linebreaks")

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
                        product_brand = scrape_brand_from_add_description(ad_info_text_html_code, brand_array)
                    if found_type is False:
                        product_type = scrape_type_from_add_description(ad_info_text_html_code, type_array)
                else:
                    product_type = scrape_type_from_add_description(ad_info_text_html_code, type_array)
                    product_brand = scrape_brand_from_add_description(ad_info_text_html_code, brand_array)

            # Scraping only "Til Salgs ads" from finn.no
            if ad_payment_type.lower() == "til salgs":

                # handling None-pointer exception
                if ad_price is None:
                    pass

                # Otherwise, splitting the price "kr" and adding it to the sheet
                else:
                    price = ad_price.text.replace(" ", "").split("kr")[0]
                    ws.append([ad_title, under_category_title, product_type, price, product_brand, ad_postnr])

                # Counting number of ads scraped
                # number_of_ads_scraped += 1


# Starting the algoritm (Scrapping)
start()
