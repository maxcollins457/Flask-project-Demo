from flask import Blueprint, render_template

extras_bp = Blueprint('extras', __name__)

@extras_bp.route('/extras')
def extras():
    return render_template('extras.html')