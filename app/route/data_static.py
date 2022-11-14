from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint, render_template
REQUEST_API = Blueprint('data_static', __name__)


def get_blueprint():
    """
        Return the blueprint for the main app module
    """
    return REQUEST_API



@REQUEST_API.route('/items-list', methods=['GET'])
def get_items():
    """
        Return the html file that renders the records list
    """
    
    return render_template('data/views/items-list.html')

