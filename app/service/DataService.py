
from flask import jsonify, abort, request
from model.data import Data
import re
import dateutil.parser

def validate_errors_in_data_request(request):
    """
        Validate data in the request
        Returns an tuple with the error or the object 
        if everything is valid 
    """
    if not request.get_json():
        return "Invalid JSON request", 400
    data = request.get_json(force=True)
    if not validate_uri(data.get('uri')):
        return ("Invalid  URI", 400)
    if not validate_title(data.get('title')):
        return ("Invalid  Title", 400)
    if not validate_date(data.get('date')):
        return ("Invalid  Date", 400)
    return data

class ValidationError(Exception):
    pass

def validate(data: Data):
    if not validate_uri(data.url):
        raise ValidationError('Invalid URI')
    if not validate_title(data.title):
        raise ValidationError('Invalid Title')
    return True

def validate_title(title): 
    return title is not None and len(title) > 0 and len(title) < 100

def validate_uri(uri): 
    return uri is not None and re.match(r"(http|https|file)://[a-zA-Z0-9\./\-]{1,255}", uri)

def validate_date(date): 
    try :
        return date is not None and len(date) and parse_date(date) is not None
    except dateutil.parser._parser.ParserError:
        return False



def parse_date(date_string):
    if date_string is None:
        return None
    return dateutil.parser.parse(date_string)