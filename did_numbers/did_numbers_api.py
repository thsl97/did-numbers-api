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
    return jsonify([object.serialized for object in did_numbers])



@bp.route('/new', methods=('POST',))
def create_did_number():
    """Creates new DID numbers"""
    data = request.get_json()
    # returns bad request if any DID number field is empty
    fields = ['value', 'monthlyPrice', 'setupPrice', 'currency']
    for field in fields:
        if field not in data:
            return jsonify(
                {'message': f'DID Number {field} must be informed'}
            ), 400
    try:
        new_number = DIDNumber(
            value=data['value'],
            monthly_price=data['monthlyPrice'] * 100,
            setup_price=data['setupPrice'] * 100,
            currency=data['currency']
        )
        db_session.add(new_number)
        db_session.commit()
        return jsonify({'data': new_number.serialized}), 201
    except AssertionError as e:
        return jsonify(str(e)), 400


@bp.route('/<int:id>/update', methods=('PATCH',))
def update_did_number(id):
    """Updates an existing did number"""
    did_number = db_session.query(DIDNumber).get(id)
    if did_number is None:
        return jsonify(
            {'message': 'The resource was not found on this server'}
        ), 404
    else:
        data = request.get_json()
        if 'value' in data:
            did_number.value = data['value']
        if 'monthlyPrice' in data:
            did_number.monthly_price = data['monthlyPrice'] * 100
        if 'setupPrice' in data:
            did_number.setup_price = data['setupPrice'] * 100
        if 'currency' in data:
            did_number.currency = data['currency']
        try:
            db_session.add(did_number)
            db_session.commit()
            return jsonify(did_number.serialized)
        except AssertionError as e:
            return jsonify(str(e)), 400


@bp.route('/<int:id>/delete', methods=('DELETE',))
def delete_did_number(id):
    """Deletes an did number"""
    did_number = db_session.query(DIDNumber).get(id)
    if did_number is None:
        return jsonify(
            {'message': 'The resource was not found on this server'}
        ), 404
    db_session.delete(did_number)
    db_session.commit()
    return jsonify(success=True)
