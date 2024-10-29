import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.classes import Service
from src.backend.app import app
from src.backend.classes.models import User
from src.backend.classes.datastore import DEFAULT_TAGS


# Create a test client
client = TestClient(app)

INPUT_ERROR = 400
AUTHENTICATION_ERROR = 401
SUCCESS = 200
NOT_FOUND = 404
UNAUTHORISED_ERROR = 403

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

@pytest.fixture
def admin_user():
    '''
        Simulates an admin user registering their account then logging in
    '''
    # Clear database
    clear_all()

    # Register user
    user_creds = {
        "username" : "Tester 1",
        "password" : "password",
        "email" : "doxxed@gmail.com",
        "is_admin" : True
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

# Error testing
def test_no_login(simple_user):
    '''
        Test that a guest user cannot add a tag
    '''
    response = client.post("/tag/add",
                           headers={"Authorization": "Bearer"},
                           json={
                               'tag': ''
                           })
    
    assert response.status_code == AUTHENTICATION_ERROR

def test_no_tag(simple_user):
    '''
        Test whether an empty tag is caught
    '''
    response = client.post("/tag/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                               'tag' : ''
                           })
    assert response.status_code == INPUT_ERROR

def test_add_tag(simple_user):
    '''
        Test that user can add a tag
    '''
    response = client.post("/tag/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'tag' : 'testing'
                           })
    assert response.status_code == SUCCESS

    response = client.get("/tags/get",
                          params={})
    assert 'testing' in response.json()['tags']

def test_duplicate_tags(simple_user):
    '''
        Test that a duplicate tag cannot be added
    '''
    response = client.post("/tag/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'tag' : 'testing'
                           })
    assert response.status_code == SUCCESS

    response = client.post("/tag/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'tag' : 'testing'
                           })
    assert response.status_code == INPUT_ERROR

def test_get_tags(simple_user):
    '''
        Test whether default tags are retrieved
    '''
    response = client.get('/tags/get',
                           params={})
    assert response.json()['tags'] == DEFAULT_TAGS

def test_delete_tag_guest(admin_user):
    '''
        Test whether a guest user is rejected from tag deletion
    '''
    response = client.delete('/tag/delete',
                             headers={"Authorization":'Bearer'},
                             params={
                                 'tag': ''
                             })
    assert response.status_code == AUTHENTICATION_ERROR

def test_delete_tag_general_user(simple_user):
    '''
        Test whether a general user is rejected from tag deletion
    '''
    response = client.delete('/tag/delete',
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           params={
                                'tag' : ''
                           })
    assert response.status_code == UNAUTHORISED_ERROR

def test_delete_tag_nonexistent(admin_user):
    '''
        Test deleting a non existent tag
    '''
    response = client.delete('/tag/delete',
                           headers={"Authorization": f"Bearer {admin_user['token']}"},
                           params={
                                'tag' : '123'
                           })
    assert response.status_code == NOT_FOUND

def test_delete_default_tag(admin_user):
    '''
        Test rejection of deleting a system tag (DEFAULT_TAGS)
    '''
    response = client.delete('/tag/delete',
                           headers={"Authorization": f"Bearer {admin_user['token']}"},
                           params={
                                'tag' : DEFAULT_TAGS[0]
                           })
    assert response.status_code == INPUT_ERROR

def test_delete_tag_success(admin_user):
    '''
        Test deletion of custom tag
    '''
    response = client.post("/tag/add",
                           headers={"Authorization": f"Bearer {admin_user['token']}"},
                           json={
                                'tag' : 'testing'
                           })
    assert response.status_code == SUCCESS

    response = client.delete('/tag/delete',
                           headers={"Authorization": f"Bearer {admin_user['token']}"},
                           params={
                                'tag' : 'testing'
                           })
    assert response.status_code == SUCCESS

    response = client.get("/tags/get",
                          params={})
    assert 'testing' not in response.json()['tags']