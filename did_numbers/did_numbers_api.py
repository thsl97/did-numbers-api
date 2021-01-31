from flask import Blueprint, request, jsonify

from did_numbers.database import db_session
from did_numbers.models import DIDNumber


bp = Blueprint('did-numbers', __name__, url_prefix='/did-numbers')


@bp.route('', methods=('GET',))
def get_did_numbers():
    """Gets a list of all did numbers, paginated by 25"""
    page = int(request.args.get('page', 1))
    # offsets the query by the page number and limit the results
    did_numbers = db_session.query(DIDNumber).offset((page - 1) * 25).limit(25)
    return jsonify({'data': [object.serialized for object in did_numbers]})
