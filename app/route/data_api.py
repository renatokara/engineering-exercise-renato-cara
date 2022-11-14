from flask import jsonify, abort, request, Blueprint, current_app
from model.data import Data
import repository.DataRepository as data_repository
import service.DataService as data_service


ITEMS_API = Blueprint('data_api', __name__)


def get_blueprint():
    """Return the blueprint for the data api"""
    return ITEMS_API

@ITEMS_API.route('/data', methods=['GET'])
def get_data():
    """Return all data
    @return: 200: an array of all known items in database
    If there's nocontent the array is empty
    """
    return jsonify(data_repository.get_all_data())


@ITEMS_API.route('/data/<string:_id>', methods=['GET'])
def get_record_by_id(_id):
    """
        Get data by it's id
        @param _id: the id
        @return: 200: a Data as a flask/response object \
        with application/json mimetype.
        @raise 404: if Data request not found
    """
    if _id is None:
        abort(404)
    data = data_repository.get_data_by_id(int(_id))
    if data is None:
        return "Data not found for given Id", 404
    return jsonify(data), 200


@ITEMS_API.route('/data/filter', methods=['POST'])
def filter_data():
    """
        Filter a data request using
        {
            "title": "",
            "uri": "",
            "date_before": "",
            "date_after": "",

        }
        Any ofthe fields may be empty,if a field is empty 
        it is disconsidered in the filter.
        @return: 200: return flask/response object \
        with application/json mimetype.
        @raise 400: if error on request
    """
    if not request.get_json():
       return "Invalid JSON request", 400
    response = request.get_json(force=True)
    # Any ofthe fields may be empty 
    results = data_repository.get_data_by_filter(response.get('title'), response.get('uri'), data_service.parse_date(response.get('date_before')), data_service.parse_date(response.get('date_after')))
    return jsonify(results), 200



@ITEMS_API.route('/data', methods=['POST'])
def create_data():
    """
        Create a data 
        @param application/json baseon the Model  
            {
            "title": string,
            "uri": string,
            "date": datetime
            }
        @return: 201: created .
        @raise 400: misunderstood request
    """
    response = data_service.validate_errors_in_data_request(request)
    if isinstance(response, tuple):
        return response

    data=Data(url=response.get('uri'), title=response.get('title'), date_added=data_service.parse_date(response.get('date')))
    data_repository.insert_data(data)
    # HTTP 201 Created
    return jsonify({}), 201




@ITEMS_API.route('/data', methods=['PUT'])
def update_data():
    """
        Update a data 
        @param application/json in the structure described in class model.Data 
        @return: 200: with application/json mimetype.
        @raise 400: misunderstood request
    """
    response = data_service.validate_errors_in_data_request(request)
    if isinstance(response, tuple):
        return response

    data = Data(id=response.get('id'), url=response.get('uri'), title=response.get('title'), date_added=data_service.parse_date(response.get('date')))
    # HTTP 200 Updated
    data_repository.update_data(data)
    return get_record_by_id(data.id)




@ITEMS_API.route('/data/<string:_id>', methods=['DELETE'])
def delete_record(_id):
    """
        Delete a data request record
        @param id: the id
        @return: 204: an empty payload.
        @raise 404: if book request not found
    """
    if _id is None:
        abort(404)

    data_repository.delete_data(_id)
    return '', 204




@ITEMS_API.route('/data/import', methods=['POST'])
def import_data_from_data_json():
    """
        Import a data from data.json
        
        @return: 201: as a flask/response object \
        with application/json mimetype with errors and 
        the quantity created.
        @raise 400: misunderstood request
    """
    if not request.get_json():
        return "Invalid JSON request", 400
    data = request.get_json(force=True)
    items = data['items']
    errors = []
    count_created = 0
    for response in items:
        try :
            data=Data(url=response.get('uri'), title=response.get('title'), date_added=data_service.parse_date(response.get('date')))
            if data_service.validate(data):
                 data_repository.insert_data(data)
                 count_created += 1
        except data_service.ValidationError as e:
            errors.append(f"Data with Title '{response.get('title')}' URL '{response.get('uri')}' and date_added = {response.get('date')} has invalid format: {e}")
           
    # HTTP 201 Created
    return jsonify({"errors": errors, "created": count_created }), 201
