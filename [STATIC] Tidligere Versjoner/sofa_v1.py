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
sofa_brand = ["ikea", "møbleringen", "ekornes", "stordal", "bohus", "milano",
              "tiki"]

ikea_sofa_models = ["angby", "backamo", "ekeskog", "ektorp", "goteborg", "harnosand", "hovas", "karlanda", "karlstad",
                    "kivik", "kramfors", "lillberg", "nikkala", "sandby", "stockholm", "stromstad", "tomelilla",
                    "tylosand", "klobo", "gronlid", "farlov", "soderhamn", "norsborg", "friheten", "vimle"]

all_sofa_models = ["angby", "backamo", "ekeskog", "ektorp", "goteborg", "harnosand", "hovas", "karlanda", "karlstad",
                    "kivik", "kramfors", "lillberg", "nikkala", "sandby", "stockholm", "stromstad", "tomelilla",
                    "tylosand", "klobo", "gronlid", "farlov", "soderhamn","norsborg", "friheten", "vimle", "scandinavia",
                   "elton", "lomi", "paste", "north", "cloud", "sepia", "hannah", "madison", "grace", "fuuga",
                   "noora", "cosima", "casia", "cosy", "angel", "jerome", "mr. big", "aya", "orlando",
                   "recover", "orlando outdoor" ]

bolia_sofa_models = ["scandinavia", "elton", "lomi", "paste", "north", "cloud", "sepia", "hannah", "madison", "grace", "fuuga", "noora", "cosima", "casia", "cosy", "angel", "jerome", "mr. big", "aya", "orlando"
                     "recover", "orlando outdoor"]

sofa_brand_and_model = [{"brand": "ikea", "model": ikea_sofa_models},
                        {"brand": "bolia", "model": bolia_sofa_models},
                        {"brand": "ekornes", "model": [None]},
                        {"brand": "stordal", "model": [None]}]





# under categries
# sofa_under_categories = ["2-seter", "3-seter", "hjørnesofaer", "lenestoler", "puffer", "sofagrupper", "sovesofaer"]

# colors
sofa_colors = ["hvit", "grå", "svart", "brun", "turkis", "gul", "rød", "rosa", "grønn", "oransj"]

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
        "brand": sofa_brand,
        "type": [None]
    },
    {
        "category": "3-seter",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.205&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": sofa_brand,
        "type": [None]
    },
    {
        "category": "hjørnesofaer",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.207&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": sofa_brand,
        "type": [None]
    },
    {
        "category": "lenestoler",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.210&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": sofa_brand,
        "type": ["stressless"]
    },
    {
        "category": "puffer",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.209&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": sofa_brand,
        "type": [None]
    },
    {
        "category": "sofagrupper",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.208&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": sofa_brand,
        "type": [None]
    },
    {
        "category": "sovesofaer",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&for_rent=Kj%C3%B8p&product_category=2.78.7756.206&segment=1&sort=PUBLISHED_DESC&trade_type=1",
        "brand": sofa_brand,
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
ws.append(["Varenavn", "Kategori", "Pris", "Merke", "Modell", "Postnummer", "Lokasjon", "Finn kode"])

# Naming the output excel file:
filename = "../sofa-test04.07.xlsx"


# this function scrapes date from each under-category
# each under-category will run scrape function in their own thread
def scrape(under_category_object):
    under_category_title = under_category_object["category"]
    category_link = under_category_object["link"]
    # type_array = under_category_object["type"]

    global ad_finn_code_span, ad_html_code, ad_price, ad_location
    global page_html_code, ad_title, ad_payment_type

    number_of_ads_scraped = 0   # used to count number of ads scraped from an under-category
    page_number = 1             # used for counting number of pages scraped and to move to next ad-page
    count_ad_has_no_price = 0   # used to track number of ads which is for sale but don't have a price,
                                # these ads will not be added to the excel sheet

    while True:
        page_link = category_link + "&page=" + str(page_number)     # creating page link for each page
        page_html_code = requests.get(page_link).text               # extracting the html code from website
        soup = BeautifulSoup(page_html_code, 'lxml')                # making the html-code compact

        all_ads_on_page = soup.find_all('article', class_="ads__unit")  # finding all ads on the page

        # ------------------------------------ Save & exit ------------------------------------
        # Ending the script for "this" under-category, if there are no more ads to be scraped
        if len(all_ads_on_page) <= 1:
            print(f"[END_OF_ADS]: Total ads from category: {under_category_title} collected is {number_of_ads_scraped}")
            print(f"[Info] : Total ads that was for sale and had no price from under-category: {under_category_title} is {count_ad_has_no_price}")
            wb.save(filename)
            return

        # entring each ad...
        for ad in all_ads_on_page:
            ad_link_code = ad.find('a', href=True)      # extracting the ad_link_code
            ad_link = ad_link_code['href']              # extracting the ad_link

            # Checking for sponsored ad on the page, the sponsored ad will be ignored because,
            # the non-sponsored version of the ad will be scraped, so we avoid duplicate ads
            sponsored_ad = ad.find('span', class_="status status--sponsored u-mb8")
            if sponsored_ad is not None:
                continue

            # ------------------------------------ Entered ad ------------------------------------
            # trying to enter an ad/fetch data from an ad:
            try:
                ad_html_code = requests.get(f'{ad_link}').text  # fetching the html code for each ad
            except AttributeError as err:
                print("[Critical] : Error trying to access html text of ad (ad_html_code): ", err)
            except:
                print("[Critical] : Unexpected error occurred when trying to access html text of ad (ad_html_code):")

            soup = BeautifulSoup(ad_html_code, 'lxml')          # making the html code compact

            # ------------------------------------ Section element ------------------------------------
            # each ad inn "finn.no" has a section with class_name "panel u-mb16"
            # section has ad-title, ad-payment-type and ad-price
            section = soup.find('section', class_="panel u-mb16")

            # handling None-pointer exception
            if section is not None:
                # if the section element exist, extract as much info as possible
                try:
                    ad_title = (section.find('h1', class_="u-t2 u-mt16")).text
                    ad_payment_type = (section.find('div', class_="u-t4")).text
                    ad_price = section.find('div', class_="u-t1")  # sometimes ads don't have price, therefore no .text
                except AttributeError as err:
                    print("[Critical] : Error trying to access text element of section_element: ", err)
                except:
                    print("[Critical] : Unexpected error occured in section element, line 188")
            else:
                print(f"[Info] : This ad does not have a section element : {ad_link}")

            # ------------------------------------ ad_description  ------------------------------------
            # finding brand and under-category form ad_description
            table_additional_info_html_code = soup.find('table', class_="u-width-auto u-mt16")
            ad_description_div_element = soup.find('div', class_="preserve-linebreaks")

            product_brand = ""
            product_model = ""
            found_brand = False
            found_type = False
            found_model = False

            # 1. method: finding the brand and model from the ad title:
            ad_title_split = ad_title.split(" ")
            for word in ad_title_split:

                for sofa_element in sofa_brand_and_model:


                    # found the sofa brand
                    if sofa_element["brand"] == word.lower():
                        product_brand = word.lower()
                        found_brand = True

                        # searching for the model for that brand
                        for word_2 in ad_title_split:
                            if word_2 in sofa_element["model"]:
                                product_model = word_2
                                found_model = True
                                break


                    if word.lower() in sofa_element["model"]:
                        product_brand = sofa_element["brand"]
                        product_model = word
                        found_model = True
                        found_brand = True



            # 2. method: finding the brand and/or model from the ad_description:
            if found_brand is False or found_model is False:
                # if table_additional_info_html_code is not None:
                #     table_td = (table_additional_info_html_code.find_all('td', class_="u-pl16"))
                #     for td in table_td:
                #         if td.text.lower() in brand_array:
                #             product_brand = td.text.lower()
                #             found_brand = True
                #
                #         if td.text.lower() in type_array:
                #             product_type = td.text.lower()
                #             found_type = True
                #
                #     # 3. method: finding the brand and type for the product from description:
                #     if found_brand is False:
                #         if ad_description is not None:
                #             product_brand = scrape_brand_from_ad_description(ad_description, brand_array)
                #         else:
                #             print(f"[Info] : This ad does not have a description element: {ad_link}")
                #
                #     if found_type is False:
                #         if ad_description is not None:
                #             product_type = scrape_type_from_ad_description(ad_description, type_array)
                #         else:
                #             print(f"[Info] : This ad does not have a description element: {ad_link}")

                # If table is empty, we go straight to scrapping the description
                if ad_description_div_element is not None:
                    # if the product model or product brand is not found, we can use the div element to find it
                    if found_model is False:
                        # trying to find the model
                        product_model = scrape_from_ad_description(ad_description_div_element, all_sofa_models)

                        # if the model is found and the brand is not found, we can find the brand
                        # using the mode
                        if found_brand is False:
                            for sofa_element in sofa_brand_and_model:
                                if product_model in sofa_element["model"]:
                                    product_brand = sofa_element["brand"]
                    elif found_model is True and found_brand is False:
                        for sofa_element in sofa_brand_and_model:
                            if product_model in sofa_element["model"]:
                                product_brand = sofa_element["brand"]
                else:
                    print(f"[Info] : This ad does not have a table nor a description element: {ad_link}")

            # ------------------------------------ Location (post nr) ------------------------------------
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

            # ------------------------------------ Finn code ------------------------------------
            # extracting the finn code for each ad, it is located in a div with class = "panel u-text-left":
            ad_finn_div_table = soup.find('div', class_="panel u-text-left")

            if ad_finn_div_table is not None:
                ad_finn_code_span = ad_finn_div_table.find('span', class_="u-select-all")

            # ad_finn_code is "finnkode"
            ad_finn_code = ""

            if ad_finn_code_span is None:
                print(f"[Info] : This ad does not have finn code {ad_link}")
            else:
                try:
                    ad_finn_code = ad_finn_code_span.text
                except AttributeError as err:
                    print(f"[Critical] :  This ad {ad_link} has finn_code_span but no text element", err)
                except:
                    print(f"[Critical]: This ad {ad_link} has finn_code_span, but the program was not able to"
                          f" extract the finncode, because of an unexpected error! ")

            # ------------------------------------ appending to sheet ------------------------------------
            # Scraping only "Til Salgs" ads from private sellers, which have a price
            if ad_price is None:
                count_ad_has_no_price += 1
                # Otherwise, splitting the price "kr" and adding it to the sheet
            else:
                number_of_ads_scraped += 1
                price = ad_price.text.replace(" ", "").split("kr")[0]
                ws.append(
                    [ad_title, under_category_title, price,
                     product_brand, product_model, ad_postnr, "", ad_finn_code])
            # ------------------------------------ Page n of undergategory x is done ----------------------------------

        # ------------------------------------ next page & save sheet ------------------------------------
        # next page
        print(f"Page {page_number} of category {under_category_title} is done")
        page_number += 1

        # Saving file for each page that is scraped
        wb.save(filename)


# starting the algorithme
start()