import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.classes import Service
from src.backend.app import app
from src.backend.classes.models import User, db


# Create a test client
client = TestClient(app)

INPUT_ERROR = 400
AUTHENTICATION_ERROR = 401
SUCCESS = 200

def clear_all():
    ''' 
        Method to reset local database for new test
    '''
    response = client.post("/testing/clear")
    assert response.status_code == SUCCESS
    assert  response.json() == {"message" : "Clear Successful"}
    db.users.delete_many({})

@pytest.fixture
def simple_user():
    '''
        Simulates a simple user registering their account then logging in
    '''
    # Clear data abse
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

    return usable_data


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
                'tags' : ['API']
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['sid']
    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    assert response.status_code == SUCCESS
    response_info = response.json()[0]
    assert response_info['sid'] == sid
    assert response_info['name'] == api_info['name']
    assert response_info['description'] == api_info['description']
    assert response_info['tags'] == api_info['tags']