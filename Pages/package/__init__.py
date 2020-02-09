from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

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

from package.utilis import set_up_variables
set_up_variables()

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
