import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.classes import Service
from src.backend.app import app
from src.backend.classes.models import User
from src.backend.database import *
from src.backend.classes.Endpoint import Endpoint
from src.backend.classes.Parameter import Parameter 
from src.backend.classes.Response import Response

# Create a test client
client = TestClient(app)

INPUT_ERROR = 400
AUTHENTICATION_ERROR = 401
SUCCESS = 200
NOT_FOUND = 404

# test endpoint
simple_parameter = Parameter(id="1", endpoint_link='https://api.example.com/users/12345', required=True, 
                            type='HEADER', name='paramtest', value_type='int')
simple_response = Response(code='404', description='not found', conditions=["site is down", "badtest"], 
                            example="example...")
simple_endpoint = Endpoint(link='https://api.example.com/users/12345', title_description='testTitle1', 
                            main_description='tests endpoint', tab='tabTest', parameters=[simple_parameter], 
                            method="POST", responses=[simple_response])

simple_endpoint2 = Endpoint(link='https://api.example.com/users/99999', title_description='testTitle2', 
                            main_description='tests endpoint', tab='tabTest', parameters=[simple_parameter], 
                            method="POST", responses=[simple_response])

simple_endpoint3 = Endpoint(link='https://api.example.com/users/1111', title_description='testTitle3', 
                            main_description='tests', tab='tab', parameters=[simple_parameter], 
                            method="POST", responses=[simple_response])

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
        "displayname": "Tester 1",
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


def test_yaml(simple_user):
    '''
        Test YAML import
    '''
    file = {
        'file' : open('tests/resources/sample.yaml', 'rb')
    }
    response = client.post("/upload/yaml", file)
    
    print(response)