from flask import Flask, render_template, request
from Forms import CreateUserForm, loginform

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")


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
    return render_template("rentmovie.html", title="Rent Movie")

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
    return render_template("promotion.html", title="Promotions")

@app.route("/frozenpromo")
def frozenpromo():
    return render_template("promotionfrozendetails.html", title="Frozen Promo")

@app.route("/studentpromo")
def studentpromo():
    return render_template("promotionstudentdetails.html", title="Frozen Promo")

if __name__ == "__main__":
    app.run(debug=True)
