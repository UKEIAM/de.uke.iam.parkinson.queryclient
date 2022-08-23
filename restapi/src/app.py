from flask import Flask, request, jsonify, make_response, Response
import databaseHandler, jsonHandler
from flask_cors import CORS, cross_origin
app = Flask('QueryClient_RESTAPI')
cors = CORS(app)
app.json.sort_keys = False
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return "<h1>Query Client</h1>" \
           "<p>This REST-API can be used to send print jobs, retrieve all open jobs and mark print jobs as processed</p>"

@app.route('/incoming', methods=['GET'])
@cross_origin()
def homeIncoming():
    return 'Incoming Jobs\nHere you can send print jobs</p>\n'

@app.route('/incoming', methods=['POST'])
@cross_origin()
def insert_record():
    response_dict = {'message':'The print job was successfully stored', 'status':'200'}
    if not request.is_json:
        response_dict['message'] = "You have to provide a JSON"
        response_dict['status'] = '401'
        return make_response(jsonify(response_dict), 401)
    record_json = request.json
    if len(record_json) == 0:
        response_dict['message'] = "The provided JSON is empty"
        response_dict['status'] = '204'
        return make_response(jsonify(response_dict), 204)
    jsonOk, error = jsonHandler.check_validity(record_json)
    if not jsonOk:
        response_dict['message'] = "JSON invalid, " + error
        response_dict['status'] = '401'
        return make_response(jsonify(response_dict), 401)
    connection, cursor = databaseHandler.initialize_db()
    id = databaseHandler.insert_job(cursor, record_json)
    if id == -1:
        cursor.close()
        connection.close()
        response_dict['message'] = "The provided JSON could not be stored"
        response_dict['status'] = '500'
        return make_response(jsonify(response_dict), 500)
    connection.commit()
    cursor.close()
    connection.close()
    response_dict['id'] = id
    response_dict['message'] = "The print job was successfully stored"
    response_dict['status'] = '200'
    return make_response(jsonify(response_dict), 200)

@app.route('/outgoing', methods=['GET'])
@cross_origin()
def openJobs():
    connection, cursor = databaseHandler.initialize_db()
    response = make_response(jsonify(databaseHandler.get_open_jobs(cursor)))
    response.headers["Content-Type"] = "application/json"
    cursor.close()
    connection.close()
    return response

@app.route('/outgoing', methods=['PUT'])
@cross_origin()
def update_record():
    response_dict = {'id': 'NaN', 'message': 'Job was marked as processed', 'status': '200'}
    if not request.is_json:
        response_dict['message'] = "You have to provide a JSON with the key 'id' with an integer as value"
        response_dict['status'] = '401'
        return make_response(response_dict, 401)
    id_dict = request.json
    if len(id_dict) == 0:
        response_dict['message'] = "Provided JSON is empty, specify a key 'id' with an integer as value"
        response_dict['status'] = '204'
        return make_response(response_dict, 204)
    if 'id' not in id_dict:
        response_dict['message'] = "You have to provide a job ID with the key 'id' and an integer as value"
        response_dict['status'] = '401'
        return make_response(response_dict, 401)
    id = -1
    try:
        id = int(id_dict['id'])
    except ValueError:
        response_dict['message'] = 'The job ID must be an integer'
        response_dict['status'] = '401'
        return make_response(response_dict, 401)
    response_dict['id'] = str(id)
    connection, cursor = databaseHandler.initialize_db()
    if not databaseHandler.mark_job_processed(cursor, id):
        response_dict['message'] = 'Job ID not found in database'
        response_dict['status'] = '401'
        cursor.close()
        connection.close()
        return make_response(response_dict, 401)
    connection.commit()
    cursor.close()
    connection.close()
    return make_response(response_dict, 200)

@app.route('/outgoing', methods=['DELETE'])
@cross_origin()
def remove_record():
    response_dict = {'id': 'NaN', 'message': 'Job was removed', 'status': '200'}
    if not request.is_json:
        response_dict['message'] = "You have to provide a JSON with the key 'id' with an integer as value"
        response_dict['status'] = '401'
        return make_response(response_dict, 401)
    id_dict = request.json
    if len(id_dict) == 0:
        response_dict['message'] = "Provided JSON is empty, specify a key 'id' with an integer as value"
        response_dict['status'] = '204'
        return make_response(response_dict, 204)
    if 'id' not in id_dict:
        response_dict['message'] = "You have to provide a job ID with the key 'id' and an integer as value"
        response_dict['status'] = '401'
        return make_response(response_dict, 401)
    id = -1
    try:
        id = int(id_dict['id'])
    except ValueError:
        response_dict['message'] = 'The job ID must be an integer'
        response_dict['status'] = '401'
        return make_response(response_dict, 401)
    response_dict['id'] = str(id)
    connection, cursor = databaseHandler.initialize_db()
    if not databaseHandler.remove_job(cursor, id):
        response_dict['message'] = 'Job ID not found in database'
        response_dict['status'] = '401'
        cursor.close()
        connection.close()
        return make_response(response_dict, 401)
    connection.commit()
    cursor.close()
    connection.close()
    return make_response(response_dict, 200)