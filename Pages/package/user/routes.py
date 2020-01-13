from flask import Blueprint
from flask import render_template

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/login")
def login():
    # form = loginform()
    return render_template("User/login.html", title="Login Page",form=form)


@user_blueprint.route("/register")
def register():
    createUserForm = CreateUserForm(request.form)
    return render_template("User/register.html", title="Register",form=createUserForm)

@user_blueprint.route("/accountpage")
def accountpage():
    return render_template("User/accountpage.html", title="Account")
