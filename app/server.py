from flask import Flask, redirect, send_from_directory, make_response, jsonify
from route import data_api, data_static
from service.Database import DatabaseSingleton
from service.JsonEncoder import DataEncoder
import logging
import os 
log_filename = '/tmp/log/engineering-exercise.log'
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
logging.basicConfig(filename=log_filename, level=logging.INFO)
logger = logging.getLogger()

template_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__  ))))
template_dir = os.path.join(template_dir, 'app', 'static')
server = Flask(__name__, template_folder=template_dir)
logger.info(f'Using template_dir={template_dir}')


# creates and initializes the singleton that handles the database connection
databaseSingleton = DatabaseSingleton() 
databaseSingleton.create()

# Flask doesn't serialize classes, a custom encoder must be  provided 
server.json_encoder = DataEncoder

@server.route('/')
def home():
    return redirect("/items-list", code=302)


@server.route("/static/<path:path>")    
def send_static(path):
    return send_from_directory('static', path)

server.register_blueprint(data_api.get_blueprint())
server.register_blueprint(data_static.get_blueprint())


@server.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    logger.exception(_error)
    return make_response(jsonify({'error': 'Server error'}), 500)


if __name__ == "__main__":
    server.run(host='0.0.0.0', port=5000)