from flask import Blueprint, jsonify

from did_numbers.database import db_session
from did_numbers.models import DIDNumber


bp = Blueprint('did-numbers', __name__, url_prefix='/did-numbers')


@bp.route('', methods=('GET',))
def get_did_numbers():
    """Gets a list of all did numbers"""
    did_numbers = db_session.query(DIDNumber).all()
    return jsonify({'data': [object.serialized for object in did_numbers]})
