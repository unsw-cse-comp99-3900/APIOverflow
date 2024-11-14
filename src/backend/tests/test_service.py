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

# Error testing
def test_invalid_user(simple_user):
    '''
        Test that add_service is only usable by users not guests
    '''
    response = client.post("/service/add",
                           headers={"Authorization": "Bearer"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : '',
                                'tags' : [],
                                'endpoints': []
                           })
    assert response.status_code == AUTHENTICATION_ERROR


def test_no_name(simple_user):
    '''
        Test whether no name is caught
    '''
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                            json={
                                'name' : '',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : '',
                                'tags' : [],
                                'endpoints': []
                           })
    assert response.status_code == INPUT_ERROR

def test_invalid_url(simple_user):
    '''
        Test whether bad url (www.googlefake.xyzabsdh) is caught
    '''
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : 'www.googlefake.xyzabsdh',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : 'hi',
                                'tags' : ['API'],
                                'endpoints': []
                           })
    assert response.status_code == INPUT_ERROR

def test_invalid_dimensions(simple_user):
    '''
        Test whether combinations of bad dimensions are caught
    '''
    # Negative x-start
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : -10,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : 'hi',
                                'tags' : ['API'],
                                'endpoints': []
                           })
    assert response.status_code == INPUT_ERROR

    # x-start bigger than x-end
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 1000,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : 'hi',
                                'tags' : ['API'],
                                'endpoints': []
                           })
    assert response.status_code == INPUT_ERROR

    # Negative y-start
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : -10,
                                'y_end' : 0,
                                'description' : 'hi',
                                'tags' : ['API'],
                                'endpoints': []
                           })
    assert response.status_code == INPUT_ERROR

    # Bigger y-start than y-end
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 1000,
                                'y_end' : 0,
                                'description' : 'hi',
                                'tags' : ['API'],
                                'endpoints': []
                           })
    assert response.status_code == INPUT_ERROR

def test_no_description(simple_user):
    '''
        Test whether no description given is caught
    '''
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : '',
                                'tags' : [],
                                'endpoints': []
                           })
    assert response.status_code == INPUT_ERROR

def test_no_tags(simple_user):
    '''
        Test whether no description given is caught
    '''
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : 'This is a test API',
                                'tags' : [],
                                'endpoints': []
                           })
    assert response.status_code == INPUT_ERROR

def test_no_endpoint(simple_user):
    '''
        Test whether no description given is caught
    '''
    response = client.post("/service/add",
                            headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json={
                                'name' : 'Test API',
                                'icon_url' : '',
                                'x_start' : 0,
                                'x_end' : 0,
                                'y_start' : 0,
                                'y_end' : 0,
                                'description' : 'This is a test API',
                                'tags' : ['API'],
                                'endpoints': []
                           })
    assert response.status_code == INPUT_ERROR

# Valid instances
def test_create_api(simple_user):
    '''
        Test whether an API is correctly created
    '''
    api_info = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()]
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']
    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info['id'] == sid
    assert response_info['name'] == api_info['name']
    assert response_info['description'] == api_info['description']
    assert response_info['tags'] == api_info['tags']
    assert response_info["versions"][0]["endpoints"] == api_info["endpoints"]

    database_object = db_get_service(sid)
    assert database_object['id'] == sid
    assert database_object['name'] == api_info['name']
    assert database_object['description'] == api_info['description']
    assert database_object['tags'] == api_info['tags']
    assert database_object["versions"][0]["endpoints"] == api_info["endpoints"]

def test_multiple_tags(simple_user):
    '''
        Test whether an API is correctly created where it has multiple tags
    '''
    api_info = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API', 'Public', 'In Development'],
                'endpoints': [simple_endpoint.model_dump()]
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info['id'] == sid
    assert response_info['name'] == api_info['name']
    assert response_info['description'] == api_info['description']
    assert response_info['tags'] == api_info['tags']
    assert response_info["versions"][0]["endpoints"] == api_info["endpoints"]
    assert response_info['icon_url'] == ''

def test_custom_icon(simple_user):
    '''
        Test whether create can handle custom icon_url:
            http://cdn.mos.cms.futurecdn.net/iC7HBvohbJqExqvbKcV3pP.jpg
    '''
    api_info = {
                'name' : 'Fake Google',
                'icon_url': 'http://cdn.mos.cms.futurecdn.net/iC7HBvohbJqExqvbKcV3pP.jpg',
                'x_start' : 0,
                'x_end' : 100,
                'y_start' : 0,
                'y_end' : 100,
                'description' : 'This is a definitely... Google',
                'tags' : ['API', 'Public', 'In Development'],
                'endpoints': [simple_endpoint.model_dump()]
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']
    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'token' : simple_user['token'],
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info['id'] == sid
    assert response_info['name'] == api_info['name']
    assert response_info['description'] == api_info['description']
    assert response_info['tags'] == api_info['tags']
    assert response_info["versions"][0]["endpoints"] == api_info["endpoints"]

def test_update_api_invalid_sid(simple_user):
    '''
        Tests error received when sid is not valid
    '''

    api_info = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()]
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS

    update_request_info = {
        'sid' : "invalid id",
        'name' : 'new name',
        'description' : 'new name',
        'tags' : ['new', 'name'],
        'endpoints': [simple_endpoint.model_dump()]
    }

    response = client.post("/service/update",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=update_request_info)
    assert response.status_code == 404

def test_update_api_documents(simple_user):
    '''
        Test whether an API is correctly created then updated
    '''
    api_info = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()]
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']

    filename = 'git_guide.pdf'
    file = {
        'file' : (filename, open("tests/resources/git_guide.pdf", 'rb'))
    }
    response = client.post("/upload/pdfs", files=file)
    assert response.status_code == SUCCESS
 
    doc_id = response.json()['doc_id']
    api_data = {
        'sid': sid,
        'doc_id': doc_id
    }
    response = client.post("/service/upload_docs",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_data)
    assert response.status_code == SUCCESS
    
    response = client.get("/service/get_service",
                        params={
                            'sid': sid
                        })
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info["versions"][0]['docs'] == ["1"]
    database_object = db_get_service(sid)

    # path of file is accessible via get_service but internally
    # stored by document id instead of path
    assert database_object["versions"][0]['docs'] == [doc_id]

    update_request_info = {
        'sid' : sid,
        'name' : 'new name',
        'description' : 'new description',
        'tags' : ['new', 'tag'],
        'endpoints': [simple_endpoint.model_dump()]
    }

    response = client.post("/service/update",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=update_request_info)
    assert response.status_code == SUCCESS
    
    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
   
    assert response_info["versions"][0]['docs'] == ["1"]
    database_object = db_get_service(sid)
    assert database_object["versions"][0]['docs'] == [doc_id]

# Delete non-existing service
def test_delete_non_api(simple_user):
    '''
        Test whether an delete a fake service works
    '''
    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info == []

    response = client.delete("/service/delete",
                        headers={"Authorization": f"Bearer {simple_user['token']}"},
                        params={
                              'sid' : 'what'
                          })
    assert response.status_code == NOT_FOUND

# Delete instances
def test_delete_api(simple_user):
    '''
        Test whether delete an API works
    '''
    api_info1 = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()]
                }
    
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info1)
    assert response.status_code == SUCCESS
    sid = response.json()['id']

    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()[0]
    assert response_info != {}

    assert db_get_service(sid) is not None

    response = client.delete("/service/delete",
                        headers={"Authorization": f"Bearer {simple_user['token']}"},
                        params={
                              'sid' : sid
                          })
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info["name"] == api_info1['name']
    assert response_info["deleted"] == True
    assert db_get_service(sid) is None

    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info == []

def test_delete_apis(simple_user):
    '''
        Test whether delete an API with out of multiple APIs work
    '''
    api_info1 = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()]
                }
    
    api_info2 = {
                'name' : 'Test API I',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()]
                }
    
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info1)
    assert response.status_code == SUCCESS
    sid1 = response.json()['id']

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info2)
    assert response.status_code == SUCCESS
    sid2 = response.json()['id']

    response = client.delete("/service/delete",
                        headers={"Authorization": f"Bearer {simple_user['token']}"},
                        params={
                              'sid' : sid1
                          })
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info["name"] == api_info1['name']
    assert response_info["deleted"] == True

    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()[0]
    assert response_info['id'] == sid2
    assert response_info['name'] == api_info2['name']
    assert response_info['description'] == api_info2['description']
    assert response_info['tags'] == api_info2['tags']

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid1
                          })
    assert response.status_code == NOT_FOUND

    response = client.delete("/service/delete",
                        headers={"Authorization": f"Bearer {simple_user['token']}"},
                        params={
                              'sid' : sid2
                          })
    assert response.status_code == SUCCESS

    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info == []


# Valid instances
def test_get_apis(simple_user):
    '''
        Test whether an API is correctly get
    '''
    api_info1 = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()]
                }
    
    api_info2 = {
                'name' : 'Test API I',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()]
                }
    
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info1)
    assert response.status_code == SUCCESS
    sid1 = response.json()['id']

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info2)
    assert response.status_code == SUCCESS
    sid2 = response.json()['id']

    response = client.get("/service/my_services",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()[0]
    assert response_info['id'] == sid1
    assert response_info['name'] == api_info1['name']
    assert response_info['description'] == api_info1['description']
    assert response_info['tags'] == api_info1['tags']

    response_info = response.json()[1]
    assert response_info['id'] == sid2
    assert response_info['name'] == api_info2['name']
    assert response_info['description'] == api_info2['description']
    assert response_info['tags'] == api_info2['tags']


def test_admin_get_pending_services(simple_user):
    api_info = {
                'name' : 'Test API 1',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API 1',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()],
                "version_name": "some name",
                "version_description": "some description"
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]

    response = client.get("/admin/get/services",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 1
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 0

    new_global_service = response_info["new_services"][0]
    new_version_service = new_global_service["version_fields"]
    
    assert new_global_service['id'] == sid
    assert new_global_service['name'] == api_info['name']
    assert new_global_service['description'] == api_info['description']
    assert new_global_service['tags'] == api_info['tags']

    assert new_version_service['endpoints'] == api_info["endpoints"]
    assert new_version_service['version_name'] == api_info["version_name"]
    assert new_version_service['version_description'] == api_info["version_description"]

def test_admin_approve(simple_user):
    api_info = {
                'name' : 'Test API 1',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API 1',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()],
                'version_name': "some_version_name"
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]
    reason = 'very pog service'

    response = client.get("/admin/get/services",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 1
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 0

    client.post("/admin/service/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'sid': sid,
                                'reason': reason,
                                'approved': True,
                                'version_name': api_info["version_name"],
                                'service_global': True
                            })
    assert response.status_code == SUCCESS

    response = client.get("/service/filter",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                          })
    assert response.status_code == SUCCESS
    response_info = response.json()

    assert response_info[0]['id'] == sid
    assert response_info[0]['name'] == api_info['name']
    assert response_info[0]['description'] == api_info['description']
    assert response_info[0]['tags'] == api_info['tags']

    response = client.get("/service/get_service",
                        headers={"Authorization": f"Bearer {simple_user['token']}"},
                        params={
                            'token' : simple_user['token'],
                            'sid' : sid
                        })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info['status'] == "LIVE"
    assert response_info['status_reason'] == reason

    response = client.get("/admin/get/services",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 0
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 0


def test_admin_disapprove(simple_user):
    api_info = {
                'name' : 'Test API 1',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API 1',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()],
                'version_name': "some_version_name"
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]
    reason = 'very unpog service'

    response = client.get("/admin/get/services",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS
    response_info = response.json()
    
    assert len(response_info["new_services"]) == 1
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 0

    client.post("/admin/service/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'sid': sid,
                                'reason': reason,
                                'approved': False,
                                'version_name': api_info["version_name"],
                                'service_global': True
                            })

    response = client.get("/admin/get/services",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS
    response_info = response.json()
    
    assert len(response_info["new_services"]) == 0
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 0

    response = client.get("/service/filter",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                          })
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert len(response_info) == 0

    response = client.get("/service/get_service",
                        headers={"Authorization": f"Bearer {simple_user['token']}"},
                        params={
                            'token' : simple_user['token'],
                            'sid' : sid
                        })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
    assert response_info['status'] == "REJECTED"
    assert response_info['status_reason'] == reason


def test_update_global_api_fields(simple_user):
    '''
        Test whether an API is correctly created then updated
    '''
    api_info = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()],
                'version_name': "some_version_name"
                }
    
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']

    client.post("/admin/service/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'sid': sid,
                                'reason': "",
                                'approved': True,
                                'version_name': api_info["version_name"],
                                'service_global': True
                            })

    update_request_info = {
        'sid' : sid,
        'name' : 'new name',
        'description' : 'new description',
        'tags' : ['new', 'tag'],
    }

    response = client.post("/service/update",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=update_request_info)
    assert response.status_code == SUCCESS

    # Information returned should be of updated service not original
    response = client.get("/admin/get/services",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 0
    assert len(response_info["global_updates"]) == 1
    assert len(response_info["version_updates"]) == 0

    global_fields = response_info["global_updates"][0]
    
    assert global_fields['id'] == sid
    assert global_fields['name'] == update_request_info['name']
    assert global_fields['description'] == update_request_info['description']
    assert global_fields['tags'] == update_request_info['tags']

    # make sure pending update so details have not yet changed and status is pending
    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
   
    assert response_info['id'] == sid
    assert response_info['name'] == api_info['name']
    assert response_info['description'] == api_info['description']
    assert response_info['tags'] == api_info['tags']
    assert response_info["versions"][0]["endpoints"] == api_info["endpoints"]
    assert response_info['status'] == "UPDATE_PENDING"

    response = client.get("/service/filter",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()

    assert response_info[0]['id'] == sid
    assert response_info[0]['name'] == api_info['name']
    assert response_info[0]['description'] == api_info['description']
    assert response_info[0]['tags'] == api_info['tags']

    reason = 'unpog service'

    client.post("/admin/service/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'sid': sid,
                                'reason': reason,
                                'approved': False,
                                'service_global': True
                            })
    
    # check after rejection details have not changed

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
   
    assert response_info['id'] == sid
    assert response_info['name'] == api_info['name']
    assert response_info['description'] == api_info['description']
    assert response_info['tags'] == api_info['tags']
    assert response_info["versions"][0]["endpoints"] == api_info["endpoints"]
    assert response_info['status'] == "UPDATE_REJECTED"
    assert response_info['status_reason'] == reason

    response = client.get("/service/filter",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()

    assert response_info[0]['id'] == sid
    assert response_info[0]['name'] == api_info['name']
    assert response_info[0]['description'] == api_info['description']
    assert response_info[0]['tags'] == api_info['tags']

    response = client.get("/admin/get/services",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 0
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 0

    response = client.post("/service/update",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=update_request_info)
    assert response.status_code == SUCCESS

    
    response = client.get("/admin/get/services",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 0
    assert len(response_info["global_updates"]) == 1
    assert len(response_info["version_updates"]) == 0

    reason = "pog service"
    client.post("/admin/service/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'sid': sid,
                                'reason': reason,
                                'approved': True,
                                'service_global': True
                            })


    # now approved, so check details have properly changed and status is LIVE
    
    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
   
    assert response_info['id'] == sid
    assert response_info['name'] == update_request_info['name']
    assert response_info['description'] == update_request_info['description']
    assert response_info['tags'] == update_request_info['tags']
    assert response_info['status'] == "LIVE"
    assert response_info['status_reason'] == reason

    database_object = db_get_service(sid)
    assert database_object['id'] == sid
    assert database_object['name'] == update_request_info['name']
    assert database_object['description'] == update_request_info['description']
    assert database_object['tags'] == update_request_info['tags']

    response = client.get("/service/filter",
                          headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    response_info = response.json()

    assert response_info[0]['id'] == sid
    assert response_info[0]['name'] == update_request_info['name']
    assert response_info[0]['description'] == update_request_info['description']
    assert response_info[0]['tags'] == update_request_info['tags']

    response = client.get("/admin/get/services",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    
    response = client.get("/admin/get/services",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 0
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 0


def test_service_version(simple_user):
    '''
        Test whether an API is correctly created
    '''
    api_info = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()],
                "version_name": "test version",
                "version_description": "test description"
                }

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS

    sid = response.json()['id']

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]

    response = client.post("/admin/service/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'sid': sid,
                                'reason': "",
                                'approved': True,
                                'version_name': api_info["version_name"],
                                'service_global': True
                            })
    assert response.status_code == SUCCESS

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS

    new_version = {
        "sid" : sid,
        "version_name" : "version 2",
        "version_description" : "new description",
        "endpoints" : [simple_endpoint2.model_dump()]
    }

    response = client.post("/service/version/add",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          json=new_version)
    
    assert response.status_code == SUCCESS
    response_info = response.json()

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()

    # global fields should be unchanged
    assert response_info['id'] == sid
    assert response_info['name'] == api_info['name']
    assert response_info['description'] == api_info['description']
    assert response_info['tags'] == api_info['tags']
    assert response_info['status'] == "LIVE"

    most_recent_version = response_info["versions"][0]
    assert most_recent_version["version_name"] == new_version["version_name"]
    assert most_recent_version["version_description"] == new_version["version_description"]
    assert most_recent_version["endpoints"] == new_version["endpoints"]
    assert most_recent_version["status"] == "PENDING"

    original_version = response_info["versions"][1]
    assert original_version["version_name"] == api_info["version_name"]
    assert original_version["version_description"] == api_info["version_description"]
    assert original_version["endpoints"] == api_info["endpoints"]
    assert original_version['status'] == "LIVE"


    response = client.delete("/service/version/delete",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid,
                              'version_name': most_recent_version["version_name"]
                          })
    assert response.status_code == SUCCESS

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()

    # global fields should be unchanged
    assert response_info['id'] == sid
    assert response_info['name'] == api_info['name']
    assert response_info['description'] == api_info['description']
    assert response_info['tags'] == api_info['tags']
    assert response_info['status'] == "LIVE"

    assert len(response_info["versions"]) == 1

    original_version = response_info["versions"][0]
    assert original_version["version_name"] == api_info["version_name"]
    assert original_version["version_description"] == api_info["version_description"]
    assert original_version["endpoints"] == api_info["endpoints"]
    assert original_version['status'] == "LIVE"

def test_update_version_api_fields(simple_user):
    '''
        Test whether an API is correctly created then updated for version specific fields
    '''
    api_info = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()],
                'version_name': "some_version_name"
                }
    
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS

    response_info = response.json()
    sid = response_info['id']

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()

    assert response_info["newly_created"]
    assert response_info["versions"][0]["newly_created"]

    client.post("/admin/service/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'sid': sid,
                                'reason': "",
                                'approved': True,
                                'version_name': api_info["version_name"],
                                'service_global': True
                            })
    
    assert response.status_code == SUCCESS

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
    
    assert not response_info["newly_created"]
    assert not response_info["versions"][0]["newly_created"]

    new_version = {
        "sid" : sid,
        "version_name" : "version 2",
        "version_description" : "new description",
        "endpoints" : [simple_endpoint2.model_dump()]
    }

    response = client.get("/admin/get/services",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 0
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 0


    response = client.post("/service/version/add",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          json=new_version)
    
    assert response.status_code == SUCCESS
    response_info = response.json()

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()

    assert response_info["versions"][0]["newly_created"]
    assert not response_info["versions"][1]["newly_created"]

    response = client.get("/admin/get/services",
                        headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 0
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 1

    new_version_service = response_info["version_updates"][0]

    assert new_version_service['endpoints'] == new_version["endpoints"]
    assert new_version_service['version_name'] == new_version["version_name"]
    assert new_version_service['version_description'] == new_version["version_description"]
    
    reason = "good"
    response = client.post("/admin/service/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'sid': sid,
                                'reason': reason,
                                'approved': True,
                                'service_global': False,
                                "version_name": new_version["version_name"]
                            })
    assert response.status_code == SUCCESS

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()

    assert response_info['status'] == "LIVE"
    assert response_info['status_reason'] == reason
    assert response_info["versions"][0]["status"] == "LIVE"
    assert response_info["versions"][0]["status_reason"] == reason
    assert not response_info["versions"][0]["newly_created"]
    assert not response_info["versions"][1]["newly_created"]

    response = client.get("/admin/get/services",
                    headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 0
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 0
    
    update_request_info = {
        'sid' : sid,
        'version_name': new_version["version_name"],
        'new_version_name': "new version name",
        'endpoints' : [simple_endpoint3.model_dump()],
        'version_description': "new version description"
    }

    response = client.post("/service/version/update",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=update_request_info)
    assert response.status_code == SUCCESS

    response = client.get("/admin/get/services",
                    headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 0
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 1
    
    new_version_service = response_info["version_updates"][0]

    assert new_version_service['endpoints'] == update_request_info["endpoints"]
    assert new_version_service['version_name'] == update_request_info["new_version_name"]
    assert new_version_service['version_description'] == update_request_info["version_description"]

    # make sure pending update so details have not yet changed and status is pending
    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
   
    assert response_info['status'] == "LIVE"
    assert response_info['status_reason'] == reason
    assert response_info["versions"][0]["status"] == "UPDATE_PENDING"
    assert response_info["versions"][0]["status"] == "UPDATE_PENDING"

    reason = 'unpog service'

    client.post("/admin/service/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'sid': sid,
                                'reason': reason,
                                'approved': False,
                                'service_global': False,
                                'version_name': new_version["version_name"]
                            })
    
    # check after rejection details have not changed

    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()

    assert response_info['status'] == "LIVE"
    assert response_info['status_reason'] != reason
    assert response_info["versions"][0]["status"] == "UPDATE_REJECTED"
    assert response_info["versions"][0]["status_reason"] == reason

    response = client.get("/admin/get/services",
                    headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 0
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 0

    response = client.post("/service/version/update",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=update_request_info)
    assert response.status_code == SUCCESS

    response = client.get("/admin/get/services",
                    headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 0
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 1

    reason = "pog service"
    client.post("/admin/service/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'sid': sid,
                                'reason': reason,
                                'approved': True,
                                'service_global': False,
                                'version_name': new_version["version_name"]
                            })


    # now approved, so check details have properly changed and status is LIVE
    
    response = client.get("/service/get_service",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          params={
                              'sid' : sid
                          })
    
    assert response.status_code == SUCCESS
    response_info = response.json()
   
    assert response_info['id'] == sid
    assert response_info['name'] == api_info['name']
    assert response_info['description'] == api_info['description']
    assert response_info['tags'] == api_info['tags']
    assert len(response_info["versions"]) == 2

    original_version = response_info["versions"][1]
    assert original_version["version_name"] == api_info["version_name"]
    assert original_version["endpoints"] == api_info["endpoints"]
    assert original_version["status"] == "LIVE"
    assert not original_version["newly_created"]

    new_version = response_info["versions"][0]
    assert new_version["version_name"] == update_request_info["new_version_name"]
    assert new_version["endpoints"] == update_request_info["endpoints"]
    assert new_version["version_description"] == update_request_info["version_description"]
    assert new_version["status"] == "LIVE"
    assert new_version["status_reason"] == reason
    assert not new_version["newly_created"]



    #TODO: check newly created
    # TODO: database tests
    # database_object = db_get_service(sid)
    # assert database_object['id'] == sid
    # assert database_object['name'] == update_request_info['name']
    # assert database_object['description'] == update_request_info['description']
    # assert database_object['tags'] == update_request_info['tags']


def test_global_version_combination_updates(simple_user):

    service1 = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.model_dump()],
                'version_name': "some_version_name"
                }
    

    service2 = {
        'name' : 'Test API 2',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This ',
                'tags' : ['Service'],
                'endpoints': [simple_endpoint2.model_dump()],
                'version_name': "other version name"
    }
    
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]

    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=service1)
    assert response.status_code == SUCCESS

    response_info = response.json()
    sid = response_info['id']

    client.post("/admin/service/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'sid': sid,
                                'reason': "",
                                'approved': True,
                                'version_name': service1["version_name"],
                                'service_global': True
                            })
    
    response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=service2)
    assert response.status_code == SUCCESS

    response_info = response.json()
    sid2 = response_info['id']

    response = client.get("/admin/get/services",
                    headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 1
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 0 

    # perform local update
    update_local_info = {
        'sid' : sid,
        'version_name': service1["version_name"],
        'new_version_name': "new version name",
        'endpoints' : [simple_endpoint3.model_dump()],
        'version_description': "new version description"
    }

    response = client.post("/service/version/update",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=update_local_info)
    assert response.status_code == SUCCESS

    response = client.get("/admin/get/services",
                    headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 1
    assert len(response_info["global_updates"]) == 0
    assert len(response_info["version_updates"]) == 1 

    update_global_info = {
        'sid' : sid,
        'name' : 'new name',
        'description' : 'new description',
        'tags' : ['new', 'tag'],
    }

    response = client.post("/service/update",
                           headers={"Authorization": f"Bearer {simple_user['token']}"},
                           json=update_global_info)
    assert response.status_code == SUCCESS

    response = client.get("/admin/get/services",
                    headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 1
    assert len(response_info["global_updates"]) == 1
    assert len(response_info["version_updates"]) == 1

    new_version = {
        "sid" : sid,
        "version_name" : "version 2",
        "version_description" : "new description",
        "endpoints" : [simple_endpoint2.model_dump()]
    }

    response = client.post("/service/version/add",
                          headers={"Authorization": f"Bearer {simple_user['token']}"},
                          json=new_version)
    
    assert response.status_code == SUCCESS

    response = client.get("/admin/get/services",
                    headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS

    response_info = response.json()
    assert len(response_info["new_services"]) == 1
    assert len(response_info["global_updates"]) == 1
    assert len(response_info["version_updates"]) == 2