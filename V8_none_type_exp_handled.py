'''
    In this version we will scrape the category "Hvitevarer",
    and all its under categories, with threading enabled.
    They will all be saved on the file Hvitevarer.xlsx
'''

import threading                # enables threading, making the program run faster

import requests                 # to make request (html-request)
from bs4 import BeautifulSoup   # to make the html code compact
from openpyxl import Workbook   # To create excel sheets


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
    # Each under category gets it own thread
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


# This part of the code is "hardcoded" for the category "hvitevarer"
# TODO: make this part of the code dynamic

filename = "Hvitevarer.xlsx"
wb = Workbook()
wb.create_sheet("Hvitevarer")
ws = wb["Hvitevarer"]
ws.append(["Varenavn", "Under kategori", "Kategori (type)", "Pris", "Merke", "Postnummer"])

count_no_price = 0
count_no_to_sale = 0
count_to_sale = 0


# this function scrapes date from each under-category
def scrape(under_category_object):
    under_category_title = under_category_object["category"]
    category_link = under_category_object["link"]
    brand_array = under_category_object["brand"]
    type_array = under_category_object["type"]

    global ad_finn_code_span, ad_html_code, ad_price, ad_location
    global page_html_code, ad_title, ad_payment_type
    global count_no_price, count_no_to_sale, count_to_sale

    number_of_ads_scraped = 0

    # defining a work excel book
    ws = wb["Hvitevarer"]

    page_number = 1

    while True:
        # checking every page for each under-category to scrape data from
        page_link = category_link + "&page=" + str(page_number)  # creating page link for each page
        try:
            page_html_code = requests.get(page_link).text  # extracting the html code from website
        except IOError:
            print(f"Page 1 of {under_category_title} does not exist")

        soup = BeautifulSoup(page_html_code, 'lxml')  # making the html-code compact
        all_ads_on_site = soup.find_all('article', class_="ads__unit")  # finding all ads in the category

        # Ending the script for "this" undercategory, if there are no more ads to be scraped
        if len(all_ads_on_site) <= 1:
            print(f"[END_OF_ADS]: Total ads from category: {under_category_title} collected is {number_of_ads_scraped}")
            wb.save(filename)
            return


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
                print(f"Ad link does not exist {ad_link}")


            soup = BeautifulSoup(ad_html_code, 'lxml')  # making the html code compact

            # each ad inn "finn.no" has a section with class_name "panel u-mb16"
            # section has information about ad-title, ad-payment-type and ad-price
            section = soup.find('section', class_="panel u-mb16")

            # handling None-pointer exception
            if section is None:
                print(f"This ad does not have a section element : {ad_link}")
            else:
                try:
                    ad_title = (section.find('h1', class_="u-t2 u-mt16")).text
                    ad_payment_type = (section.find('div', class_="u-t4")).text
                    ad_price = section.find('div', class_="u-t1")
                except IOError:
                    print("Error trying to access text element of section_element")


            # finding the postnr for the ads
            ad_location_div = soup.find('div', class_="panel u-mt32")

            if ad_location_div is None:
                print(f"This ad does not have a location element : {ad_link}")
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
                            print(f"This ad does not have a description element: {ad_link}")

                    if found_type is False:
                        if ad_description is not None:
                            product_type = scrape_type_from_add_description(ad_description, type_array)

                        else:
                            print(f"This ad does not have a description element: {ad_link}")

                # If table is empty, we go straight to scrapping the description
                elif ad_description is not None :
                    product_type = scrape_type_from_add_description(ad_description, type_array)
                    product_brand = scrape_brand_from_ad_description(ad_description, brand_array)

                else:
                    print(f"This ad does not have a data table and description element: {ad_link}")

            # Scraping only "Til Salgs ads" from finn.no
            if ad_payment_type.lower() == "til salgs":
                # handling None-pointer exception
                if ad_price is None:
                    count_no_price += 1

                # Otherwise, splitting the price "kr" and adding it to the sheet
                else:
                    count_to_sale += 1
                    price = ad_price.text.replace(" ", "").split("kr")[0]
                    ws.append([ad_title, under_category_title, product_type, price, product_brand, ad_postnr])
            else:
                count_no_to_sale += 1


        # Next-page
        print(f"Page {page_number} of category {under_category_title} is done")
        page_number += 1

        wb.save("/Users/gurjotsinghaulakh/Library/CloudStorage/OneDrive-OsloMet/Jobb/Secundo/Web-Scraper-API-Github/Scrapped Data Static/" + filename)

# Starting the algoritm (Scrapping)
start()
