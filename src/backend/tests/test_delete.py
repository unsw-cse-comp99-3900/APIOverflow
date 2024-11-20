import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.app import app 
from src.backend.classes.models import db
from src.backend.classes.Endpoint import Endpoint
from src.backend.classes.Parameter import Parameter 
from src.backend.classes.Response import Response

# Create a test client
client = TestClient(app)

INPUT_ERROR = 400
MISSING_ERROR = 404
FORBIDDEN_ERROR = 403
SUCCESS = 200
AUTHENTICATION_ERROR = 401

# endpoint1
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

    usable_data = {"c_token" : None, "uid": None}

    response = client.post("/auth/register",
                            json=user_creds)
    assert response.status_code == SUCCESS
    usable_data['uid'] = response.json()['uid']

    # Log into account
    response = client.post("/auth/login",
                           json=user_creds)
    assert response.status_code == SUCCESS
    usable_data['c_token'] = response.json()['access_token']

    # Generate imposter
    user_creds = {
        "displayname": "Sus Imposter 6969",
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
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()]
                }
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {usable_data['c_token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    usable_data['sid'] = response.json()['id']

    yield usable_data
    clear_all()

def test_service_removed_user_delete(simple_user):

    data = simple_user
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]
    response = client.delete("/user/delete/me",
                headers={"Authorization": f"Bearer {data['c_token']}"})
    assert response.status_code == SUCCESS

    response = client.get("/service/get_service",
                headers={"Authorization": f"Bearer {access_token}"},
                params={
                            'sid' : data['sid']
                        })
    assert response.status_code == MISSING_ERROR

def test_review_removed_user_delete(simple_user):

    data = simple_user
    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'sid': data['sid']
    }
    response = client.get("/service/get/rating",
                          params=package)
    assert response.status_code == SUCCESS
    assert response.json()['rating'] == -1.00

    response = client.get("/service/get/reviews",
                          params={
                              'sid': data['sid'],
                              'testing': True
                          })
    assert response.status_code == SUCCESS
    print(response.json())
    assert len(response.json()['reviews']) == 1

    response = client.delete("/user/delete/me",
                headers={"Authorization": f"Bearer {data['u_token']}"})
    assert response.status_code == SUCCESS

    response = client.get("/service/get/reviews",
                          params={
                              'sid': data['sid'],
                              'testing': True
                          })
    assert response.status_code == SUCCESS
    print(response.json())
    assert len(response.json()['reviews']) == 0

    package = {
        'sid':data['sid']
    }
    response = client.get("/service/get/rating",
                          params=package)
    assert response.status_code == SUCCESS
    assert response.json()['rating'] == 0.00

def test_service_review_removed_user_delete(simple_user):
    '''
        Test whether upvoting a review works
    '''
    data = simple_user
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    rid = '0'
    response = client.get("/review/get",
                          params = {'rid': rid})
    assert response.status_code == SUCCESS
    assert response.json()['rid'] == rid
    assert response.json()['upvotes'] == 0
    assert response.json()['downvotes'] == 0

    package = {
        'rid': rid
    }
    response = client.post("/review/upvote",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    response = client.get("/review/get",
                          params = {'rid': rid})
    assert response.status_code == SUCCESS
    assert response.json()['rid'] == rid
    assert response.json()['upvotes'] == 1
    assert response.json()['downvotes'] == 0

    response = client.delete("/admin/delete/user", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : data['uid']
                            })
    assert response.status_code == SUCCESS

    response = client.get("/review/get",
                          params = {'rid': rid})
    assert response.status_code == MISSING_ERROR

def test_upvote_review_removed_user_delete(simple_user):
    '''
        Test whether upvoting a review works
    '''
    data = simple_user
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    rid = '0'
    response = client.get("/review/get",
                          params = {'rid': rid})
    assert response.status_code == SUCCESS
    assert response.json()['rid'] == rid
    assert response.json()['upvotes'] == 0
    assert response.json()['downvotes'] == 0

    response = client.post("/auth/register", json={
        "displayname": "guestuser",
        "username": "guestuser123",
        "password": "guestpassword",
        "email" : "doxxedddddd@gmail.com"
    })
    gid = response.json()['uid']
    response = client.post("/auth/login", json={
        "username": "guestuser123",
        "password": "guestpassword"
    })
    access_token_g = response.json()["access_token"]

    package = {
        'rid': rid
    }
    response = client.post("/review/upvote",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    response = client.post("/review/downvote",
                           headers={"Authorization": f"Bearer {access_token_g}"},
                           json=package)
    assert response.status_code == SUCCESS

    response = client.get("/review/get",
                          params = {'rid': rid})
    assert response.status_code == SUCCESS
    assert response.json()['rid'] == rid
    assert response.json()['upvotes'] == 1
    assert response.json()['downvotes'] == 1

    response = client.delete("/admin/delete/user", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : gid
                            })
    assert response.status_code == SUCCESS

    response = client.get("/review/get",
                          params = {'rid': rid})
    assert response.status_code == SUCCESS
    assert response.json()['rid'] == rid
    assert response.json()['upvotes'] == 1
    assert response.json()['downvotes'] == 0


