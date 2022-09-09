from flask import Flask, request, jsonify, make_response
import databaseHandler, inputHandler, printHandler
from flask_cors import CORS, cross_origin
app = Flask('QueryClient_RESTAPI')
cors = CORS(app)
app.json.sort_keys = False
app.config['CORS_HEADERS'] = 'Content-Type'

def check_id_json(request_json: dict, response_dict: dict) -> int:
    """
    Checks the JSON contain in the HTTP PUT and DELETE requests

    :param request_json: The request JSON
    :param response_dict: The JSON containing the response
    :return: Return the HTTP return code
    """
    if len(request_json) == 0:
        response_dict['message'] = "Provided JSON is empty, specify a key 'id' with an integer as value"
        response_dict['status'] = 204
        return 204
    if 'id' not in request_json:
        response_dict['message'] = "You have to provide a job ID with the key 'id' and an integer as value"
        response_dict['status'] = 401
        return 401
    try:
        id = int(request_json['id'])
    except ValueError:
        response_dict['message'] = 'The job ID must be an integer'
        response_dict['status'] = 401
        return 401
    response_dict['id'] = id
    return 200

def delete_entry(id: int, response_dict: dict) -> int :
    """
    Deletes a print job specified by an ID from the database

    :param id: The ID of the print job
    :param response_dict: The JSON containing the response
    :return: Returns a HTTP return code
    """
    connection, cursor = databaseHandler.initialize_db()
    if not databaseHandler.remove_job(cursor, id):
        response_dict['message'] = 'Job ID not found in database'
        response_dict['status'] = 401
        cursor.close()
        connection.close()
        return 401
    connection.commit()
    cursor.close()
    connection.close()
    return 200



@app.route('/incoming', methods=['POST'])
@cross_origin()
def insert_record():
    """
    Processes a POST request by inserting a print job in the database

    :return: Returns a Flask HTTP response with the generated ID of the job, a message, and return code
    """
    response_dict = {'message':'The print job was successfully stored', 'status':'200'}
    if not request.is_json:
        response_dict['message'] = "You have to provide a JSON"
        response_dict['status'] = 401
        return make_response(jsonify(response_dict), 401)
    record_json = request.json
    if len(record_json) == 0:
        response_dict['message'] = "The provided JSON is empty"
        response_dict['status'] = 204
        return make_response(jsonify(response_dict), 204)
    jsonOk, error, converted_json = inputHandler.check_validity(record_json)
    if not jsonOk:
        response_dict['message'] = "JSON invalid, " + error
        response_dict['status'] = 401
        return make_response(jsonify(response_dict), 401)
    connection, cursor = databaseHandler.initialize_db()
    id = databaseHandler.insert_job(cursor, converted_json)
    if id == -1:
        cursor.close()
        connection.close()
        response_dict['message'] = "The provided JSON could not be stored"
        response_dict['status'] = 500
        return make_response(jsonify(response_dict), 500)
    connection.commit()
    cursor.close()
    connection.close()
    response_dict['id'] = id
    response_dict['message'] = "The print job was successfully stored"
    response_dict['status'] = 200
    return make_response(jsonify(response_dict), 200)

@app.route('/outgoing', methods=['GET'])
@cross_origin()
def get_jobs():
    """
    Processes a GET request by retrieving all print jobs from the database

    :return: Returns a Flask HTTP response containing all jobs in the database
    """
    connection, cursor = databaseHandler.initialize_db()
    response = make_response(jsonify(databaseHandler.get_all_jobs(cursor)))
    response.headers["Content-Type"] = "application/json"
    cursor.close()
    connection.close()
    return response

@app.route('/outgoing', methods=['PUT'])
@cross_origin()
def process_record():
    """
    Processes a PUT request by sending the data for the given print job to the printers

    :return: Returns a Flask HTTP response with the ID of the specified job, a message, and return code
    """
    response_dict = {'id': 'NaN', 'message': 'Job was processed', 'status': '200'}
    if not request.is_json:
        response_dict['message'] = "You have to provide a JSON with the key 'id' with an integer as value"
        response_dict['status'] = 401
        return make_response(response_dict, 401)
    request_json = request.json
    return_code = check_id_json(request_json, response_dict)
    if return_code != 200:
        return make_response(response_dict, return_code)
    id = response_dict['id']
    connection, cursor = databaseHandler.initialize_db()
    record = databaseHandler.get_job(cursor, id)
    if len(record) == 0:
        response_dict['message'] = 'Job ID not found in database'
        response_dict['status'] = 401
        cursor.close()
        connection.close()
        return make_response(response_dict, 401)
    cursor.close()
    connection.close()
    # print label
    label_ok = printHandler.print_label(record)
    if not label_ok:
        print('Label could not be printed')
        print('Currently the label printer might not be attached, the print text would be')
        print(printHandler.generate_label_string(record))
        response_dict['message'] = 'Could not print label'
        response_dict['status'] = 500
        return make_response(response_dict, 500)
    return_code = delete_entry(response_dict['id'], response_dict)
    return make_response(response_dict, return_code)

@app.route('/outgoing', methods=['DELETE'])
@cross_origin()
def remove_record():
    """
    Processes a DELETE request by deleting a print job from the database without printing it

    :return: Returns a Flask HTTP response with the ID of the specified job, a message, and return code
    """
    response_dict = {'id': 'NaN', 'message': 'Job was removed', 'status': '200'}
    if not request.is_json:
        response_dict['message'] = "You have to provide a JSON with the key 'id' with an integer as value"
        response_dict['status'] = 401
        return make_response(response_dict, 401)
    request_json = request.json
    return_code = check_id_json(request_json, response_dict)
    if return_code != 200:
        return make_response(response_dict, return_code)
    return_code = delete_entry(response_dict['id'], response_dict)
    return make_response(response_dict, return_code)