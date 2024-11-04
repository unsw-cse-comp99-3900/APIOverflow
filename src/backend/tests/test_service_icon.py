import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.app import app 
from src.backend.classes.models import db

# Create a test client
client = TestClient(app)

INPUT_ERROR = 400
MISSING_ERROR = 404
FORBIDDEN_ERROR = 403
SUCCESS = 200
AUTHENTICATION_ERROR = 401

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
        "displayname" : "Tester 1",
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

    # Generate imposter
    imp_creds = {
        'displayname' : 'Sus Imposter 69420',
        'username' : 'Sus Imposter',
        'password': 'amogus',
        'email' : 'hackerman@gmail.com'
    }

    response = client.post("/auth/register",
                           json=imp_creds)
    assert response.status_code == SUCCESS

    # Imposter login
    response = client.post("/auth/login",
                           json=imp_creds)
    assert response.status_code == SUCCESS
    usable_data['i_token'] = response.json()['access_token']

    # Create an API
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
                           headers={"Authorization": f"Bearer {usable_data['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    usable_data['sid'] = response.json()['id']

    yield usable_data
    clear_all()

def test_guest_attempt():
    '''
        Test whether guest attempt is caught
    '''
    file = {
        'file' : open('tests/resources/default_icon.png', 'rb')
    }

    response = client.post("/upload/imgs", files=file)
    assert response.status_code == SUCCESS

    doc_id = response.json()['doc_id']
    package = {'sid': '0',
               'doc_id': doc_id}
    response = client.post("/service/add_icon", 
                           headers={"Authorization": f"Bearer"},
                           json=package)
    assert response.status_code == AUTHENTICATION_ERROR

def test_bad_icon(simple_user):
    '''
        Test whether an invalid icon is caught
    '''
    data = simple_user
    package = {'sid': data['sid'],
               'doc_id': '-111'}
    response = client.post("/service/add_icon", 
                           headers={"Authorization": f"Bearer {data['token']}"},
                           json=package)
    assert response.status_code == MISSING_ERROR

def test_bad_service_add(simple_user):
    '''
        Test whether a invalid service is caught
    '''
    data = simple_user
    file = {
        'file' : open('tests/resources/default_icon.png', 'rb')
    }

    response = client.post("/upload/imgs", files=file)
    assert response.status_code == SUCCESS
    doc_id = response.json()['doc_id']

    package = {'sid': '-111',
               'doc_id': doc_id}
    response = client.post("/service/add_icon", 
                           headers={"Authorization": f"Bearer {data['token']}"},
                           json=package)
    assert response.status_code == MISSING_ERROR

def test_not_owner_add(simple_user):
    '''
        Test whether a non-owner attempting modification is rejected
    '''
    data = simple_user
    file = {
        'file' : open('tests/resources/default_icon.png', 'rb')
    }

    response = client.post("/upload/imgs", files=file)
    assert response.status_code == SUCCESS
    doc_id = response.json()['doc_id']

    package = {'sid': data['sid'],
               'doc_id': doc_id}
    response = client.post("/service/add_icon", 
                           headers={"Authorization": f"Bearer {data['i_token']}"},
                           json=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_not_owner_delete(simple_user):
    '''
        Test whether a non-owner attempting deletion is rejected
    '''
    data = simple_user
    package = {'sid': data['sid']}
    response = client.delete("/service/delete_icon", 
                           headers={"Authorization": f"Bearer {data['i_token']}"},
                           params=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_bad_service_delete(simple_user):
    '''
        Test whether an invalid service is caught
    '''
    data = simple_user
    package = {'sid': '-111'}
    response = client.delete("/service/delete_icon", 
                           headers={"Authorization": f"Bearer {data['token']}"},
                           params=package)
    assert response.status_code == MISSING_ERROR

def test_successful_add(simple_user):
    '''
        Test a successful update of icon
    '''
    data = simple_user
    file = {
        'file' : open('tests/resources/default_icon.png', 'rb')
    }

    response = client.post("/upload/imgs", files=file)
    assert response.status_code == SUCCESS
    doc_id = response.json()['doc_id']

    package = {'sid': data['sid'],
               'doc_id': doc_id}
    response = client.post("/service/add_icon", 
                           headers={"Authorization": f"Bearer {data['token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {data['token']}"},
                          params={'sid': data['sid']})
    assert response.json()['icon'] == '1'

def test_successful_delete(simple_user):
    '''
        Test a successful modification then delete
    '''
    data = simple_user
    file = {
        'file' : open('tests/resources/default_icon.png', 'rb')
    }

    response = client.post("/upload/imgs", files=file)
    assert response.status_code == SUCCESS
    doc_id = response.json()['doc_id']

    package = {'sid': data['sid'],
               'doc_id': doc_id}
    response = client.post("/service/add_icon", 
                           headers={"Authorization": f"Bearer {data['token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {data['token']}"},
                          params={'sid': data['sid']})
    assert response.json()['icon'] == '1'

    # Delete
    response = client.delete("/service/delete_icon",
                             headers={"Authorization": f"Bearer {data['token']}"},
                            params={'sid': data['sid']})
    assert response.status_code == SUCCESS

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {data['token']}"},
                          params={'sid': data['sid']})
    assert response.json()['icon'] == '0'
