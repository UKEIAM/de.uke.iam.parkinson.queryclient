import sys, json, pytest
sys.path.append('../src')
import databaseHandler, app
from unittest.mock import MagicMock

valid_data = [
    {
        "dataString":"Lustig|Peter|1990-03-05|12345|Station 9|Medi0815|Ibu 400|1.5|2022-08-17 01:01"
    },
    {
        "dataString":"Mustermann|Max|1995-01-01|05671|Station 1|Dope1|Asperin C|2|2022-08-17 01:01"
    },
    {
        "dataString":"Apfel|Anna|1967-08-08|12348|Station 2|Medi0815|Ibu 400|10.3|2022-09-09 11:08"
    }]

incomplete_data = {
    "dataString":"Peter|1990-03-05|12345|Station 9|Medi0815|Ibu 400|1.5|2022-08-17 01:01"
}

missing_key = {
    "invalid":"Lustig|Peter|1990-03-05|12345|Station 9|Medi0815|Ibu 400|1.5|2022-08-17 01:01"
}

invalid_date = {
    "dataString":"Lustig|Peter|1 May 1990|12345|Station 9|Medi0815|Ibu 400|1.5|2022-08-17 01:01"
}

invalid_timestamp = {
    "dataString":"Lustig|Peter|1990-03-05|12345|Station 9|Medi0815|Ibu 400|1.5|2022-08-17 01:01:01"
}

def test_insert_valid():
    databaseHandler.insert_job = MagicMock(return_value = 1)
    test_client = app.app.test_client()
    for record in valid_data:
        response = test_client.post('/incoming', data = json.dumps(record), content_type='application/json')
        assert response.status_code == 200

def test_insert_incomplete():
    databaseHandler.insert_job = MagicMock(return_value=1)
    test_client = app.app.test_client()
    response = test_client.post('/incoming', data=json.dumps(incomplete_data), content_type='application/json')
    assert response.status_code == 401

def test_invalid_date():
    databaseHandler.insert_job = MagicMock(return_value=1)
    test_client = app.app.test_client()
    response = test_client.post('/incoming', data=json.dumps(invalid_date), content_type='application/json')
    assert response.status_code == 401
    response = test_client.post('/incoming', data=json.dumps(invalid_timestamp), content_type='application/json')
    assert response.status_code == 401

def test_mark_processed():
    databaseHandler.remove_job = MagicMock(return_value=True)
    test_client = app.app.test_client()
    response = test_client.put('/outgoing', data='{"id":1}', content_type='application/json')
    assert response.status_code == 200
    # empty JSON
    response = test_client.put('/outgoing', data='{}', content_type='application/json')
    assert response.status_code == 204
    # no entry 'id'
    response = test_client.put('/outgoing', data='{"param":"val"}', content_type='application/json')
    assert response.status_code == 401
    # entry 'id' is not an integer
    response = test_client.put('/outgoing', data='{"id":"invalid"}', content_type='application/json')
    assert response.status_code == 401
    # 'id' not found in database
    databaseHandler.remove_job = MagicMock(return_value=False)
    response = test_client.put('/outgoing', data='{"id":1}', content_type='application/json')
    assert response.status_code == 401

def test_remove():
    databaseHandler.remove_job = MagicMock(return_value=True)
    test_client = app.app.test_client()
    response = test_client.delete('/outgoing', data='{"id":1}', content_type='application/json')
    assert response.status_code == 200
    # emtpy JSON
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

