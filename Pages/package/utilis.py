from flask import redirect, url_for, render_template, abort
from flask_login import current_user

def check_admin():    
    if current_user.id[0] != "A":
        abort(401)

