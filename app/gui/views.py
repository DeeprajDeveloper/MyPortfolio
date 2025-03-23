import os
from flask import Blueprint, jsonify, request, render_template
from app.gui import functionality as func

bp_gui = Blueprint('bp_gui', __name__, url_prefix='/gui', template_folder='templates', static_folder=os.path.join(os.path.dirname(__file__), 'static'), static_url_path='/bp_gui/static')


@bp_gui.route('/test', methods=['GET'])
def test():
    return render_template('test.html')
