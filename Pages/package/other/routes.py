from flask import Blueprint
from flask import render_template, request, redirect, url_for, Markup
from flask_login import current_user, login_required
from package.other.forms import CreateContactUsForm
from package.utilis import check_admin, check_rights
from flask_login import login_required
import shelve
# from package.utilis import check_admin

main_blueprint = Blueprint("other", __name__)

@main_blueprint.route("/contactUs")
def contactUs():
    form = CreateContactUsForm()
    return render_template("User/contactUs.html", title="Contact Us", form=form)

# admin routes
@main_blueprint.route("/admin")
@main_blueprint.route("/admin/home")
@login_required
def admin_home():
    check_admin()
    first_rights = check_rights()
    if first_rights:
        if first_rights == "Manage admins":
            return redirect(url_for("user.admin_accounts"))
        if first_rights == "Carousel":
            return redirect(url_for("carousel.admin_carousel"))
        if first_rights == "Theatres":
            return redirect(url_for("movie_theatre.admin_movie_theatre"))
        if first_rights == "Movies":
            return redirect(url_for("movie.admin_movies"))
        if first_rights == "Rental":
            return redirect(url_for("rental.admin_rental"))
        if first_rights == "Showtime":
            return redirect(url_for("showtime.admin_showtime"))
        if first_rights == "Promotion":
            return redirect(url_for("promotion.admin_promotion"))
        
    db = shelve.open("shelve.db", "c")
    try:
        Promotion_dict = db["promotion"]
    except:        
        Promotion_dict = {}
        db["promotion"] = Promotion_dict 
    count_of_promotion = 0
    for key in Promotion_dict:
        count_of_promotion += 1
#For loop for rental data
    try:
        Rental_dict = db["rental"]
    except:        
        Rental_dict = {}
        db["rental"] = Rental_dict
    count_of_rental = 0
    for key in Rental_dict:
        count_of_rental += 1 

    try:
        Movies_dict = db["movies"]        
    except:
        Movies_dict = {}    
        db["movies"] = Movies_dict
    count_of_movie = 0
    for key in Movies_dict:
        count_of_movie += 1

    admin_dict = db["Users"]
    count_of_admin = 0
    for key in admin_dict:
        if key[0]== "A":
            count_of_admin += 1
        
    return render_template("Admin/index.html", title="Dashboard", count_of_promotion=count_of_promotion, count_of_rental=count_of_rental, count_of_movie=count_of_movie, count_of_admin=count_of_admin)

@main_blueprint.route("/admin/composeMail")
@login_required
def admin_composeMail():
    check_admin()
    return render_template("Admin/compose.html", title="Compose Mail") 

@main_blueprint.route("/admin/readMail")
@login_required
def admin_readMail():
    check_admin()
    return render_template("Admin/read-mail.html", title="Read Mail")

@main_blueprint.route("/admin/calendar")
@login_required
def admin_calendar():
    check_admin()
    return render_template("Admin/calendar.html", title="Calendar")

@main_blueprint.route("/admin/mailbox")
@login_required
def admin_mailbox():
    check_admin()
    return render_template("Admin/mailbox.html", title="Mailbox")
    
@main_blueprint.route("/legal")
def legal_page():
    return render_template("User 2/legal.html",title="Terms&Condition")

@main_blueprint.route("/aboutUs")
def aboutUs():
    return render_template("User 2/aboutUs.html",title="AboutUs")

@main_blueprint.route("/faq")
def faq():
    return render_template("User 2/faq.html", title="FAQ")

@main_blueprint.route("/pp")
def pp_page():
    return render_template("User 2/pp.html",title="Privacy Policy")