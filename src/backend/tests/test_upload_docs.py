import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.app import app 
from src.backend.classes.models import db

# Create a test client
client = TestClient(app)

INPUT_ERROR = 400
AUTHENTICATION_ERROR = 401
SUCCESS = 200

def clear_all():
    '''
        Method to reset local databsed for new test
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
    # Clear database
    clear_all()

    usable_data = {"token" : None}

    # Register user
    user_creds = {
        "username" : "Tester 1",
        "password" : "password",
        "email" : "doxxed@gmail.com"
    }

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

@pytest.fixture
def two_users():
    '''
        Scenario with two users, general user and service-provider
    '''

    # Clear data
    clear_all()

    # Register users
    creator_creds = {
        "username" : "Creator",
        "password" : "password",
        "email" : "doxxed@gmail.com",
        "role" : "service provider"
    }
    user_creds = {
        "username" : "User",
        "password" : "password",
        "email" : "doxxed2@gmail.com",
        "role" : "account user"
    }

# Error Testing
def test_invalid_file(simple_user):
    '''
        Test whether non-pdf files are caught
    '''
    pass

def test_no_file(simple_user):
    '''
        Test whether no-file is caught
    '''
    pass

def test_no_service(simple_user):
    '''
        Test whether uploading to non-existent service is caught
    '''
    pass

def test_no_perms(two_users):
    '''
        Test whether uploading as non-owner is caught
    '''
    pass


# Success Cases (Cannot be tested)