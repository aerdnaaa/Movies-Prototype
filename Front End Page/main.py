from flask import Flask, render_template, request, Markup
# from Forms import CreateUserForm, loginform
from Promotion import Promotion

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    # carousel list will be created from Admin
    return render_template("home.html", title="Home", carousel_list=["carousel1.jpeg","carousel2.jpeg","carousel3.jpeg"])


# list of movies
@app.route("/movieslist")
def movieslist():
    return render_template("movieslist.html", title="Movies List")


@app.route("/frozenmoviedetails")
def frozenmoviedetails():
    return render_template("frozenmoviedetails.html", title="Frozen Movie Detail")

@app.route("/jokermoviedetails")
def jokermoviedetails():
    return render_template("jokermoviedetails.html", title="Joker Movie Detail")


@app.route("/bookmovie")
def bookmovie():
    return render_template("bookmovie.html", title="Book Movie")


@app.route("/bookmovieseats")
def bookmovieseats():
    return render_template("bookmovieseats.html", title="Buying Seats")


@app.route("/rentmovie")
def rentmovie():
    return render_template("rentmovie.html", title="Rent Movie", genreList = ["Action","Adventure","Comedy","Horror"], rentMovieList=[[]])

@app.route("/login")
def login():
    form = loginform()
    return render_template("login.html", title="Login Page",form=form)


@app.route("/register")
def register():
    createUserForm = CreateUserForm(request.form)
    return render_template("register.html", title="Register",form=createUserForm)


@app.route("/accountpage")
def accountpage():
    return render_template("accountpage.html", title="Account")


@app.route("/promotions")
def promotion():
    # promotion_list needs a list in a list. Outer list for rows, inner list for promotions in 1 row
    return render_template("promotion.html", title="Promotions", promotion_list=[{'frozen':'frozen.jpg', 'student':'student.jpg'}])

@app.route("/promotion/<name_of_promo>")
def promotionDetail(name_of_promo):
    frozenPromotion = Promotion("DISNEY'S FROZEN 2 POPCORN COMBO","promotion/frozen.jpg",Markup("""<em>Brrr... Are you ready for the magic of winter?</em><br><b>Follow Elsa and Anna into the unknown with your snowflake Crystal Dome Cups and Tin Tubs!</b>"""),['Not valid with other offers, privileges, promotions or voucher redemptions.','Not valid for group/corporate bookings.'])
    studentPromotion = Promotion("STUDENT PRIVILEGES","promotion/student.jpg",Markup("""<table class="table"><tbody><tr><td>$6</td><td>Tue, Thurs</td><td>At all SAW Theatre</td></tr><tr><td>$7</td><td>Mon, Wed, Fri</td><td>At all SAW Theatre</td></tr></tbody></table>"""),['Not valid with other offers, privileges, promotions or voucher redemptions.','Not valid for group/corporate bookings.'])
    dictionary_of_promos = {"frozen":frozenPromotion,"student":studentPromotion}
    promo = dictionary_of_promos[name_of_promo]
    return render_template("promotionDetail.html", promo=promo, title=name_of_promo.capitalize() + " Promo")

if __name__ == "__main__":
    app.run(debug=True)
