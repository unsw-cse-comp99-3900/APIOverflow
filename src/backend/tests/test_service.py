import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.classes import Service
from src.backend.app import app
from src.backend.classes.models import User
from src.backend.database import *


# Create a test client
client = TestClient(app)

INPUT_ERROR = 400
AUTHENTICATION_ERROR = 401
SUCCESS = 200
NOT_FOUND = 404

def clear_all():
    ''' 
        Method to reset local database for new test
    '''
    response = client.post("/testing/clear")
    assert response.status_code == SUCCESS
    assert response.json() == {"message" : "Clear Successful"}

@pytest.fixture
def simple_user():
    '''
        Simulates a simple user registering their account then logging in
    '''
    # Clear database
    clear_all()

    # Register user
    user_creds = {
        "username" : "Tester 1",
        "password" : "password",
        "email" : "doxxed@gmail.com"
    }

    usable_data = {"token" : None}

    response = client.post("/auth/register",
                            json=user_creds)
    assert response.status_code == SUCCESS

    # Log into account
    response = client.post("/auth/login",
                           json=user_creds)
    assert response.status_code == SUCCESS
    usable_data['token'] = response.json()['access_token']

    yield usable_data
    clear_all()

# Error testing
def test_invalid_user(simple_user):
    '''
        Test that add_service is only usable by users not guests
    '''
    response = client.post("/service/add",
                           headers={"Authorization": "Bearer"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : '',
                                'tags' : [],
                                'endpoint': ''
                           })
    assert response.status_code == AUTHENTICATION_ERROR


def test_no_name(simple_user):
    '''
        Test whether no name is caught
    '''
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                            json={
                                'name' : '',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : '',
                                'tags' : [],
                                'endpoint': ''
                           })
    assert response.status_code == INPUT_ERROR

def test_invalid_url(simple_user):
    '''
        Test whether bad url (www.googlefake.xyzabsdh) is caught
    '''
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : 'www.googlefake.xyzabsdh',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : 'hi',
                                'tags' : ['API'],
                                'endpoint': ''
                           })
    assert response.status_code == INPUT_ERROR

def test_invalid_dimensions(simple_user):
    '''
        Test whether combinations of bad dimensions are caught
    '''
    # Negative x-start
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : -10,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : 'hi',
                                'tags' : ['API'],
                                'endpoint': ''
                           })
    assert response.status_code == INPUT_ERROR

    # x-start bigger than x-end
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 1000,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : 'hi',
                                'tags' : ['API'],
                                'endpoint': ''
                           })
    assert response.status_code == INPUT_ERROR

    # Negative y-start
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : -10,
                                'y_end' : 0,
                                'description' : 'hi',
                                'tags' : ['API'],
                                'endpoint': ''
                           })
    assert response.status_code == INPUT_ERROR

    # Bigger y-start than y-end
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 1000,
                                'y_end' : 0,
                                'description' : 'hi',
                                'tags' : ['API'],
                                'endpoint': ''
                           })
    assert response.status_code == INPUT_ERROR

def test_no_description(simple_user):
    '''
        Test whether no description given is caught
    '''
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : '',
                                'tags' : [],
                                'endpoint': ''
                           })
    assert response.status_code == INPUT_ERROR

def test_no_tags(simple_user):
    '''
        Test whether no description given is caught
    '''
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : 'This is a test API',
                                'tags' : [],
                                'endpoint': ''
                           })
    assert response.status_code == INPUT_ERROR

def test_no_endpoint(simple_user):
    '''
        Test whether no description given is caught
    '''
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : 'This is a test API',
                                'tags' : ['API'],
                                'endpoint': ''
                           })
    assert response.status_code == INPUT_ERROR

# Valid instances
def test_create_api(simple_user):
    '''
        Test whether an API is correctly created
    '''
    api_info = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoint': 'https://api.example.com/users/12345'
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']
    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info['id'] == sid
    assert response_info['name'] == api_info['name']
    assert response_info['description'] == api_info['description']
    assert response_info['tags'] == api_info['tags']
    assert response_info['endpoint'] == api_info['endpoint']

    database_object = db_get_service(sid)
    assert database_object['id'] == sid
    assert database_object['name'] == api_info['name']
    assert database_object['description'] == api_info['description']
    assert database_object['tags'] == api_info['tags']
    assert database_object['endpoint'] == api_info['endpoint']

def test_multiple_tags(simple_user):
    '''
        Test whether an API is correctly created where it has multiple tags
    '''
    api_info = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API', 'Public', 'In Development'],
                'endpoint': 'https://api.example.com/users/12345'
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info['id'] == sid
    assert response_info['name'] == api_info['name']
    assert response_info['description'] == api_info['description']
    assert response_info['tags'] == api_info['tags']
    assert response_info['endpoint'] == api_info['endpoint']
    assert response_info['icon_url'] == ''

def test_custom_icon(simple_user):
    '''
        Test whether create can handle custom icon_url:
            http://cdn.mos.cms.futurecdn.net/iC7HBvohbJqExqvbKcV3pP.jpg
    '''
    api_info = {
                'name' : 'Fake Google',
                'icon_url': 'http://cdn.mos.cms.futurecdn.net/iC7HBvohbJqExqvbKcV3pP.jpg',
                'x_start' : 0,
                'x_end' : 100,
                'y_start' : 0,
                'y_end' : 100,
                'description' : 'This is a definitely... Google',
                'tags' : ['API', 'Public', 'In Development'],
                'endpoint': 'https://api.example.com/users/12345'
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']
    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'token' : simple_user['token'],
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info['id'] == sid
    assert response_info['name'] == api_info['name']
    assert response_info['description'] == api_info['description']
    assert response_info['tags'] == api_info['tags']
    assert response_info['endpoint'] == api_info['endpoint']

def test_update_api(simple_user):
    '''
        Test whether an API is correctly created then updated
    '''
    api_info = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoint': 'https://api.example.com/users/12345'
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']

    update_request_info = {
        'sid' : sid,
        'name' : 'new name',
        'description' : 'new description',
        'tags' : ['new', 'tag'],
        'endpoint': 'https://api.example.com/users/12345'
    }

    response = client.put("/service/update",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=update_request_info)
    assert response.status_code == SUCCESS
    
    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
   
    assert response_info['id'] == sid
    assert response_info['name'] == update_request_info['name']
    assert response_info['description'] == update_request_info['description']
    assert response_info['tags'] == update_request_info['tags']
    assert response_info['endpoint'] == update_request_info['endpoint']

    database_object = db_get_service(sid)
    assert database_object['id'] == sid
    assert database_object['name'] == update_request_info['name']
    assert database_object['description'] == update_request_info['description']
    assert database_object['tags'] == update_request_info['tags']
    assert database_object['endpoint'] == update_request_info['endpoint']

def test_update_api_invalid_sid(simple_user):
    '''
        Tests error received when sid is not valid
    '''

    api_info = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoint': 'https://api.example.com/users/12345'
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS

    update_request_info = {
        'sid' : "invalid id",
        'name' : 'new name',
        'description' : 'new name',
        'tags' : ['new', 'name'],
        'endpoint': 'https://api.example.com/users/12345'
    }

    response = client.put("/service/update",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=update_request_info)
    assert response.status_code == 404

def test_update_api_documents(simple_user):
    '''
        Test whether an API is correctly created then updated
    '''
    api_info = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoint': 'https://api.example.com/users/12345'
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']

    filename = 'git_guide.pdf'
    file = {
        'file' : (filename, open("tests/resources/git_guide.pdf", 'rb'))
    }
    response = client.post("/upload/pdfs", files=file)
    assert response.status_code == SUCCESS
 
    doc_id = response.json()['doc_id']
    api_data = {
        'sid': sid,
        'doc_id': doc_id
    }
    response = client.post("/service/upload_docs",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_data)
    assert response.status_code == SUCCESS
    
    response = client.get("/service/get_service",
                        params={
                            'sid': sid
                        })
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info['docs'] == ["static/docs/git_guide_1.pdf"]
    database_object = db_get_service(sid)

    # path of file is accessible via get_service but internally
    # stored by document id instead of path
    assert database_object['documents'] == [doc_id]

    update_request_info = {
        'sid' : sid,
        'name' : 'new name',
        'description' : 'new description',
        'tags' : ['new', 'tag'],
        'endpoint': 'https://api.example.com/users/12345'
    }

    response = client.put("/service/update",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=update_request_info)
    assert response.status_code == SUCCESS
    
    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
   
    assert response_info['docs'] == ["static/docs/git_guide_1.pdf"]
    database_object = db_get_service(sid)
    assert database_object['documents'] == [doc_id]

# Delete non-existing service
def test_delete_non_api(simple_user):
    '''
        Test whether an delete a fake service works
    '''
    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info == []

    response = client.delete("/service/delete",
                        headers={"Authorization": f"Bearer {simple_user['token']}"},
                        params={
                              'sid' : 'what'
                          })
    assert response.status_code == NOT_FOUND

# Delete instances
def test_delete_api(simple_user):
    '''
        Test whether delete an API works
    '''
    api_info1 = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoint': 'https://api.example.com/users/12345'
                }
    
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info1)
    assert response.status_code == SUCCESS
    sid = response.json()['id']

    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()[0]
    assert response_info != {}

    assert db_get_service(sid) is not None

    response = client.delete("/service/delete",
                        headers={"Authorization": f"Bearer {simple_user['token']}"},
                        params={
                              'sid' : sid
                          })
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info["name"] == api_info1['name']
    assert response_info["deleted"] == True
    assert db_get_service(sid) is None

    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info == []

def test_delete_apis(simple_user):
    '''
        Test whether delete an API with out of multiple APIs work
    '''
    api_info1 = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoint': 'https://api.example.com/users/12345'
                }
    
    api_info2 = {
                'name' : 'Test API I',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoint': 'https://api.example.com/users/12345'
                }
    
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info1)
    assert response.status_code == SUCCESS
    sid1 = response.json()['id']

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info2)
    assert response.status_code == SUCCESS
    sid2 = response.json()['id']

    response = client.delete("/service/delete",
                        headers={"Authorization": f"Bearer {simple_user['token']}"},
                        params={
                              'sid' : sid1
                          })
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info["name"] == api_info1['name']
    assert response_info["deleted"] == True

    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()[0]
    assert response_info['id'] == sid2
    assert response_info['name'] == api_info2['name']
    assert response_info['description'] == api_info2['description']
    assert response_info['tags'] == api_info2['tags']

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid1
                          })
    assert response.status_code == NOT_FOUND

    response = client.delete("/service/delete",
                        headers={"Authorization": f"Bearer {simple_user['token']}"},
                        params={
                              'sid' : sid2
                          })
    assert response.status_code == SUCCESS

    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info == []


# Valid instances
def test_get_apis(simple_user):
    '''
        Test whether an API is correctly get
    '''
    api_info1 = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoint': 'https://api.example.com/users/12345'
                }
    
    api_info2 = {
                'name' : 'Test API I',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoint': 'https://api.example.com/users/12345'
                }
    
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info1)
    assert response.status_code == SUCCESS
    sid1 = response.json()['id']

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info2)
    assert response.status_code == SUCCESS
    sid2 = response.json()['id']

    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()[0]
    assert response_info['id'] == sid1
    assert response_info['name'] == api_info1['name']
    assert response_info['description'] == api_info1['description']
    assert response_info['tags'] == api_info1['tags']

    response_info = response.json()[1]
    assert response_info['id'] == sid2
    assert response_info['name'] == api_info2['name']
    assert response_info['description'] == api_info2['description']
    assert response_info['tags'] == api_info2['tags']