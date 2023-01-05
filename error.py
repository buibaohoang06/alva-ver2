from flask import Blueprint, render_template

errorbp = Blueprint('errors', __name__, template_folder="templates", static_folder="static")

@errorbp.app_errorhandler(404)
def handle_404(err):
    return render_template('error.html'), 404
