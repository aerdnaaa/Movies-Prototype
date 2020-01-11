from flask import Blueprint
from flask import render_template

booking_blueprint = Blueprint("booking", __name__)

@booking_blueprint.route("/admin/booking")
def admin_booking():
    return render_template("Admin/booking.html", title="Booking")

@booking_blueprint.route("/bookmovie")
def bookmovie():
    return render_template("User/bookmovie.html", title="Book Movie")


@booking_blueprint.route("/bookmovieseats")
def bookmovieseats():
    return render_template("User/bookmovieseats.html", title="Buying Seats")