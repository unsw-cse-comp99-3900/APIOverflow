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

    usable_data = {"token" : None,
                   "displayname" : "Tester 1",
                   "username" : "Tester 1",
                   "email": "doxxed@gmail.com"}

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

def test_user_profile_guest():
    '''
        Guest user attempt
    '''
    response = client.get("/user/get/profile",
                          headers={"Authorization": f"Bearer "})
    assert response.status_code == AUTHENTICATION_ERROR

def test_user_profile_invalid(simple_user):
    '''
        Test invalid user trying profile (not testable)
    '''
    assert 1 == 1

def test_user_profile_success(simple_user):
    '''
        Test successful case
    '''
    data = simple_user
    response = client.get("/user/get/profile",
                          headers={"Authorization": f"Bearer {data['token']}"})
    assert response.status_code == SUCCESS
    assert response.json()['email'] == data['email']
    assert response.json()['username'] == data['username'] 
    assert response.json()['icon'] == '0'

def test_user_profile_success_custom_icon(simple_user):
    '''
        Test successful case
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

    response = client.get("/user/get/profile",
                          headers={"Authorization": f"Bearer {data['token']}"})
    assert response.status_code == SUCCESS
    assert response.json()['email'] == data['email']
    assert response.json()['username'] == data['username'] 
    assert response.json()['icon'] == '1'

def test_user_delete_self(simple_user):
    data = simple_user
    response = client.delete("/user/delete/me", 
                        headers={"Authorization": f"Bearer {data['token']}"})
    assert response.status_code == SUCCESS
    assert response.json() == {"name": data['username'] , "deleted": True}

    response = client.delete("/user/delete/me", 
                        headers={"Authorization": f"Bearer {data['token']}"})
    assert response.status_code == AUTHENTICATION_ERROR

    response = client.post("/auth/login", json={
        "username": data['username'],
        "password": "password"
    })
    assert response.status_code == INPUT_ERROR

    response = client.post("/auth/register", json={
        "displayname": data['displayname'],
        "username": data['username'],
        "password": "password",
        "email" : "doxxed@gmail.com"
    })
    assert response.status_code == SUCCESS
    response = client.post("/auth/login", json={
        "username": data['username'],
        "password": "password"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.delete("/user/delete/me", 
                        headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS
    assert response.json() == {"name": data['username'] , "deleted": True}

def test_user_update_displayname(simple_user):
    '''
        Test successful case
    '''
    new_display = "Cool Display Name"
    data = simple_user
    response = client.post("/user/update/displayname",
                          headers={"Authorization": f"Bearer {data['token']}"},
                            json={
                                'content': "Cool Display Name"
                            })
    assert response.status_code == SUCCESS
    assert response.json() == {"displayname": new_display, "updated": True}

    response = client.get("/user/get/profile",
                          headers={"Authorization": f"Bearer {data['token']}"})
    assert response.status_code == SUCCESS
    assert response.json()['email'] == data['email']
    assert response.json()['displayname'] == new_display
    assert response.json()['displayname'] != data['displayname']
    assert response.json()['username'] == data['username']