import sys, json, copy, pytest
sys.path.append('../src')
import databaseHandler, app
from unittest.mock import MagicMock

valid_data = [
    {"surname":"Lustig",
      "givenName":"Peter",
      "birthday":"1990-03-05",
      "logisticsID":"145",
      "medicationName": "Best Stoff",
      "medicationDose": "60/40",
      "medicationUnit":"l",
      "medicationTimestamp": "2022-01-01 15:22:10",
      "hospitalWard":"St 5"},
    {"surname":"Columna",
      "givenName":"Carla",
      "birthday":"1981-03-22",
      "logisticsID":"123",
      "medicationName": "Okay Stoff",
      "medicationDose": "20/80",
      "medicationUnit":"t",
      "medicationTimestamp": "2022-02-02 14:22:17",
      "hospitalWard":"Station Uno"},
    {"surname":"Mustermann",
      "givenName":"Max",
      "birthday":"1900-03-22",
      "logisticsID":"121",
      "medicationName": "Guter Stoff",
      "medicationDose": "10/-90",
      "medicationUnit":"kg",
      "medicationTimestamp": "2022-08-17 01:01:17",
      "hospitalWard":"Station 2"}]

def test_insert_valid():
    databaseHandler.insert_job = MagicMock(return_value = 1)
    test_client = app.app.test_client()
    for record in valid_data:
        response = test_client.post('/incoming', data = json.dumps(record), content_type='application/json')
        assert response.status_code == 200

def test_insert_incomplete():
    databaseHandler.insert_job = MagicMock(return_value=1)
    test_client = app.app.test_client()
    for key in  valid_data[0].keys():
        invalid = copy.deepcopy(valid_data[0])
        del invalid[key]
        response = test_client.post('/incoming', data=json.dumps(invalid), content_type='application/json')
        assert response.status_code == 401

def test_invalid_date():
    databaseHandler.insert_job = MagicMock(return_value=1)
    test_client = app.app.test_client()
    invalid_date = copy.deepcopy(valid_data[0])
    invalid_date['birthday'] = '12 May 1990'
    response = test_client.post('/incoming', data=json.dumps(invalid_date), content_type='application/json')
    assert response.status_code == 401

    invalid_timestamp = copy.deepcopy(valid_data[0])
    invalid_timestamp['medicationTimestamp'] = '1990-05-12 13:30 Uhr'
    response = test_client.post('/incoming', data=json.dumps(invalid_timestamp), content_type='application/json')
    assert response.status_code == 401

def test_mark_processed():
    databaseHandler.mark_job_processed = MagicMock(return_value=True)
    test_client = app.app.test_client()
    response = test_client.put('/outgoing', data='{"id":1}', content_type='application/json')
    assert response.status_code == 200
    # empy JSON
    response = test_client.put('/outgoing', data='{}', content_type='application/json')
    assert response.status_code == 204
    # no entry 'id'
    response = test_client.put('/outgoing', data='{"param":"val"}', content_type='application/json')
    assert response.status_code == 401
    # entry 'id' is not an integer
    response = test_client.put('/outgoing', data='{"id":"invalid"}', content_type='application/json')
    assert response.status_code == 401
    # 'id' not found in database
    databaseHandler.mark_job_processed = MagicMock(return_value=False)
    response = test_client.put('/outgoing', data='{"id":1}', content_type='application/json')
    assert response.status_code == 401

def test_remove():
    databaseHandler.remove_job = MagicMock(return_value=True)
    test_client = app.app.test_client()
    response = test_client.delete('/outgoing', data='{"id":1}', content_type='application/json')
    assert response.status_code == 200
    # empy JSON
    response = test_client.delete('/outgoing', data='{}', content_type='application/json')
    assert response.status_code == 204
    # no entry 'id'
    response = test_client.delete('/outgoing', data='{"param":"val"}', content_type='application/json')
    assert response.status_code == 401
    # entry 'id' is not an integer
    response = test_client.delete('/outgoing', data='{"id":"invalid"}', content_type='application/json')
    assert response.status_code == 401
    # 'id' not found in database
    databaseHandler.remove_job = MagicMock(return_value=False)
    response = test_client.delete('/outgoing', data='{"id":1}', content_type='application/json')
    assert response.status_code == 401

if __name__ == '__main__':
    pytest.main(['apiTest.py'])


