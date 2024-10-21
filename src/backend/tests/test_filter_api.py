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

def test_simple_filter(simple_user):
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Googl3',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : 'This is a test API',
                                'tags' : ['API', 'Public'],
                                'endpoint': 'https://api.example.com/users/12345'
                           })
    api2 = {
            'name' : 'Googl2',
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

    response = client.get("/service/filter",
                          params={
                              'tags': ['Private'],
                              'providers': []
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    print(response_info)
    assert response_info[0]['name'] == api2['name']
    assert response_info[0]['tags'] == api2['tags']

def test_simple_filter_multiple(simple_user):
    api = {
            'name' : 'Googl2',
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
                           json=api)
    
    response = client.post("/service/add",
                                headers={"Authorization": f"Bearer {simple_user['token']}"},
                            json={
                                    'name' : 'Googl3',
                                    'icon_url' : '',
                                    'x_start' : 0,
                                    'x_end' : 0,
                                    'y_start' : 0,
                                    'y_end' : 0,
                                    'description' : 'This is a test API',
                                    'tags' : ['API', 'Public'],
                                    'endpoint': 'https://api.example.com/users/12345'
                            })
    api2 = {
            'name' : 'Googl2',
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
                        json=api2)

    response = client.get("/service/filter",
                          params={
                              'tags': ['API'],
                              'providers': []
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    found1 = False
    found2 = False
    found3 = False
    for api in response_info:
        if "Googl3" == api['name'] and ['API', 'Public'] == api['tags']:
            found1 = True 
        if "Googl2" == api['name'] and ['API', 'Private'] == api['tags']:
            found2 = True
        if "Googl2" == api['name'] and ['API'] == api['tags']:
            found3 = True
    assert found1 and found2 and found3

def test_providers(simple_user):
    api = {
            'name' : 'Googl2',
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
                           json=api)
    
    response = client.post("/service/add",
                                headers={"Authorization": f"Bearer {simple_user['token']}"},
                            json={
                                    'name' : 'Googl3',
                                    'icon_url' : '',
                                    'x_start' : 0,
                                    'x_end' : 0,
                                    'y_start' : 0,
                                    'y_end' : 0,
                                    'description' : 'This is a test API',
                                    'tags' : ['API', 'Public'],
                                    'endpoint': 'https://api.example.com/users/12345'
                            })
    api2 = {
            'name' : 'Googl2',
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
                        json=api2)

    response = client.get("/service/filter",
                          params={
                              'tags': [],
                              'providers': [simple_user['uid']]
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    found1 = False
    found2 = False
    found3 = False
    for api in response_info:
        if "Googl3" == api['name'] and ['API', 'Public'] == api['tags']:
            found1 = True 
        if "Googl2" == api['name'] and ['API', 'Private'] == api['tags']:
            found2 = True
        if "Googl2" == api['name'] and ['API'] == api['tags']:
            found3 = True
    assert found1 and found2 and found3

def test_providers_with_tags(simple_user):
    api = {
            'name' : 'Googl2',
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
                           json=api)
    
    response = client.post("/service/add",
                                headers={"Authorization": f"Bearer {simple_user['token']}"},
                            json={
                                    'name' : 'Googl3',
                                    'icon_url' : '',
                                    'x_start' : 0,
                                    'x_end' : 0,
                                    'y_start' : 0,
                                    'y_end' : 0,
                                    'description' : 'This is a test API',
                                    'tags' : ['API', 'Public'],
                                    'endpoint': 'https://api.example.com/users/12345'
                            })
    api2 = {
            'name' : 'Googl2',
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
                        json=api2)

    response = client.get("/service/filter",
                          params={
                              'tags': ['Private'],
                              'providers': [simple_user['uid']]
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    found1 = False
    found2 = False
    found3 = False
    for api in response_info:
        if "Googl3" == api['name'] and ['API', 'Public'] == api['tags']:
            found1 = True 
        if "Googl2" == api['name'] and ['API', 'Private'] == api['tags']:
            found2 = True
        if "Googl2" == api['name'] and ['API'] == api['tags']:
            found3 = True
    assert not found1 and found2 and not found3

def test_invalid_providers(simple_user):
    api = {
            'name' : 'Googl2',
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
                           json=api)
    
    response = client.post("/service/add",
                                headers={"Authorization": f"Bearer {simple_user['token']}"},
                            json={
                                    'name' : 'Googl3',
                                    'icon_url' : '',
                                    'x_start' : 0,
                                    'x_end' : 0,
                                    'y_start' : 0,
                                    'y_end' : 0,
                                    'description' : 'This is a test API',
                                    'tags' : ['API', 'Public'],
                                    'endpoint': 'https://api.example.com/users/12345'
                            })
    api2 = {
            'name' : 'Googl2',
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
                        json=api2)

    response = client.get("/service/filter",
                          params={
                              'tags': ['Private'],
                              'providers': ['5']
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    found1 = False
    found2 = False
    found3 = False
    for api in response_info:
        if "Googl3" == api['name'] and ['API', 'Public'] == api['tags']:
            found1 = True 
        if "Googl2" == api['name'] and ['API', 'Private'] == api['tags']:
            found2 = True
        if "Googl2" == api['name'] and ['API'] == api['tags']:
            found3 = True
    assert not found1 and not found2 and not found3

def test_providers_with_tags2(simple_user):
    api = {
            'name' : 'Googl2',
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
                           json=api)
    
    response = client.post("/service/add",
                                headers={"Authorization": f"Bearer {simple_user['token']}"},
                            json={
                                    'name' : 'Googl3',
                                    'icon_url' : '',
                                    'x_start' : 0,
                                    'x_end' : 0,
                                    'y_start' : 0,
                                    'y_end' : 0,
                                    'description' : 'This is a test API',
                                    'tags' : ['API', 'Public'],
                                    'endpoint': 'https://api.example.com/users/12345'
                            })
    api2 = {
            'name' : 'Googl2',
            'icon_url' : '',
            'x_start' : 0,
            'x_end' : 0,
            'y_start' : 0,
            'y_end' : 0,
            'description' : 'This is a test API',
            'tags' : ['NOT API'],
            'endpoint': 'https://api.example.com/users/12345'
            }
    response = client.post("/service/add",
                        headers={"Authorization": f"Bearer {simple_user['token']}"},
                        json=api2)

    response = client.get("/service/filter",
                          params={
                              'tags': ['API'],
                              'providers': [simple_user['uid']]
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    found1 = False
    found2 = False
    found3 = False
    for api in response_info:
        if "Googl3" == api['name'] and ['API', 'Public'] == api['tags']:
            found1 = True 
        if "Googl2" == api['name'] and ['API', 'Private'] == api['tags']:
            found2 = True
        if "Googl2" == api['name'] and ['NOT API'] == api['tags']:
            found3 = True
    assert found1 and found2 and not found3

def test_providers_with_tags_multiple(simple_user):

    user_creds = {
        "username" : "Tester 2",
        "password" : "passwordsad",
        "email" : "doxxed2@gmail.com"
    }

    usable_data2 = {"token" : None}

    response = client.post("/auth/register",
                            json=user_creds)
    assert response.status_code == SUCCESS
    user2_id = response.json()['uid']
    # Log into account
    response = client.post("/auth/login",
                           json=user_creds)
    assert response.status_code == SUCCESS
    usable_data2['token'] = response.json()['access_token']

    api = {
            'name' : 'Googl2',
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
                           json=api)
    
    response = client.post("/service/add",
                                headers={"Authorization": f"Bearer {usable_data2['token']}"},
                            json={
                                    'name' : 'Googl3',
                                    'icon_url' : '',
                                    'x_start' : 0,
                                    'x_end' : 0,
                                    'y_start' : 0,
                                    'y_end' : 0,
                                    'description' : 'This is a test API',
                                    'tags' : ['API', 'Public'],
                                    'endpoint': 'https://api.example.com/users/12345'
                            })
    api2 = {
            'name' : 'Googl2',
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
                        json=api2)

    response = client.get("/service/filter",
                          params={
                              'tags': ['API'],
                              'providers': [simple_user['uid'], user2_id]
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    found1 = False
    found2 = False
    found3 = False

    #api1 is simple user
    #api2 is user2
    #api3 is simple user

    for api in response_info:
        if "Googl3" == api['name'] and ['API', 'Public'] == api['tags']:
            found1 = True 
        if "Googl2" == api['name'] and ['API', 'Private'] == api['tags']:
            found2 = True
        if "Googl2" == api['name'] and ['API'] == api['tags']:
            found3 = True
    assert found1 and found2 and found3

def test_providers_with_tags_multiple2(simple_user):

    user_creds = {
        "username" : "Tester 2",
        "password" : "passwordsad",
        "email" : "doxxed2@gmail.com"
    }

    usable_data2 = {"token" : None}

    response = client.post("/auth/register",
                            json=user_creds)
    assert response.status_code == SUCCESS

    # Log into account
    response = client.post("/auth/login",
                           json=user_creds)
    assert response.status_code == SUCCESS
    usable_data2['token'] = response.json()['access_token']

    api = {
            'name' : 'Googl2',
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
                           json=api)
    
    response = client.post("/service/add",
                                headers={"Authorization": f"Bearer {usable_data2['token']}"},
                            json={
                                    'name' : 'Googl3',
                                    'icon_url' : '',
                                    'x_start' : 0,
                                    'x_end' : 0,
                                    'y_start' : 0,
                                    'y_end' : 0,
                                    'description' : 'This is a test API',
                                    'tags' : ['NOT API', 'Public'],
                                    'endpoint': 'https://api.example.com/users/12345'
                            })
    api2 = {
            'name' : 'Googl2',
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
                        json=api2)

    response = client.get("/service/filter",
                          params={
                              'tags': ['NOT API'],
                              'providers': [simple_user['uid']]
                          })
    assert (response.status_code) == SUCCESS 
    response_info = response.json()
    found1 = False
    found2 = False
    found3 = False

    #api1 is simple user
    #api2 is user2
    #api3 is simple user

    for api in response_info:
        if "Googl3" == api['name'] and ['API', 'Public'] == api['tags']:
            found1 = True 
        if "Googl2" == api['name'] and ['NOT API', 'Private'] == api['tags']:
            found2 = True
        if "Googl2" == api['name'] and ['API'] == api['tags']:
            found3 = True
    assert not found1 and not found2 and not found3