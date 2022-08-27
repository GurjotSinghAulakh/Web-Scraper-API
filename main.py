ikea_sofa_models = ["hei", "hade"]
bolia_sofa_models = ["ok", "suii"]
dict = [{"brand": "ikea", "model": ikea_sofa_models},
        {"brand": "bolia", "model": bolia_sofa_models}]


for sofa in dict:
    if "hei" in sofa["model"]:
        print(sofa["model"])