import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.classes import Service
from src.backend.app import app, register, add_service, login
from src.backend.classes.models import User, db, UserCreate, LoginModel, 
from src.backend.database import db_add_service

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
    db.services.delete_many({})

@pytest.fixture
def simple_filter(simple_user):
    clear_all()
    api1 = {
                'name' : 'Googl3',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API', 'Public']
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    
    api2 = {
            'name' : 'Googl2',
            'icon_url' : '',
            'x_start' : 0,
            'x_end' : 0,
            'y_start' : 0,
            'y_end' : 0,
            'description' : 'This is a test API',
            'tags' : ['API', 'Private']
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
    response_info = response.json 
    assert response_info == [api2]

def simple_filter_multiple(simple_user):
    clear_all()
    api1 = {
                'name' : 'Googl3',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API', 'Public']
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    
    api2 = {
            'name' : 'Googl2',
            'icon_url' : '',
            'x_start' : 0,
            'x_end' : 0,
            'y_start' : 0,
            'y_end' : 0,
            'description' : 'This is a test API',
            'tags' : ['API', 'Private']
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
    response_info = response.json 
    assert response_info == [api1, api2]

def filter_same_name(simple_user):
    clear_all()
    api1 = {
                'name' : 'Googl3',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API', 'Public']
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api1)
    
    api2 = {
            'name' : 'Googl3',
            'icon_url' : '',
            'x_start' : 0,
            'x_end' : 0,
            'y_start' : 0,
            'y_end' : 0,
            'description' : 'This is a test API',
            'tags' : ['API', 'Private']
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
    response_info = response.json 
    assert response_info == [api1, api2]

    def filter_non(simple_user):
        clear_all()
        api1 = {
                    'name' : 'Googl3',
                    'icon_url' : '',
                    'x_start' : 0,
                    'x_end' : 0,
                    'y_start' : 0,
                    'y_end' : 0,
                    'description' : 'This is a test API',
                    'tags' : ['API', 'Public']
                    }

        response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                            json=api1)
        
        api2 = {
                'name' : 'Googl2',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API', 'Private']
                }
        
        response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                            json=api2)

        response = client.get("/service/filter",
                            params={
                                'tags': ['testing1'],
                                'providers': []
                            })
        assert (response.status_code) == SUCCESS 
        response_info = response.json 
        assert response_info == []

