import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.classes import Service
from src.backend.app import app
from src.backend.classes.models import User
from src.backend.classes.datastore import defaults
from src.backend.classes.Endpoint import Endpoint
from src.backend.classes.Parameter import Parameter 
from src.backend.classes.Response import Response

# test endpoint
simple_parameter = Parameter(id="1", endpoint_link='https://api.example.com/users/12345', required=True, 
                            type='HEADER', name='paramtest', value_type='int')
simple_response = Response(code='404', description='not found', conditions=["site is down", "badtest"], 
                            example="example...")
simple_endpoint = Endpoint(link='https://api.example.com/users/12345', title_description='testTitle1', 
                            main_description='tests endpoint', tab='tabTest', parameters=[simple_parameter], 
                            method="POST", responses=[simple_response])

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

@pytest.fixture
def admin_user():
    '''
        Simulates an admin user registering their account then logging in
    '''
    # Clear database
    clear_all()

    # Register user
    user_creds = {
        "username" : "superadmin",
        "password" : "superadminpassword"
    }

    usable_data = {"token" : None}

    # response = client.post("/auth/register",
    #                         json=user_creds)
    # assert response.status_code == SUCCESS

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
    assert response.json()['tags'] == defaults

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
                                'tag' : defaults[0]
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

def test_get_top5(admin_user):
    '''
        Test whether get top 5 works
    '''   
    custom = [
        {'tag': 'custom1'},
        {'tag': 'custom2'},
        {'tag': 'custom3'},
        {'tag': 'custom4'},
        {'tag': 'custom5'},
    ]
    customs = ['custom1', 'custom2', 'custom3', 'custom4', 'custom5']
    sid = []
    for tag in custom:
        response = client.post("/tag/add",
                            headers={"Authorization": f"Bearer {admin_user['token']}"},
                            json=tag)
        assert response.status_code == SUCCESS
    for i in range(4):
        api_info = {
                    'name' : f'Test API{i}',
                    'description' : 'This is a test API',
                    'tags' : ['API', 'Microservice'] + customs[:(i + 1)],
                    'endpoints': [simple_endpoint.model_dump()],
                    'version_name': "some_version_name"
                    }
        response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {admin_user['token']}"},
                           json=api_info)
        assert response.status_code == SUCCESS
        sid.append(response.json()['id'])

    reason = 'very pog service'
    for i in range(4):
        response = client.post("/admin/service/approve",
                            headers={"Authorization": f"Bearer {admin_user['token']}"},
                                json={
                                    'sid': sid[i],
                                    'reason': reason,
                                    'approved': True,
                                    'version_name': api_info["version_name"],
                                    'service_global': True
                                })
        assert response.status_code == SUCCESS

    response = client.get("/tags/get/ranked",
                          params={'num': 5})
    assert response.status_code == SUCCESS
    assert response.json()['tags'][0]['tag'] == 'API'
    assert response.json()['tags'][0]['num'] == 4
    assert response.json()['tags'][1]['tag'] == 'custom1'
    assert response.json()['tags'][1]['num'] == 4
    assert response.json()['tags'][2]['tag'] == 'Microservice'
    assert response.json()['tags'][2]['num'] == 4
    assert response.json()['tags'][3]['tag'] == 'custom2'
    assert response.json()['tags'][3]['num'] == 3
    assert response.json()['tags'][4]['tag'] == 'custom3'
    assert response.json()['tags'][4]['num'] == 2

def test_ranked_tags_delete_shift(admin_user):
    '''
        Test whether deleting a service updates tag analytics
    '''
    custom = [
        {'tag': 'custom1'},
        {'tag': 'custom2'},
        {'tag': 'custom3'},
        {'tag': 'custom4'},
        {'tag': 'custom5'},
    ]
    customs = ['custom1', 'custom2', 'custom3', 'custom4', 'custom5']
    sid = []
    for tag in custom:
        response = client.post("/tag/add",
                            headers={"Authorization": f"Bearer {admin_user['token']}"},
                            json=tag)
        assert response.status_code == SUCCESS
    for i in range(4):
        api_info = {
                    'name' : f'Test API{i}',
                    'description' : 'This is a test API',
                    'tags' : ['API'] + customs[:(i + 1)],
                    'endpoints': [simple_endpoint.model_dump()],
                    'version_name': "some_version_name"
                    }
        response = client.post("/service/add",
                           headers={"Authorization": f"Bearer {admin_user['token']}"},
                           json=api_info)
        assert response.status_code == SUCCESS
        sid.append(response.json()['id'])

    reason = 'very pog service'
    for i in range(4):
        response = client.post("/admin/service/approve",
                            headers={"Authorization": f"Bearer {admin_user['token']}"},
                                json={
                                    'sid': sid[i],
                                    'reason': reason,
                                    'approved': True,
                                    'version_name': api_info["version_name"],
                                    'service_global': True
                                })
        assert response.status_code == SUCCESS

    response = client.delete("/service/delete",
                             headers={"Authorization": f"Bearer {admin_user['token']}"},
                             params={'sid': sid[0]})
    assert response.status_code == SUCCESS

    response = client.get("/tags/get/ranked",
                          params={'num': 5})
    assert response.status_code == SUCCESS
    assert response.json()['tags'][0]['tag'] == 'API'
    assert response.json()['tags'][0]['num'] == 3
    assert response.json()['tags'][1]['tag'] == 'custom1'
    assert response.json()['tags'][1]['num'] == 3
    assert response.json()['tags'][2]['tag'] == 'custom2'
    assert response.json()['tags'][2]['num'] == 3
    assert response.json()['tags'][3]['tag'] == 'custom3'
    assert response.json()['tags'][3]['num'] == 2
    assert response.json()['tags'][4]['tag'] == 'custom4'
    assert response.json()['tags'][4]['num'] == 1

def test_ranked_tags_edit_shift(admin_user):
    '''
        Test whether updates properly update tag analytics
    '''
    custom = [
        {'tag': 'custom1'},
        {'tag': 'custom2'},
        {'tag': 'custom3'},
        {'tag': 'custom4'},
        {'tag': 'custom5'},
    ]
    customs = ['custom1', 'custom2', 'custom3', 'custom4', 'custom5']
    for tag in custom:
        response = client.post("/tag/add",
                            headers={"Authorization": f"Bearer {admin_user['token']}"},
                            json=tag)
        assert response.status_code == SUCCESS
    
    api_info = {
                    'name' : 'Test API',
                    'description' : 'This is a test API',
                    'tags' : ['API', 'Microservice'],
                    'endpoints': [simple_endpoint.model_dump()],
                    'version_name': "some_version_name"
                    }
    response = client.post("/service/add",
                        headers={"Authorization": f"Bearer {admin_user['token']}"},
                        json=api_info)
    assert response.status_code == SUCCESS
    sid = response.json()['id']

    response = client.post("/admin/service/approve",
                        headers={"Authorization": f"Bearer {admin_user['token']}"},
                            json={
                                'sid': sid,
                                'reason': "LOL",
                                'approved': True,
                                'version_name': api_info["version_name"],
                                'service_global': True
                            })
    assert response.status_code == SUCCESS

    response = client.get("/tags/get/ranked",
                          params={'num': 2})
    assert response.status_code == SUCCESS
    assert response.json()['tags'][0]['tag'] == 'API'
    assert response.json()['tags'][0]['num'] == 1
    assert response.json()['tags'][1]['tag'] == 'Microservice'
    assert response.json()['tags'][1]['num'] == 1

    package = {
        'name': 'HAXORZED',
        'description': 'This API has been HAXED',
        'tags': customs,
        'sid': sid,
        'pay_model': 'Premium'
    }
    response = client.post("/service/update",
                           headers={"Authorization": f"Bearer {admin_user['token']}"},
                            json=package)
    assert response.status_code == SUCCESS

    response = client.post("/admin/service/approve",
                        headers={"Authorization": f"Bearer {admin_user['token']}"},
                            json={
                                'sid': sid,
                                'reason': "LOL",
                                'approved': True,
                                'version_name': api_info["version_name"],
                                'service_global': True
                            })
    assert response.status_code == SUCCESS

    response = client.get("/tags/get/ranked",
                          params={'num': 5})
    assert response.status_code == SUCCESS
    assert response.json()['tags'][0]['tag'] == 'custom1'
    assert response.json()['tags'][0]['num'] == 1
    assert response.json()['tags'][1]['tag'] == 'custom2'
    assert response.json()['tags'][1]['num'] == 1
    assert response.json()['tags'][2]['tag'] == 'custom3'
    assert response.json()['tags'][2]['num'] == 1
    assert response.json()['tags'][3]['tag'] == 'custom4'
    assert response.json()['tags'][3]['num'] == 1
    assert response.json()['tags'][4]['tag'] == 'custom5'
    assert response.json()['tags'][4]['num'] == 1