from flask import Blueprint

from did_numbers.database import db_session
from did_numbers.models import DIDNumber


bp = Blueprint('did-numbers', __name__, url_prefix='/did-numbers')


@bp.route('', methods=('GET',))
def get_did_numbers():
    """Gets a list of all did numbers"""
    did_numbers = db_session.query(DIDNumber).all()
    print(did_numbers)
