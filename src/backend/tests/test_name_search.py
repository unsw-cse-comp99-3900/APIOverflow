import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.classes import Service
from src.backend.app import app, register, add_service, login
from src.backend.classes.models import User, db, UserCreate, LoginModel
from src.backend.classes.Endpoint import Endpoint
from src.backend.classes.Parameter import Parameter 
from src.backend.classes.Response import Response

# Create a test client
client = TestClient(app)

INPUT_ERROR = 400
AUTHENTICATION_ERROR = 401
SUCCESS = 200

# test endpoint
simple_parameter = Parameter(id="1", endpoint_link='https://api.example.com/users/12345', required=True, 
                            type='HEADER', name='paramtest', value_type='int')
simple_response = Response(code='404', description='not found', conditions=["site is down", "badtest"], 
                            example="example...")
simple_endpoint = Endpoint(link='https://api.example.com/users/12345', title_description='testTitle1', 
                            main_description='tests endpoint', tab='tabTest', parameters=[simple_parameter], 
                            method="POST", responses=[simple_response])

def clear_all():
    ''' 
        Method to reset local database for new test
    '''
    response = client.post("/testing/clear")
    assert response.status_code == SUCCESS
    assert  response.json() == {"message" : "Clear Successful"}

@pytest.fixture
def simple_user():
    '''
        Simulates a simple user registering their account then logging in
    '''
    # Clear data abse
    clear_all()

    # Register user
    user_creds = {
        "displayname": "Tester 1",
        "username" : "Tester 1",
        "password" : "password",
        "email" : "doxxed@gmail.com"
    }

    usable_data = {"token" : None, "uid": None}

    response = client.post("/auth/register",
                            json=user_creds)
    assert response.status_code == SUCCESS
    usable_data['uid'] = response.json()['uid']

    # Log into account
    response = client.post("/auth/login",
                           json=user_creds)
    assert response.status_code == SUCCESS
    usable_data['token'] = response.json()['access_token']

    return usable_data

def test_simple_search(simple_user):
    api1 = {
        'name' : 'Google',
        'description' : 'This is a test API',
        'tags' : ['API', 'Public'],
        'endpoints': [simple_endpoint.dict()]
        }
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    api2 = {
            'name' : 'Googooww',
            'description' : 'This is a test API',
            'tags' : ['API', 'Private'],
            'endpoints': [simple_endpoint.dict()]
            }
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api2)

    response = client.get("/service/search",
                          params={
                              'name': "Google",
                              'hide_pending': False
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    assert any(api['name'] == api1['name'] for api in response_info)

def test_simple_search_2(simple_user):
    api1 = {
        'name' : 'Google',
        'description' : 'This is a test API',
        'tags' : ['API', 'Public'],
        'endpoints': [simple_endpoint.dict()]
        }
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    api2 = {
            'name' : 'Googooww',
            'description' : 'This is a test API',
            'tags' : ['API', 'Private'],
            'endpoints': [simple_endpoint.dict()]
            }
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api2)

    response = client.get("/service/search",
                          params={
                              'name': "Goog",
                              'hide_pending': False
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    assert any(api['name'] == api1['name'] for api in response_info)
    assert any(api['name'] == api2['name'] for api in response_info)

def test_simple_empty(simple_user):
    api1 = {
        'name' : 'Google',
        'description' : 'This is a test API',
        'tags' : ['API', 'Public'],
        'endpoints': [simple_endpoint.dict()]
        }
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    api2 = {
            'name' : 'Googooww',
            'description' : 'This is a test API',
            'tags' : ['API', 'Private'],
            'endpoints': [simple_endpoint.dict()]
            }
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api2)

    response = client.get("/service/search",
                          params={
                              'name': "dwae",
                              'hide_pending': False
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    assert len(response_info) == 0

def test_simple_regex_search(simple_user):
    api1 = {
        'name' : 'Google',
        'description' : 'This is a test API',
        'tags' : ['API', 'Public'],
        'endpoints': [simple_endpoint.dict()]
        }
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    api2 = {
            'name' : 'Googooww',
            'description' : 'This is a test API',
            'tags' : ['API', 'Private'],
            'endpoints': [simple_endpoint.dict()]
            }
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api2)

    response = client.get("/service/search",
                          params={
                              'name': "og",
                              'hide_pending': False
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    assert any(api['name'] == api1['name'] for api in response_info)
    assert any(api['name'] == api2['name'] for api in response_info)

def test_simple_regex_sensitivity(simple_user):
    api1 = {
        'name' : 'Google',
        'description' : 'This is a test API',
        'tags' : ['API', 'Public'],
        'endpoints': [simple_endpoint.dict()]
        }
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    api2 = {
            'name' : 'Googooww',
            'description' : 'This is a test API',
            'tags' : ['API', 'Private'],
            'endpoints': [simple_endpoint.dict()]
            }
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api2)

    response = client.get("/service/search",
                          params={
                              'name': "LE",
                              'hide_pending': False
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    assert any(api['name'] == api1['name'] for api in response_info)