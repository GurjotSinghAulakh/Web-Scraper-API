adresse = "4319 Sandnes"
postnr = adresse.strip().split(" ")[-2]

print(postnr)

# by = adresse.split(",")[0].strip()
# print(by)
#
# postnr = by.split(" ")[-2]
# print(postnr)