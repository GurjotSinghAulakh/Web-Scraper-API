category_array = []


def printer(category):
    category_array.append(category)


while True:
    category_link = input("category link:")
    if category_link.lower() == "quit":
        break
    description = input("description: ")
    number_of_ads_to_scrap = input("number of ads: ")

    # making dictionary
    category = {"link": category_link, "description": description, "number": number_of_ads_to_scrap}

    printer(category)