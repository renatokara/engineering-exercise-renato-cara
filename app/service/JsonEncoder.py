
import json




class DataEncoder(json.JSONEncoder):
    """
        JSONencoder for encoding classes
    """
    def default(self, o):
       
        if hasattr(o, 'to_json'):
            return o.to_json()
        else:
            return super(DataEncoder, self).default(o)