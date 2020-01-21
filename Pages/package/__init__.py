from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = "73892748739"

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from package.showtime.routes import showtime_blueprint
from package.carousel.routes import carousel_blueprint
from package.movie.routes import movie_blueprint
from package.movie_theatre.routes import theatre_blueprint
from package.other.routes import main_blueprint
from package.promotion.routes import promotion_blueprint
from package.rental.routes import rental_blueprint
from package.user.routes import user_blueprint

app.register_blueprint(showtime_blueprint)
app.register_blueprint(carousel_blueprint)
app.register_blueprint(movie_blueprint)
app.register_blueprint(theatre_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(promotion_blueprint)
app.register_blueprint(rental_blueprint)
app.register_blueprint(user_blueprint)