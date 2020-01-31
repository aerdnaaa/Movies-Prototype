from flask import Blueprint
from flask import render_template, request, redirect, url_for, Markup
from package.other.forms import CreateContactUsForm
from flask_login import login_required
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
    
    return render_template("Admin/index.html", title="Dashboard")

@main_blueprint.route("/admin/composeMail")
def admin_composeMail():
    return render_template("Admin/compose.html", title="Compose Mail") 

@main_blueprint.route("/admin/readMail")
def admin_readMail():
    return render_template("Admin/read-mail.html", title="Read Mail")

@main_blueprint.route("/admin/calendar")
def admin_calendar():
    return render_template("Admin/calendar.html", title="Calendar")

@main_blueprint.route("/admin/mailbox")
def admin_mailbox():
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