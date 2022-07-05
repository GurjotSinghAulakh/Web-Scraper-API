to_ord = ["hei allesammen"]


tekststreng = "dette er en test, hei allesammen"

array = tekststreng.split(" ")

# for i in range(len(array)):
#     if i < len(array)-1:
#         sammen = array[i] + " " + array[i+1]
#         if sammen in to_ord:
#             print("YESSSS")


for word in array:
    word2 = word
