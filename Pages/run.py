from package import app
import shelve

if __name__ == "__main__":
    app.run(debug=True)

db = shelve.open("shelve.db", "c")
# creating admin account / ensuring a super admin account exists

# creating genre list
try:
    genre_list = db["genre_list"]
    if genre_list == []:
        genre_list = [("Action","Action"),("Adventure","Adventure"),("Comedy","Comedy"),("Drama","Drama"),("Fantasy","Fantasy"),("History","History"),("Horror","Horror"),("Music","Music"),("Mystery/Crime","Mystery/Crime"),("Romance","Romance"),("Sci-fi","Sci-fi")]
        db["genre_list"] = genre_list

except:
    genre_list = [("Action","Action"),("Adventure","Adventure"),("Comedy","Comedy"),("Drama","Drama"),("Fantasy","Fantasy"),("History","History"),("Horror","Horror"),("Music","Music"),("Mystery/Crime","Mystery/Crime"),("Romance","Romance"),("Sci-fi","Sci-fi")]
    db["genre_list"] = genre_list

