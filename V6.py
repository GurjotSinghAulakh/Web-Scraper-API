'''
    In this version we will try and seperate each uppercategory
    as fridges, sofas and such in their own excel files, as well
    in those excel files, seperate each model/brand in their own sheet
'''

import requests  # to make request (html-request)
from bs4 import BeautifulSoup  # to make the html code compact
from openpyxl import Workbook  # To create excel sheets
import threading

# TODO: legge til resten av data
# Creating brand arrays:
appliances_brand = ["bosch", "gram", "miele", "siemens", "candy", "samsung", "lg", "whirlpool", "aeg",
                    "husqvarna", "electrolux", "kenwood", "matsui", "scandomestic", "senz", "gorenje"]

under_categori = ["frysere", "innbyggingsovner", "kjøleskap", "komfyrer", "mikrobølgeovner", "oppvaskmaskiner",
                  "platetopper", "tørketromler", "vaskemaskiner", "ventilatorer"]

counties = ["agder", "innlandet", "møre og romsdal", "nordland", "oslo", "rogaland", "svalbard", "troms og finnmark",
            "trøndelag", "vestfold og telemark", "vestland", "viken"]

muncipality_agder = ["arendal", "birkenes", "bygland", "bykle", "evje og hornnes", "farsund", "flekkefjord", "froland",
                     "gjerstad", "grimstad", "hægebostad", "iveland", "kristiansand", "kvinesdal", "lillesand",
                     "lindesnes", "lyngdal", "risør", "sirdal", "tvedestrand", "valle", "vegårshei", "vennesla",
                     "åmli", "åseral"]

muncipality_innlandet = ["alvdal", "dovre", "eidskog", "elverum", "engerdal", "etnedal", "folldal", "gausdal",
                         "gjøvik", "gran", "grue", "hamar", "kongsvinger", "lesja", "lillehammer",
                         "lom", "løten", "nord-aurdal", "nord-fron", "nord-odal", "nodre land", "os (innlandet)",
                         "rendalen",
                         "ringebu", "ringsaker", "sel", "skjåk", "stange", "stor-elvdal", "søndre land", "sør-aurdal",
                         "sør-fron", "sør-odal", "tolga", "trysil", "tynset", "vang", "vestre slidre", "vestre toten",
                         "vågå", "våler (innlandet)", "åmot", "åsnes", "østre toten", "øyer", "øystre slidre"]

muncipality_more_og_romsdal = ["aukra", "aure", "averøy", "fjord", "giske", "gjemnes", "hareid", "herøy",
                               "hustadvika", "kristiansund", "molde", "rauma", "sande", "smøla", "stranda",
                               "sula", "sunndal", "surnadal", "sykkylven", "tingvoll", "ulstein", "vanylven", "vestnes",
                               "volda", "ålesund", "ørsta"]

muncipality_nordland = ["alstahaug", "andøy", "beiarn", "bindal", "bodø", "brønnøy", "bø", "dønna",
                        "evenes", "fauske", "glideskål", "grane", "hadsel", "hamarøy", "hattfjelldal",
                        "hemnes", "herøy", "leirfjord", "lurøy", "lødingen", "meløy", "moskenes", "narvik",
                        "nesna", "rana", "rødøy", "røst", "saltdal", "sortland", "steigen", "sømna", "sørfold", "træna",
                        "vefsn", "vega", "vestvågøy", "vevelstad", "vågan", "værøy", "øksnes"]

muncipality_oslo = ["oslo nord", "oslo sentrum", "oslo syd", "oslo vest", "oslo øst"]

muncipality_rogaland = ["bjerkreim", "bokn", "eigersund", "gjesdal", "haugesund", "hjelmeland", "hå", "karmøy",
                        "klepp", "kvitøy", "lund", "randaberg", "sandnes", "sauda", "sokndal",
                        "sola", "stavanger", "strand", "suldal", "time", "tysvær", "utsira", "vindafjord"]

muncipality_troms_og_finnmark = ["alta", "balsfjord", "bardu", "berlevåg", "båtsfjord", "dyrøy", "gamvik", "grantangen",
                                 "hammerfest", "harstad", "hasvik", "ibestad", "karasjok", "karlsøy", "kautokeino",
                                 "kvæfjord", "kvænangen", "kåfjord", "lavangen", "lebesby", "loppa", "lyngen",
                                 "målselv", "måsøy",
                                 "nesseby", "nordkapp", "nordreisa", "porsanger", "salangen", "senja", "skjervøy",
                                 "storfjord",
                                 "sør-varanger", "sørreisa", "tana", "tjeldsund", "tromsø", "vadsø", "vardø"]

muncipality_trondelag = ["flatanger", "frosta", "frøya", "grong", "heim", "hitra", "holtålen", "inderøy",
                         "indre fosen", "leka", "levanger", "lierne", "malvik", "melhus", "meråker",
                         "midtre gauldal", "namsos", "namsskogan", "nærøysund", "oppdal", "orkland", "osen",
                         "overhalla", "måsøy",
                         "rennebu", "rindal", "røros", "røyrvik", "selbu", "skaun", "snåsa", "steinkjer",
                         "stjørdal", "trondheim", "tydal", "verdal", "åfjord", "ørland"]

muncipality_vestfold_og_telemark = ["bamble", "drangedal", "fyresdal", "færder", "hjartdal", "holmestrand", "horten",
                                    "kragerø",
                                    "kviteseid", "larvik", "midt-telemark", "nissedal", "nome", "notodden", "porsgrunn",
                                    "sandefjord", "seljord", "siljan", "skien", "tinn", "tokke", "tønsberg", "vinje"]

muncipality_vestland = ["alver", "askvoll", "askøy", "aurland", "austevoll", "austrheim", "bergen", "bjørnafjorden",
                        "bremanger", "bømlo", "eidfjord", "etne", "fedje", "gloppen", "gulen",
                        "hyllestad", "høyanger", "kinn", "kvam", "kviinnherad", "luster", "lærdal", "masfjorden",
                        "modalen",
                        "osterøy", "samnanger", "sogndal", "solund", "stad", "stord", "stryn", "sunnfjord", "sveio",
                        "tysnes", "ullensvang", "ulvik", "vaksdal", "vik", "voss", "årdal", "øygarden"]

muncipality_viken = ["aremark", "asker", "aurskog-høland", "bærum", "drammen", "eidsvoll", "enebakk", "flesberg",
                     "flå", "fredrikstad", "frogn-drøbak", "gjerdrum", "gol", "halden", "hemsedal",
                     "hol", "hole", "hurdal", "hvaler", "indre østfold", "jevnaker", "kongsberg", "krødsherad", "lier",
                     "lillestrøm", "lunner", "lørenskog", "marker", "modum", "moss", "nannestad", "nes", "nesbyen",
                     "nesodden", "nittedal", "nordre follo", "nore og uvdal", "rakkestad", "ringerike", "rollag",
                     "råde", "rælingen", "sarpsborg", "sigdal", "skiptvet", "ullensaker", "vestby", "våler", "ål", "ås",
                     "øvre eiker"]

muncipality_dictionary = [
    {
        "county": "agder",
        "muncipalities": muncipality_agder
    },
    {
        "county": "innlandet",
        "muncipalities": muncipality_innlandet
    },
    {
        "county": "more og romsdal",
        "muncipalities": muncipality_more_og_romsdal
    },
    {
        "county": "nordland",
        "muncipalities": muncipality_nordland
    },
    {
        "county": "oslo",
        "muncipalities": muncipality_oslo
    },
    {
        "county": "rogaland",
        "muncipalities": muncipality_rogaland
    },
    {
        "county": "troms og finnmark",
        "muncipalities": muncipality_troms_og_finnmark
    },
    {
        "county": "trondelag",
        "muncipalities": muncipality_trondelag
    },
    {
        "county": "vestfold og telemark",
        "muncipalities": muncipality_vestfold_og_telemark
    },
    {
        "county": "vestland",
        "muncipalities": muncipality_vestland
    },
    {
        "county": "viken",
        "muncipalities": muncipality_viken
    },
]

# Dictonary containing information about each product we can scrape
# TODO : Add more products (objects)
appliances_dictionary = [
    {
        "category": "andre hvitevarer",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.305&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": under_categori
    },
    {
        "category": "frysere",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.72&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": ["fryseboks", "fryseskap", "fryser"]
    },
    {
        "category": "innbyggingsovner",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.74&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": ["stekeovn", "dampovn", "med platetopp"]  ## Sendere ta med platetopp, sjekk for mer data på finn
    },
    {
        "category": "kjøleskap",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&product_category=2.93.3907.292&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": ["kombiskap", "fryser", "side by side"]

    },
    {
        "category": "komfyrer",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.73&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": ["med keramisk", "gasskomfyr"]
    },
    {
        "category": "mikrobølgeovner",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.77&sort=PUBLISHED_DESC",
        "brand": appliances_brand
    },
    {
        "category": "oppvaskmaskiner",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.78&sort=PUBLISHED_DESC",
        "brand": appliances_brand
    },
    {
        "category": "platetopper",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.75&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": ["induksjon", "keramisk"]
    },
    {
        "category": "tørketromler",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.80&sort=PUBLISHED_DESC",
        "brand": appliances_brand
    },
    {
        "category": "vaskemaskiner",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.79&sort=PUBLISHED_DESC",
        "brand": appliances_brand,
        "type": ["tørketrommel"]
    },
    {
        "category": "ventilatorer",
        "link": "https://www.finn.no/bap/forsale/search.html?abTestKey=controlsuggestions&product_category=2.93.3907.76&sort=PUBLISHED_DESC",
        "brand": appliances_brand
    }
]


def ask():
    category_to_be_scraped = input("skriv inn kategori: ").lower()
    # TODO: after solving the problem for max ads to be scraped, we will add this functionality
    number_of_ads = input("Hvor mange annonser ønsker du å scarpe? ")

    for dictionary_element in appliances_dictionary:
        if category_to_be_scraped in dictionary_element["category"]:
            category = category_to_be_scraped
            link = dictionary_element["link"]
            brand = dictionary_element["brand"]
            type = dictionary_element["type"]

            test_threading = threading.Thread(target=scrape, args=(category, link, brand, type, number_of_ads))
            # scrape(category, link, brand, type, number_of_ads)
            test_threading.start()
            break


# common function
def start():
    print("Hey, Welcome to the scraper!")
    count = 0

    while True:
        if count == 0:
            ask()
            count += 1
        else:
            countinue_to_scrape = input("fortsette ? (y/n) ")
            if countinue_to_scrape.strip().lower() == "n":
                break
            ask()
            count += 1


# NB: we find and use the only first brand_name, in future maybe we scrape even more...
def scrape_brand_from_add_description(div_element, brand_array):
    if div_element is None:
        return "EMPTY"
    else:
        description_text = div_element.text
        description_text_array = description_text.split(" ")
        for word in description_text_array:
            if word.lower() in brand_array:
                return word.lower()
        return "Annet"


# NB: we find and use the only first type name, in future maybe we scrape even more...
def scrape_type_from_add_description(div_element, type_array):
    if div_element is None:
        return "EMPTY"
    else:
        description_text = div_element.text
        description_text_array = description_text.split(" ")
        for word in description_text_array:
            if word.lower() in type_array:
                return word.lower()
        return "Annet"


# def find_county(ad_postnr):
#     # for county in counties:
#     #     if ad_address == county:
#     #         return ad_address
#     #
#     # for dictionary_element in muncipality_dictionary:
#     #     for muncipality in dictionary_element["muncipalities"]:
#     #         if ad_address == muncipality:
#     #             return dictionary_element["county"]
#     #
#     # return None
#     ad_postnr = int(ad_postnr)
#
#     if ad_postnr >= 0o010 or ad_postnr <= 1295:
#         return "oslo"
#
#     elif 1311 <= ad_postnr <= 2093 or 2150 <= ad_postnr <= 2170 or 2720 <= ad_postnr <= 2743 or \
#             3004 <= ad_postnr <= 3648:
#         if ad_postnr == 3522 or ad_postnr == 3528:
#             return "innlandet"
#         return "viken"
#
#     elif 2100 <= ad_postnr <= 2134 or 2208 <= ad_postnr <= 2695 or 2750 <= ad_postnr <= 2985:
#          return "innlandet"
#
#     elif 3070 <= ad_postnr <= 3962:
#         if ad_postnr == 3522 or ad_postnr == 3528:
#             return "innlandet"
#         return "vestfold og telemark"
#
#     elif 4005 <= ad_postnr <= 4389 or 5514 <= ad_postnr <= 5549 or 5560 <= ad_postnr <= 5585:
#         return "rogaland"
#
#     elif 4400 <= ad_postnr <= 4994:
#         if ad_postnr == 4460 or ad_postnr == 4462 or ad_postnr == 4463:
#             return "rogaland"
#         return "agder"
#
#     elif 5003 <= ad_postnr <= 5499:
#         return "vestland"
#
#     elif 5550 <= ad_postnr <= 6996:
#         return "vestland"
#
#     elif ad_postnr >= 6002 or ad_postnr <= 6763:
#         if ad_postnr == 6657 or ad_postnr == 6658 or ad_postnr == 6680 or ad_postnr == 6683 or ad_postnr == 6686 \
#              or ad_postnr == 6687:
#             return "trøndelag"
#         return "møre og romsdal"
#
#     elif ad_postnr >= 7980 or ad_postnr <= 8985:
#         return "nordland"
#
#     elif 8409 <= ad_postnr <= 9990:
#         return "troms og finnmark"
#
#     elif ad_postnr >= 7010 and ad_postnr >= 7994:
#         return "trøndelag"

def scrape(category_title, category_link, brand_array, type_array, number_of_ads_to_scrap):
    # variables
    number_of_ads_scraped = 0
    number_of_ads_to_scrap = int(number_of_ads_to_scrap)

    # defining a work excel book
    wb = Workbook()

    wb.create_sheet("Hvitevarer")
    ws = wb["Hvitevarer"]
    ws.append(["Product title", "Product brand", "Under category", "Under-under category", "Price", "Post number", "Link"])

    # start of scraper algorithm
    page_number = 1

    while True:
        if number_of_ads_scraped >= number_of_ads_to_scrap:
            print(f"Total ads from category: {category_title} collected is {number_of_ads_scraped}")
            wb.save(category_title + ".xlsx")
            return

        page_link = category_link + "&page=" + str(page_number)

        page_html_code = requests.get(page_link).text  # extracting the html code from website
        soup = BeautifulSoup(page_html_code, 'lxml')  # making the html-code compact

        all_ads_on_site = soup.find_all('article', class_="ads__unit")  # finding all ads in the category

        for ad in all_ads_on_site:
            ad_link_code = ad.find('a', href=True)
            ad_link = ad_link_code['href']

            # checking if there are any sponsored ads on this category/site
            sponsored_ad = ad.find('span', class_="status status--sponsored u-mb8")
            if sponsored_ad is not None:
                ad_link = "https://www.finn.no" + ad_link

            ad_html_code = requests.get(f'{ad_link}').text  # fetching the html code for each ad
            soup = BeautifulSoup(ad_html_code, 'lxml')  # making the html code compact

            # each ad inn "finn.no" has a section with class_name "panel u-mb16"
            # section has information about ad-title, ad-payment-type and ad-price
            section = soup.find('section', class_="panel u-mb16")

            ad_title = (section.find('h1', class_="u-t2 u-mt16")).text
            ad_payment_type = (section.find('div', class_="u-t4")).text
            ad_price = section.find('div', class_="u-t1")

            # finding the location for the ads
            ad_location = soup.find('h3', class_="u-mb0")
            ad_postnr = ""

            if ad_location is None:
                pass
            else:
                ad_postnr = ad_location.text.split(" ")[0]
                ad_address = ad_location.text.split(" ")[1]

            # mal: https://www.finn.no/bap/forsale/ad.html?finnkode=258968174
            # finding additional data about the ad
            table_additional_info_html_code = soup.find('table', class_="u-width-auto u-mt16")
            ad_info_text_html_code = soup.find('div', class_="preserve-linebreaks")

            # TODO LIST:
            # must check if it is not empty

            # finding product brand and updating
            product_brand = ""
            product_type = ""
            found_brand = False
            found_type = False

            ad_title_split = ad_title.split(" ")
            for word in ad_title_split:
                if word.lower() in brand_array:
                    product_brand = word.lower()
                    found_brand = True

                if word.lower() in type_array:
                    product_type = word.lower()
                    found_type = True

            if found_brand is False or found_type is False:
                if table_additional_info_html_code is not None:
                    # table_th = (table_additional_info_html_code.find_all('th', class_="u-text-left u-no-break u-pa0"))
                    table_td = (table_additional_info_html_code.find_all('td', class_="u-pl16"))
                    for td in table_td:
                        if td.text.lower() in brand_array:
                            product_brand = td.text.lower()
                            found_brand = True

                        if td.text.lower() in type_array:
                            product_type = td.text.lower()
                            found_type = True

                    if found_brand is False:
                        product_brand = scrape_brand_from_add_description(ad_info_text_html_code, brand_array)
                    if found_type is False:
                        product_type = scrape_type_from_add_description(ad_info_text_html_code, type_array)
                else:
                    product_type = scrape_type_from_add_description(ad_info_text_html_code, type_array)
                    product_brand = scrape_brand_from_add_description(ad_info_text_html_code, brand_array)
            # -----------------------------------

            # Checking if ad_product has is "til salgs", "ønskes kjøpt" or "gis bort"
            # Just the products with a price will be added to the excel-sheet, the rest will be !!ignored!!,
            ## ?? shall we do this or just add them to a seperate sheet?

            if ad_payment_type.lower() == "til salgs":
                if ad_price is None:
                    # print("denne er none")
                    # print(ad_price)
                    # print(ad_link)
                    pass
                else:
                    # ad_county = find_county(ad_postnr)
                    price = ad_price.text.replace(" ", "").split("kr")[0]
                    ws.append([ad_title, product_brand, category_title, product_type, price, ad_postnr, ad_link])

                number_of_ads_scraped += 1

        # Next-page
        print(f"Page {page_number} of category {category_title} is done")
        page_number += 1


start()
