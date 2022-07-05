import threading                # to enable threading

import requests                 # to make request (html-request)
from bs4 import BeautifulSoup   # to make the html code compact
from openpyxl import Workbook, load_workbook  # to create excel sheets

from classes.Scrape import Scrape


class Hvitevarer(Scrape):
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
            "link": "https://www.finn.no/bap/forsale/search.html?product_category=2.93.3907.305&segment=1&sort=PUBLISHED_DESC",
            "brand": appliances_brand,
            "type": appliance_under_category
        },
        {
            "category": "frysere",
            "link": "https://www.finn.no/bap/forsale/search.html?product_category=2.93.3907.72&segment=1&sort=PUBLISHED_DESC",
            "brand": appliances_brand,
            "type": ["fryseboks", "fryseskap", "fryser"]
        },
        {
            "category": "innbyggingsovner",
            "link": "https://www.finn.no/bap/forsale/search.html?product_category=2.93.3907.74&segment=1&sort=PUBLISHED_DESC",
            "brand": appliances_brand,
            "type": ["stekeovn", "dampovn", "med platetopp"]  ## Sendere ta med platetopp, sjekk for mer data på finn
        },
        {
            "category": "kjøleskap",
            "link": "https://www.finn.no/bap/forsale/search.html?product_category=2.93.3907.292&segment=1&sort=PUBLISHED_DESC",
            "brand": appliances_brand,
            "type": ["kombiskap", "fryser", "side by side"]
        },
        {
            "category": "komfyrer",
            "link": "https://www.finn.no/bap/forsale/search.html?product_category=2.93.3907.73&segment=1&sort=PUBLISHED_DESC",
            "brand": appliances_brand,
            "type": ["med keramisk", "gasskomfyr"]
        },
        {
            "category": "mikrobølgeovner",
            "link": "https://www.finn.no/bap/forsale/search.html?product_category=2.93.3907.77&segment=1&sort=PUBLISHED_DESC",
            "brand": appliances_brand,
            "type": [None]
        },
        {
            "category": "oppvaskmaskiner",
            "link": "https://www.finn.no/bap/forsale/search.html?product_category=2.93.3907.78&segment=1&sort=PUBLISHED_DESC",
            "brand": appliances_brand,
            "type": [None]
        },
        {
            "category": "platetopper",
            "link": "https://www.finn.no/bap/forsale/search.html?product_category=2.93.3907.75&segment=1&sort=PUBLISHED_DESC",
            "brand": appliances_brand,
            "type": ["induksjon", "keramisk"]
        },
        {
            "category": "tørketromler",
            "link": "https://www.finn.no/bap/forsale/search.html?product_category=2.93.3907.80&segment=1&sort=PUBLISHED_DESC",
            "brand": appliances_brand,
            "type": [None]
        },
        {
            "category": "vaskemaskiner",
            "link": "https://www.finn.no/bap/forsale/search.html?product_category=2.93.3907.79&segment=1&sort=PUBLISHED_DESC",
            "brand": appliances_brand,
            "type": ["tørketrommel"]
        },
        {
            "category": "ventilatorer",
            "link": "https://www.finn.no/bap/forsale/search.html?product_category=2.93.3907.76&segment=1&sort=PUBLISHED_DESC",
            "brand": appliances_brand,
            "type": [None]
        }
    ]

    def scrape(under_category_object):
        under_category_title = under_category_object["category"]
        category_link = under_category_object["link"]
        brand_array = under_category_object["brand"]
        type_array = under_category_object["type"]

        global ad_finn_code_span, ad_html_code, ad_price, ad_location
        global page_html_code, ad_title, ad_payment_type

        number_of_ads_scraped = 0  # used to count number of ads scraped from a undercategory
        page_number = 1  # used for counting number of pages scraped and to move to next ad-page
        count_ad_has_no_price = 0  # used to track number of ads which is for sale but don't have a price,
        # these ads will not be added to the excel sheet

        while True:
            page_link = category_link + "&page=" + str(page_number)  # creating page link for each page
            page_html_code = requests.get(page_link).text  # extracting the html code from website
            soup = BeautifulSoup(page_html_code, 'lxml')  # making the html-code compact

            all_ads_on_page = soup.find_all('article', class_="ads__unit")  # finding all ads on the page

            # ------------------------------------ Save & exit ------------------------------------
            # Ending the script for "this" under-category, if there are no more ads to be scraped
            if len(all_ads_on_page) <= 1:
                print(
                    f"[END_OF_ADS]: Total ads from category: {under_category_title} collected is {number_of_ads_scraped}")
                print(
                    f"[Info] : Total ads that was for sale and had no price from under-category: {under_category_title} is {count_ad_has_no_price}")
                wb.save(filename)
                return

            # entring each ad...
            for ad in all_ads_on_page:
                ad_link_code = ad.find('a', href=True)  # extracting the ad_link_code
                ad_link = ad_link_code['href']  # extracting the ad_link

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
                    print("[Critical] : Unexpected error occurred in line 172")

                soup = BeautifulSoup(ad_html_code, 'lxml')  # making the html code compact

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
                        ad_price = section.find('div', class_="u-t1")
                    except AttributeError as err:
                        print("[Critical] : Error trying to access text element of section_element: ", err)
                    except:
                        print("[Critical] : Unexpected error occured in section element, line 188")
                else:
                    print(f"[Info] : This ad does not have a section element : {ad_link}")

                # ------------------------------------ ad_descrption & table ------------------------------------
                # finding brand and under-category form ad_description & table
                table_additional_info_html_code = soup.find('table', class_="u-width-auto u-mt16")
                ad_description_div_element = soup.find('div', class_="preserve-linebreaks")

                product_brand = ""
                product_type = ""
                product_color = ""
                found_brand = False
                found_type = False
                found_color = False

                # 1. method: finding the brand and under-category from the ad title:
                ad_title_split = ad_title.split(" ")
                for word in ad_title_split:
                    if word.lower() in brand_array:
                        product_brand = word.lower()
                        found_brand = True

                    if word.lower() in type_array:
                        product_type = word.lower()
                        found_type = True

                    # if word.lover() in color_array:
                    #     product_color = word.lower()
                    #     found_color = True

                # 2. method: finding the brand and type for the product from the ad table:
                if found_brand is False or found_type is False or found_color is False:
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
                                print(f"[Info] : This ad does not have a description element: {ad_link}")

                        if found_type is False:
                            if ad_description is not None:
                                product_type = scrape_type_from_ad_description(ad_description, type_array)
                            else:
                                print(f"[Info] : This ad does not have a description element: {ad_link}")

                    # If table is empty, we go straight to scrapping the description
                    if ad_description_div_element is not None:
                        if found_type is False:
                            product_type = scrape_type_from_ad_description(ad_description_div_element, sofa_brand)
                        if found_brand is False:
                            product_brand = scrape_brand_from_ad_description(ad_description_div_element, brand_array)
                        if found_color is False:
                            product_color = scrape_color_from_ad_description(ad_description_div_element, color_array)
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
                        [ad_title, under_category_title, product_type, price,
                         product_brand, product_color, ad_postnr, "", ad_finn_code])
                # ------------------------------------ Page n of undergategory x is done ----------------------------------

            # ------------------------------------ next page & save sheet ------------------------------------
            # next page
            print(f"Page {page_number} of category {under_category_title} is done")
            page_number += 1

            # Saving file for each page that is scraped
            wb.save(filename)

