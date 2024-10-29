import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.classes import Service
from src.backend.app import app, register, add_service, login
from src.backend.classes.models import User, db, UserCreate, LoginModel

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
        'icon_url' : '',
        'x_start' : 0,
        'x_end' : 0,
        'y_start' : 0,
        'y_end' : 0,
        'description' : 'This is a test API',
        'tags' : ['API', 'Public'],
        'endpoint': 'https://api.example.com/users/12345'
        }
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    api2 = {
            'name' : 'Googooww',
            'icon_url' : '',
            'x_start' : 0,
            'x_end' : 0,
            'y_start' : 0,
            'y_end' : 0,
            'description' : 'This is a test API',
            'tags' : ['API', 'Private'],
            'endpoint': 'https://api.example.com/users/12345'
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
    print(response_info)
    assert response_info[0]['_name'] == api1['name']
    assert response_info[0]['_tags'] == api1['tags']

def test_simple_search_2(simple_user):
    api1 = {
        'name' : 'Google',
        'icon_url' : '',
        'x_start' : 0,
        'x_end' : 0,
        'y_start' : 0,
        'y_end' : 0,
        'description' : 'This is a test API',
        'tags' : ['API', 'Public'],
        'endpoint': 'https://api.example.com/users/12345'
        }
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    api2 = {
            'name' : 'Googooww',
            'icon_url' : '',
            'x_start' : 0,
            'x_end' : 0,
            'y_start' : 0,
            'y_end' : 0,
            'description' : 'This is a test API',
            'tags' : ['API', 'Private'],
            'endpoint': 'https://api.example.com/users/12345'
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
    print(response_info)
    assert response_info[0]['_name'] == api1['name']
    assert response_info[0]['_tags'] == api1['tags']
    assert response_info[1]['_name'] == api2['name']
    assert response_info[1]['_tags'] == api2['tags']

def test_simple_empty(simple_user):
    api1 = {
        'name' : 'Google',
        'icon_url' : '',
        'x_start' : 0,
        'x_end' : 0,
        'y_start' : 0,
        'y_end' : 0,
        'description' : 'This is a test API',
        'tags' : ['API', 'Public'],
        'endpoint': 'https://api.example.com/users/12345'
        }
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    api2 = {
            'name' : 'Googooww',
            'icon_url' : '',
            'x_start' : 0,
            'x_end' : 0,
            'y_start' : 0,
            'y_end' : 0,
            'description' : 'This is a test API',
            'tags' : ['API', 'Private'],
            'endpoint': 'https://api.example.com/users/12345'
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
    print(response_info)
    assert len(response_info) == 0

def test_simple_regex_search(simple_user):
    api1 = {
        'name' : 'Google',
        'icon_url' : '',
        'x_start' : 0,
        'x_end' : 0,
        'y_start' : 0,
        'y_end' : 0,
        'description' : 'This is a test API',
        'tags' : ['API', 'Public'],
        'endpoint': 'https://api.example.com/users/12345'
        }
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    api2 = {
            'name' : 'Googooww',
            'icon_url' : '',
            'x_start' : 0,
            'x_end' : 0,
            'y_start' : 0,
            'y_end' : 0,
            'description' : 'This is a test API',
            'tags' : ['API', 'Private'],
            'endpoint': 'https://api.example.com/users/12345'
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
    print(response_info)
    assert response_info[0]['_name'] == api1['name']
    assert response_info[0]['_tags'] == api1['tags']
    assert response_info[1]['_name'] == api2['name']
    assert response_info[1]['_tags'] == api2['tags']

def test_simple_regex_sensitivity(simple_user):
    api1 = {
        'name' : 'Google',
        'icon_url' : '',
        'x_start' : 0,
        'x_end' : 0,
        'y_start' : 0,
        'y_end' : 0,
        'description' : 'This is a test API',
        'tags' : ['API', 'Public'],
        'endpoint': 'https://api.example.com/users/12345'
        }
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    api2 = {
            'name' : 'Googooww',
            'icon_url' : '',
            'x_start' : 0,
            'x_end' : 0,
            'y_start' : 0,
            'y_end' : 0,
            'description' : 'This is a test API',
            'tags' : ['API', 'Private'],
            'endpoint': 'https://api.example.com/users/12345'
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
    print(response_info)
    assert response_info[0]['_name'] == api1['name']
    assert response_info[0]['_tags'] == api1['tags']