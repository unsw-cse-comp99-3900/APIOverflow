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

    usable_data = {"c_token" : None}

    response = client.post("/auth/register",
                            json=user_creds)
    assert response.status_code == SUCCESS

    # Log into account
    response = client.post("/auth/login",
                           json=user_creds)
    assert response.status_code == SUCCESS
    usable_data['c_token'] = response.json()['access_token']

    # Generate imposter
    user_creds = {
        'username' : 'Sus Imposter',
        'password': 'amogus',
        'email' : 'hackerman@gmail.com'
    }

    response = client.post("/auth/register",
                           json=user_creds)
    assert response.status_code == SUCCESS

    # Imposter login
    response = client.post("/auth/login",
                           json=user_creds)
    assert response.status_code == SUCCESS
    usable_data['u_token'] = response.json()['access_token']

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
                           headers={"Authorization": f"Bearer {usable_data['c_token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    usable_data['sid'] = response.json()['id']

    yield usable_data
    clear_all()