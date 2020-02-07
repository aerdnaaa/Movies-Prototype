from flask import Blueprint, render_template

errors_blueprint = Blueprint('errors', __name__)

@errors_blueprint.app_errorhandler(404)
def error_404(error):
    return render_template('User 2/errors/404.html'), 404

@errors_blueprint.app_errorhandler(401)
def error_401(error):
    return render_template('User 2/errors/401.html'), 401

@errors_blueprint.app_errorhandler(500)
def error_500(error):
    return render_template('User 2/errors/500.html'), 500

@errors_blueprint.app_errorhandler(403)
def error_403(error):
    return render_template('User 2/errors/403.html'), 403