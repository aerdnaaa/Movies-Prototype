from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from package.user.classes import Admin
import datetime, shelve

app = Flask(__name__)

app.config['SECRET_KEY'] = "73892748739"
app.config['REMEMBER_COOKIE_DURATION'] = datetime.timedelta(minutes=5)
app.config['UPLOADED_FILES_ALLOW'] = ["jpg", "jpeg", "png", "mov", "mp4"]

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

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

try:
    user_dict = db['Users']          
    if user_dict["A0"] == None:
        user_dict["A0"] = Admin("Super Admin", "superadmin@saw.com", ["Super Admin"], bcrypt.generate_password_hash("Admin").decode('utf-8') )            
except:        
    user_dict = {}
    user_dict["A0"] = Admin("Super Admin", "superadmin@saw.com", ["Super Admin"], bcrypt.generate_password_hash("Admin").decode('utf-8') )
    db["Users"] = user_dict    
print(user_dict)
db.close()

from package.showtime.routes import showtime_blueprint
from package.carousel.routes import carousel_blueprint
from package.movie.routes import movie_blueprint
from package.movie_theatre.routes import theatre_blueprint
from package.other.routes import main_blueprint
from package.promotion.routes import promotion_blueprint
from package.rental.routes import rental_blueprint
from package.user.routes import user_blueprint
from package.error.handlers import errors_blueprint

app.register_blueprint(showtime_blueprint)
app.register_blueprint(carousel_blueprint)
app.register_blueprint(movie_blueprint)
app.register_blueprint(theatre_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(promotion_blueprint)
app.register_blueprint(rental_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(errors_blueprint)
