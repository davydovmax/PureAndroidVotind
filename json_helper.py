import json
import dateutil.parser


def json_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    if hasattr(obj, 'json_dict'):
        return obj.json_dict()
    # elif isinstance(obj, Query):

    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))


def get_date(isoformat_string):
    return dateutil.parser.parse(isoformat_string);


def json_encode_query(query):
    items = [json.dumps(item, default=json_handler) for item in query]
    return '[' +  ', '.join(items) + ']'


def json_encode(obj):
    """TODO:"""
    return json.dumps(obj, default=json_handler)
