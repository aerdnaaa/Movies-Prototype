from flask import redirect, url_for, render_template, abort, request
from flask_login import current_user

def check_admin():
    print(f"{current_user.get_id()} tried to access admin pages")
    if current_user.get_id()[0] != "A":
        abort(401)

def check_if_login():
    if current_user.is_authenticated:
        abort(403)
