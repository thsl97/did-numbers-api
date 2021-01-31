import re

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


@bp.route('/new', methods=('POST',))
def create_did_number():
    """Creates new DID numbers"""
    data = request.get_json()
    # returns bad request if any DID number field is empty
    for field, value in data.items():
        if not value:
            return jsonify(
                {'message': f'DID Number {field} must be informed'}
            ), 400
    phone_pattern = re.compile(
        r'^\+(\d{2}) (\d{2}) (\d{5})-(\d{4})$'
    )
    if not phone_pattern.match(data['value']):
        return jsonify(
                {'message': 'DID Number value must be in correct format'}
            ), 400
    # checks if monthly and setup price are really numbers
    for field in ['monthlyPrice', 'setupPrice']:
        try:
            int(data[field] * 100)
        except ValueError:
            return jsonify(
                {'message': 'Incorrect format for {field}'}
            ), 400
    new_number = DIDNumber(
        value=data['value'],
        monthly_price=data['monthlyPrice'] * 100,
        setup_price=data['setupPrice'] * 100,
        currency=data['currency']
    )
    db_session.add(new_number)
    db_session.commit()
    return jsonify({'data': new_number.serialized}), 201


@bp.route('/<int:id>/update', methods=('PATCH',))
def update_did_number(id):
    did_number = db_session.query(DIDNumber).get(id)
    if did_number is None:
        return jsonify(
            {'message': 'The resource was not found on this server'}
        ), 404
    else:
        data = request.get_json()
        if 'value' in data:
            phone_pattern = re.compile(
                r'^\+(\d{2}) (\d{2}) (\d{5})-(\d{4})$'
            )
            if not phone_pattern.match(data['value']):
                return jsonify(
                        {'message': 'DID Number value must be in correct '
                                    'format'}
                    ), 400
            did_number.value = data['value']
        if 'monthlyPrice' in data:
            try:
                int(data['monthlyPrice'] * 100)
                did_number.monthly_price = data['monthlyPrice']
            except ValueError:
                return jsonify(
                    {'message': 'Incorrect format for monthlyPrice'}
                ), 400
        if 'setupPrice' in data:
            try:
                int(data['setupPrice'] * 100)
                did_number.setup_price = data['setupPrice']
            except ValueError:
                return jsonify(
                    {'message': 'Incorrect format for setupPrice'}
                ), 400
        if 'currency' in data:
            if not data['currency']:
                return jsonify(
                    {'message': 'Currency must not be empty'}
                ), 400
            did_number.currency = data['currency']
        db_session.add(did_number)
        db_session.commit()
        return jsonify({'data': did_number.serialized})
