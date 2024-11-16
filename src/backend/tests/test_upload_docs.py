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
        Method to reset local databsed for new test
    '''
    response = client.post("/testing/clear")
    assert response.status_code == SUCCESS
    assert  response.json() == {"message" : "Clear Successful"}
    db.users.delete_many({})

@pytest.fixture
def two_users():
    '''
        Scenario with two users, general user and service-provider
    '''

    # Clear data
    clear_all()

    # Register users
    creator_creds = {
        "displayname": "Creator",
        "username" : "Creator",
        "password" : "password",
        "email" : "doxxed@gmail.com"
    }
    user_creds = {
        "displayname": "User",
        "username" : "User",
        "password" : "password",
        "email" : "doxxed2@gmail.com"
    }

    c_res = client.post("/auth/register",
                          json=creator_creds)
    u_res = client.post("/auth/register",
                          json=user_creds)

    assert c_res.status_code == SUCCESS
    assert u_res.status_code == SUCCESS

    # Login
    c_res = client.post("/auth/login",
                        json=creator_creds)
    u_res = client.post("/auth/login",
                        json=user_creds)
    
    assert c_res.status_code == SUCCESS
    assert u_res.status_code == SUCCESS

    # Usable data
    usable_data = {
        'creator': c_res.json()['access_token'],
        'user': u_res.json()['access_token']
    }

    # Create an API
    api_info = {
                'name' : 'Test API',
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.dict()]
                }
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {usable_data['creator']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    usable_data['sid'] = response.json()['id']

    yield usable_data

# Error Testing
def test_invalid_file(two_users):
    '''
        Test whether non-pdf files are caught
    '''
    data = two_users
    file = {
        'file' : open('tests/resources/default_icon.png', 'rb')
    }
    response = client.post("/upload/pdfs", files=file)
    assert response.status_code == INPUT_ERROR
 
    response = client.post("/upload/imgs", files=file)
    assert response.status_code == SUCCESS

    doc_id = response.json()['doc_id']
    api_data = {
        'sid': data['sid'],
        'doc_id': doc_id
    }
    response = client.post("/service/upload_docs",
                           headers={"Authorization": f"Bearer {data['creator']}"},
                           json=api_data)
    assert response.status_code == INPUT_ERROR


def test_no_file(two_users):
    '''
        Test whether no-file is caught
    '''
    data = two_users
    api_data = {
        'sid': data['sid'],
        'doc_id': 100
    }
    response = client.post("/service/upload_docs",
                           headers={"Authorization": f"Bearer {data['creator']}"},
                           json=api_data)
    assert response.status_code == 422

def test_no_service(two_users):
    '''
        Test whether uploading to non-existent service is caught
    '''
    data = two_users
    filename = 'git_guide.pdf'
    file = {
        'file' : (filename, open("tests/resources/git_guide.pdf", 'rb'))
    }
    response = client.post("/upload/pdfs",
                           files=file)
    assert response.status_code == SUCCESS
 
    doc_id = response.json()['doc_id']
    api_data = {
        'sid': data['sid'] + '9999',
        'doc_id': doc_id
    }
    response = client.post("/service/upload_docs",
                           headers={"Authorization": f"Bearer {data['creator']}"},
                           json=api_data)
    assert response.status_code == MISSING_ERROR

def test_no_perms(two_users):
    '''
        Test whether uploading as non-owner is caught
    '''
    data = two_users
    filename = 'git_guide.pdf'
    file = {
        'file' : (filename, open("tests/resources/git_guide.pdf", 'rb'))
    }
    response = client.post("/upload/pdfs",
                           files=file)
    assert response.status_code == SUCCESS
 
    doc_id = response.json()['doc_id']
    api_data = {
        'sid': data['sid'],
        'doc_id': doc_id
    }
    response = client.post("/service/upload_docs",
                           headers={"Authorization": f"Bearer {data['user']}"},
                           json=api_data)
    assert response.status_code == FORBIDDEN_ERROR


# Success Cases (Cannot be tested)
def test_successful_upload(two_users):
    '''
        Test whether upload is successful
    '''
    data = two_users
    filename = 'git_guide.pdf'
    file = {
        'file' : (filename, open("tests/resources/git_guide.pdf", 'rb'))
    }
    response = client.post("/upload/pdfs", files=file)
    assert response.status_code == SUCCESS
 
    doc_id = response.json()['doc_id']
    api_data = {
        'sid': data['sid'],
        'doc_id': doc_id
    }
    response = client.post("/service/upload_docs",
                           headers={"Authorization": f"Bearer {data['creator']}"},
                           json=api_data)
    assert response.status_code == SUCCESS

    response = client.get("/service/get_service",
                          params={
                              'sid': data['sid']
                          })
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info["versions"][0]['docs'] == ["1"]