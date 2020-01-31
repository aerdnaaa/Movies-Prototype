import shelve

# db = shelve.open("shelve.db", "c")

# promotion_dict = db["promotion"]
# print(promotion_dict)

# for key, value in promotion_dict.items():
#     print(value.get_title())
#     print(value.get_promotion_image())
#     print(value.get_terms_and_conditions())
#     print(value.get_valid_period())
#     print()

# promotion_list = []
# promotion_sub_list = []
# index = 0
# main_index = 0
# list_of_promotion_classes = ["a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a"]
# for promotion_class in list_of_promotion_classes:
#     main_index += 1
#     if index <= 5:
#         promotion_sub_list.append(promotion_class)
#         if index == 5 or main_index == len(list_of_promotion_classes):
#             promotion_list.append(promotion_sub_list)
#         index += 1        
#         print(promotion_sub_list)
#     else:
#         promotion_sub_list = []
#         promotion_sub_list.append(promotion_class)
#         index = 1    

# print(promotion_list)
db = shelve.open("shelve.db", "c")
try:
    genre_list = db["genre_list"]
    if genre_list == []:
        genre_list = [("Action","Action"),("Adventure","Adventure"),("Comedy","Comedy"),("Drama","Drama"),("Fantasy","Fantasy"),("History","History"),("Horror","Horror"),("Music","Music"),("Mystery/Crime","Mystery/Crime"),("Romance","Romance"),("Sci-fi","Sci-fi")]
        db["genre_list"] = genre_list

except:
    genre_list = [("Action","Action"),("Adventure","Adventure"),("Comedy","Comedy"),("Drama","Drama"),("Fantasy","Fantasy"),("History","History"),("Horror","Horror"),("Music","Music"),("Mystery/Crime","Mystery/Crime"),("Romance","Romance"),("Sci-fi","Sci-fi")]
    db["genre_list"] = genre_list

