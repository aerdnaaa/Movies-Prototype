from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from package.user.classes import Admin
import datetime, shelve, stripe

stripe_keys = {
    'secret_key': 'sk_test_V3wc5tAiP5Kyn0PY0JxUT3DM005oS3wpk9',
    'publishable_key': 'pk_test_vjq81FCmjJe9hSx1kWwAAv4T00k7I5HEag'
}

stripe.api_key = stripe_keys['secret_key']

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
try:
    seat_dict = db["Seats"]   
    if seat_dict == None:
        seat_dict = {'A1': 'standard_available', 'A2': 'standard_available', 'A3': 'standard_available', 'A4': 'standard_available', 'A5': 'standard_available', 'A6': 'standard_available', 'A7': 'standard_available', 'A8': 'standard_available', 
        'B1': 'standard_available', 'B2': 'standard_available', 'B3': 'standard_available', 'B4': 'standard_available', 'B5': 'standard_available', 'B6': 'standard_available', 'B7': 'standard_available', 'B8': 'standard_available', 
        'C1': 'standard_available', 'C2': 'standard_available', 'C3': 'standard_available', 'C4': 'standard_available', 'C5': 'standard_available', 'C6': 'standard_available', 'C7': 'standard_available', 'C8': 'standard_available', 
        'D1': 'standard_available', 'D2': 'standard_available', 'D3': 'standard_available', 'D4': 'standard_available', 'D5': 'standard_available', 'D6': 'standard_available', 'D7': 'standard_available', 'D8': 'standard_available', 
        'E1': 'standard_available', 'E2': 'standard_available', 'E3': 'standard_available', 'E4': 'standard_available', 'E5': 'standard_available', 'E6': 'standard_available', 'E7': 'standard_available', 'E8': 'standard_available'}
except:
    seat_dict = {}
    seat_dict = {'A1': 'standard_available', 'A2': 'standard_available', 'A3': 'standard_available', 'A4': 'standard_available', 'A5': 'standard_available', 'A6': 'standard_available', 'A7': 'standard_available', 'A8': 'standard_available', 
        'B1': 'standard_available', 'B2': 'standard_available', 'B3': 'standard_available', 'B4': 'standard_available', 'B5': 'standard_available', 'B6': 'standard_available', 'B7': 'standard_available', 'B8': 'standard_available', 
        'C1': 'standard_available', 'C2': 'standard_available', 'C3': 'standard_available', 'C4': 'standard_available', 'C5': 'standard_available', 'C6': 'standard_available', 'C7': 'standard_available', 'C8': 'standard_available', 
        'D1': 'standard_available', 'D2': 'standard_available', 'D3': 'standard_available', 'D4': 'standard_available', 'D5': 'standard_available', 'D6': 'standard_available', 'D7': 'standard_available', 'D8': 'standard_available', 
        'E1': 'standard_available', 'E2': 'standard_available', 'E3': 'standard_available', 'E4': 'standard_available', 'E5': 'standard_available', 'E6': 'standard_available', 'E7': 'standard_available', 'E8': 'standard_available'}
    db["Seats"] = seat_dict
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
