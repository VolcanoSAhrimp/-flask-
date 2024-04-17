from flask import Blueprint, render_template

bp = Blueprint('simulation', __name__, url_prefix='/simulation')


@bp.route('/submit-book', methods=['GET'])
def submit_book():
    return render_template('simulation_add.html')
