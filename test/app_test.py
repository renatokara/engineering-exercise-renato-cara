"""The tests to run in this project.
To run the tests type,
$ nosetests --verbose
"""

from nose.tools import assert_true, assert_false
import requests
import json
#import app.service.DataService as data_service

# BASE_URL = "http://127.0.0.1"
BASE_URL = "http://localhost:5000"
# BASE_URL = "https://python3-flask-uat.herokuapp.com/"


def test_insert():
    """
        Inserts a new data 
    """
    payload = json.loads("""
        {
            "title": "Test Case INSERT Renato Cara",
            "uri": "http://test-renato-cara-insert.com/",
            "date": "2014-03-08T15"
            }
    """)
    response = requests.post(f'{BASE_URL}/data', json=payload)
    assert_true(response.status_code == 201)

def test_fail_insert_title():
    """
        Fails to inserts a new data because title is null 
    """
    payload = json.loads("""
        {
            "title": null,
            "uri": "http://test-renato-cara-insert.com/",
            "date": "2014-03-08T15"
            }
    """)
    response = requests.post(f'{BASE_URL}/data', json=payload)
    assert_true(response.status_code == 400)

def test_fail_insert_uri():
    """
        Fails to inserts a new data because uri is wrong 
    """
    payload = json.loads("""
        {
            "title": "Test Case INSERT Renato Cara",
            "uri": "//loremipsum/",
            "date": "2014-03-08T15"
            }
    """)
    response = requests.post(f'{BASE_URL}/data', json=payload)
    assert_true(response.status_code == 400)


def test_fail_insert_date():
    """
        Fails to inserts a new data because date is empty 
    """
    payload = json.loads("""
        {
            "title": "Test Case INSERT Renato Cara",
            "uri": "http://test-renato-cara-insert.com/",
            "date": ""
            }
    """)
    response = requests.post(f'{BASE_URL}/data', json=payload)
    assert_true(response.status_code == 400)


#def test_validation_date():
#    assert_true(data_service.validate_date('February 07 1984'))
#    assert_false(data_service.validate_date('February 666 1984'))
#    assert_false(data_service.validate_date(None))
#    assert_false(data_service.validate_date(''))
#    assert_false(data_service.validate_date('1991-03-11T01:39:21'))
#
#def test_validation_uri():
#    assert_true(data_service.validate_uri('http://www.brown-mcdonald.com/'))
#    assert_true(data_service.validate_uri('https://gonzalez.org/tags/posts/categories/terms.html'))
#    assert_true(data_service.validate_uri('file://gonzalez.org/'))
#    assert_false(data_service.validate_uri('Lorem Ipsum'))
#    assert_false(data_service.validate_uri('//le.net/main.php'))
#    assert_false(data_service.validate_uri(None))
#    assert_false(data_service.validate_uri(''))
#    assert_true(data_service.validate_uri('1991-03-11T01:39:21'))



def test_import():
    "Test import a new record"
    
    payload = json.loads("""{
        "items": [
            {
            "title": "Test Case Renato Cara",
            "uri": "http://test-renato-cara.com/",
            "date": "2014-03-08T15"
            },
            {
            "title": "Test Case Renato Cara 2",
            "uri": "http://test-renato-cara-2.com/",
            "date": "March 04 1987"
            },
            {
            "title": null,
            "uri": "http://www.hood.net/about.html",
            "date": "March 30 1985"
            },
            {
            "title": null,
            "uri": null,
            "date": "March 30 1985"
            }
            ]}
        """)
    response = requests.post(f'{BASE_URL}/data/import', json=payload)
    assert_true(response.status_code == 201)
    resp = response.json()
    assert_true(resp['created'] == 2)
    assert_true(len(resp['errors']) == 2)




def test_get_all_data():
    "Test getting all data"
    response = requests.get('%s/data' % (BASE_URL))
    assert_true(response.ok)

def test_filter_update_and_delete():
    """
        Testes filtering iterate over the results update and then deletes
    """
    payload = json.loads("""
        {
            "title": "Test Case Renato Cara",
            "uri": null,
            "date": null
        }
        """)
    response = requests.post(f'{BASE_URL}/data/filter', json=payload)
    assert_true(response.status_code == 200)
    resp = response.json()
    for r in resp:
        id = r['id']
        r['title'] = 'An Updated title'
        r['uri'] = 'http://google.com/'
        r['date'] = r['date_added']
        print(r)
        respUpdate = requests.put(f'{BASE_URL}/data', json = r)
        print(respUpdate.json())
        assert_true(respUpdate.status_code == 200)
        respDelete = requests.delete(f'{BASE_URL}/data/{id}')
        assert_true(respDelete.status_code == 204)
    