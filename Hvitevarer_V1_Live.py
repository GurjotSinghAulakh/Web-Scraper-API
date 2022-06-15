'''
    In this version we will scrape the category "Hvitevarer",
    and all its under categories, with threading enabled.
    They will all be saved on the file (CurrentDate).xlsx
    It will run live, and save both a backup file and a
    big file where huge data will sit
'''

import threading
import time
from datetime import datetime, date   # to measure the speed of the the algorithm
from threading import Timer

import logging
logging.basicConfig(level=logging.INFO, filename='backuplog.log')

import requests  # to make request (html-request)
from bs4 import BeautifulSoup  # to make the html code compact
from openpyxl import Workbook  # To create excel sheets

start_time = datetime.now()

# TODO: Add more categories, such as electronics

# Creating brand arrays:
appliances_brand = ["samsung", "bosch", "miele", "whirlpool", "electrolux", "grundig", "siemens", "zanussi",
                    "bauknecht", "upo", "point", "gram", "ikea", "lg", "gorenje", "candy", "aeg", "husqvarna",
                    "kenwood", "matsui", "scandomestic", "senz"]

# used for sorting the ads which does not have specified what under-category it belongs to
appliance_under_category = ["frysere", "innbyggingsovner", "kjøleskap", "komfyrer", "mikrobølgeovner",
                            "oppvaskmaskiner", "platetopper", "tørketromler", "vaskemaskiner", "ventilatorer"]

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

all_finn_code_array = []

count_no_price = 0
count_no_to_sale = 0
count_to_sale = 0


def start():
    # Threads: creating the backup file
    save_file_thread = threading.Thread(backup_file())
    save_file_thread.start()

    # Threads: creating the data file
    save_file_thread = threading.Thread(time_to_save_file())
    save_file_thread.start()

    round_counter = 1

    while True:
        for dictionary_element in appliances_dictionary:
            scrape(dictionary_element, all_finn_code_array)
            time.sleep(3)

        # Round counter
        logging.info(f"Round {round_counter} is finished")

        # Counter : Products for sale
        logging.info(f"[COUNTER]: Products for sale: {count_to_sale}")

        # Counter : Products for sale with no price
        logging.info(f"[COUNTER]: Products for sale with no price: {count_no_price}")

        # Counter : Products not for sale
        logging.info(f"[COUNTER]: Products not for sale (gis bort/ønskes kjøpt):  {count_to_sale}")
        round_counter += 1


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
ws.append(["Varenavn", "Under kategori", "Kategori (type)", "Pris", "Merke", "Postnummer", "Lokasjon", "Finn Kode"])


# Time function: that will start a thread every day at 00:00 at midnight
def time_to_save_file():
    # 24-hours : (seconds: 86_400, function)
    twentyfour_hours = Timer(3600, save_file_everyday)
    twentyfour_hours.start()


# Time function: that will start a thread every 2nd hour
def backup_file():
    # 2-hours : (seconds: 7200, function)
    two_hours = Timer(1800, save_every_two_hours)
    two_hours.start()


# A function that will save a excel file with scrapped data, at 00:00 O´olock
def save_file_everyday():
    today = date.today()
    name = str(today) + ".xlsx"
    file_name = name

    # TODO: We have to change "Absolutt Path", before we will run the algorithm

    wb.save("./[LIVE] Scrapped Data/" + file_name)

    print("hello world")
    time_to_save_file()


# A function that will save a excel file with scrapped data, every 2nd hour
def save_every_two_hours():
    today = date.today()
    name = "backup_" + str(today) + ".xlsx"
    file_name = name

    # TODO: We have to change "Absolutt Path", before we will run the algorithm

    wb.save("./[LIVE] Backup data/" + file_name)

    print("Bye world")
    backup_file()

# this function scrapes date from each under-category
def scrape(under_category_object, all_finn_code_array):
    under_category_title = under_category_object["category"]
    category_link = under_category_object["link"]
    brand_array = under_category_object["brand"]
    type_array = under_category_object["type"]

    global count_no_to_sale, ad_finn_code_span, ad_html_code, page_html_code, ad_title, ad_payment_type, ad_price, ad_location
    global count_to_sale
    global count_no_price
    counter_old_ad = 1

    print(f"[LIVE]: Now scraping {under_category_title}")

    # defining a work excel book
    ws = wb["Hvitevarer"]

    page_link = category_link + "&page=1"  # creating page link for each page
    try:
        page_html_code = requests.get(page_link).text  # extracting the html code from website
    except IOError:
        logging.critical(f"Page 1 of {under_category_title} does not exist")

    soup = BeautifulSoup(page_html_code, 'lxml')  # making the html-code compact
    all_ads_on_site = soup.find_all('article', class_="ads__unit")  # finding all ads in the category

    # entring each ad...
    for ad in all_ads_on_site:
        ad_link_code = ad.find('a', href=True)  # fetching the ad_link
        ad_link = ad_link_code['href']  # fetching the ad_link

        # checking if there are any sponsored ads on this category/site
        sponsored_ad = ad.find('span', class_="status status--sponsored u-mb8")
        if sponsored_ad is not None:
            ad_link = "https://www.finn.no" + ad_link

        try:
            ad_html_code = requests.get(f'{ad_link}').text  # fetching the html code for each ad
        except IOError:
            logging.critical(f"Ad link does not exist {ad_link}")

        soup = BeautifulSoup(ad_html_code, 'lxml')  # making the html code compact

        # extracting the finn code for each ad:
        try:
            ad_finn_div_table = soup.find('div', class_="panel u-text-left")
            if ad_finn_div_table is not None:
                ad_finn_code_span = ad_finn_div_table.find('span', class_="u-select-all")
        except IOError:
            logging.critical(f"Div table for ad: {ad_link} does not exist")

        # ad_finn_code is "finnkode"
        ad_finn_code = ""

        if ad_finn_code_span is None:
            logging.info(f"This ad does not have finn code {ad_link}")
        else:
            try:
                ad_finn_code = ad_finn_code_span.text
            except IOError:
                logging.warning(f"This ad {ad_link} has finn_code_span but no text element")

        # TODO: Go to next undercat. if there are no new ads 3x
        # checking for duplicate:
        if ad_finn_code in all_finn_code_array:
            logging.info(f"[SKIP]: no new ad in category {under_category_title}")
            if counter_old_ad == 5:
                print("Vi har sett at vi har fått 5 gamle reklamer på rad!")
                break
            counter_old_ad += 1
            continue
        else:
            all_finn_code_array.insert(0, ad_finn_code)
            logging.info(f"[NEW] : New ad is found... {ad_finn_code}, {ad_link}")
            while len(all_finn_code_array) > 600:
                all_finn_code_array.pop()

        # each ad inn "finn.no" has a section with class_name "panel u-mb16"
        # section has information about ad-title, ad-payment-type and ad-price
        section = soup.find('section', class_="panel u-mb16")

        # handling None-pointer exception
        if section is None:
            logging.warning(f"This ad does not have a section element : {ad_link}")
        else:
            try:
                ad_title = (section.find('h1', class_="u-t2 u-mt16")).text
                ad_payment_type = (section.find('div', class_="u-t4")).text
                ad_price = section.find('div', class_="u-t1")
            except IOError:
                logging.critical("Error trying to access text element of section_element")


        # finding the postnr for the ads
        ad_location_div = soup.find('div', class_="panel u-mt32")

        if ad_location_div is None:
            logging.warning(f"This ad does not have a location element : {ad_link}")
        else:
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
        ad_description = soup.find('div', class_="preserve-linebreaks")

        #---------------------------------------------- Mangler try/except ----------------------------------------#
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
                        product_brand = scrape_brand_from_add_description(ad_description, brand_array)

                    else:
                        logging.warning(f"This ad does not have a description element: {ad_link}")

                if found_type is False:
                    if ad_description is not None:
                        product_type = scrape_type_from_add_description(ad_description, type_array)

                    else:
                        logging.warning(f"This ad does not have a description element: {ad_link}")

            # If table is empty, we go straight to scrapping the description
            elif ad_description is not None :
                product_type = scrape_type_from_add_description(ad_description, type_array)
                product_brand = scrape_brand_from_add_description(ad_description, brand_array)

            else:
                logging.critical(f"This ad does not have a data table and description element: {ad_link}")

        # Scraping only "Til Salgs ads" from finn.no
        if ad_payment_type.lower() == "til salgs":
            # handling None-pointer exception
            if ad_price is None:
                count_no_price += 1
                pass

            # Otherwise, splitting the price "kr" and adding it to the sheet
            else:
                count_to_sale += 1
                price = ad_price.text.replace(" ", "").split("kr")[0]
                ws.append([ad_title, under_category_title, product_type, price, product_brand, ad_postnr,"", ad_finn_code])
        else:
            count_no_to_sale += 1


# Starting the algorithm (Scrapping)
start()
