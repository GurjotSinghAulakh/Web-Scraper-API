array = [1,2,4,5]

for i in range(20):
    kode = int(input())


    if kode in array:
        print("Duplicate sponsored ad")
        continue
    else:
        array.append(kode)

    print("Hvis contiune funker skal ikk denne meldingen skirves ut!")
