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

def test_guest_update():
    '''
        Tests whether an unlogged account would be caught
    '''
    file = {
        'file' : open('tests/resources/default_icon.png', 'rb')
    }

    response = client.post("/upload/imgs", files=file)
    assert response.status_code == SUCCESS

    doc_id = response.json()['doc_id']
    package = {'doc_id': doc_id}
    response = client.post("/user/add_icon", 
                           headers={"Authorization": f"Bearer"},
                           json=package)
    assert response.status_code == AUTHENTICATION_ERROR

def test_bad_icon(simple_user):
    '''
        Tests whether an invalid icon is caught
    '''
    data = simple_user
    package = {
        'doc_id': '-111'
        }
    response = client.post("/user/add_icon",
                           headers={"Authorization": f"Bearer {data['token']}"},
                           json=package)
    print(response.json()['detail'])
    assert response.status_code == MISSING_ERROR

def test_delete_guest():
    '''
        Tests whether a guest attempting to delete an icon is caught
    '''
    response = client.delete("/user/delete_icon",
                           headers={"Authorization": f"Bearer"})
    assert response.status_code == AUTHENTICATION_ERROR

def test_successful_icon(simple_user):
    '''
        Test a successful icon add
    '''
    data = simple_user
    file = {
        'file' : open('tests/resources/default_icon.png', 'rb')
    }

    response = client.post("/upload/imgs", files=file)
    assert response.status_code == SUCCESS

    doc_id = response.json()['doc_id']

    response = client.post("/user/add_icon", 
                        headers={"Authorization": f"Bearer {data['token']}"},
                        json={
                            'doc_id': doc_id
                        })
    assert response.status_code == SUCCESS

    response = client.get("/user/get",
                          headers={"Authorization": f"Bearer {data['token']}"},
                          params={})
    assert response.json()['icon'] == '1'

def test_successful_delete(simple_user):
    '''
        Test whether delete is successful
    '''
    data = simple_user
    file = {
        'file' : open('tests/resources/default_icon.png', 'rb')
    }

    response = client.post("/upload/imgs", files=file)
    assert response.status_code == SUCCESS

    doc_id = response.json()['doc_id']

    response = client.post("/user/add_icon", 
                        headers={"Authorization": f"Bearer {data['token']}"},
                        json={
                            'doc_id': doc_id
                        })
    assert response.status_code == SUCCESS

    response = client.get("/user/get",
                          headers={"Authorization": f"Bearer {data['token']}"},
                          params={})
    assert response.json()['icon'] == '1'

    response = client.delete("/user/delete_icon",
                             headers={"Authorization": f"Bearer {data['token']}"})
    assert response.status_code == SUCCESS

    response = client.get("/user/get",
                          headers={"Authorization": f"Bearer {data['token']}"},
                          params={})
    assert response.json()['icon'] == '0'
