# import sys, os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# import pytest
# from fastapi import FastAPI
# from fastapi.testclient import TestClient
# from src.backend.classes import Service
# from src.backend.app import app
# from src.backend.classes.models import User, db


# # Create a test client
# client = TestClient(app)

# INPUT_ERROR = 400
# AUTHENTICATION_ERROR = 401
# SUCCESS = 200

# def clear_all():
#     ''' 
#         Method to reset local database for new test
#     '''
#     response = client.post("/testing/clear")
#     assert response.status_code == SUCCESS
#     assert  response.json() == {"message" : "Clear Successful"}
#     db.users.delete_many({})

# @pytest.fixture
# def simple_user():
#     '''
#         Simulates a simple user registering their account then logging in
#     '''
#     # Clear data abse
#     clear_all()

#     # Register user
#     user_creds = {
#         "username" : "Tester 1",
#         "password" : "password"
#     }

#     usable_data = {"token" : None}

#     response = client.post("/auth/register",
#                             json=user_creds)
#     assert response.status_code == SUCCESS

#     # Log into account
#     response = client.post("/auth/login",
#                            json=user_creds)
#     assert response.status_code == SUCCESS
#     usable_data['token'] = response.json()['access_token']

#     return usable_data

# # Error testing
# def test_invalid_user(simple_user):
#     '''
#         Test that add_service is only usable by users not guests
#     '''
#     response = client.post("/service/add",
#                            headers={"Authorization": "Bearer"},
#                            json={
#                                 'name' : 'Test API',
#                                 'icon_url' : '',
#                                 'x_start' : 0,
#                                 'x_end' : 0,
#                                 'y_start' : 0,
#                                 'y_end' : 0,
#                                 'description' : '',
#                                 'tags' : []
#                            })
#     assert response.status_code == AUTHENTICATION_ERROR

# def test_no_name(simple_user):
#     '''
#         Test whether no name is caught
#     '''
#     response = client.post("/service/add",
#                             headers={"Authorization": f"Bearer {simple_user['token']}"},
#                             json={
#                                 'name' : '',
#                                 'icon_url' : '',
#                                 'x_start' : 0,
#                                 'x_end' : 0,
#                                 'y_start' : 0,
#                                 'y_end' : 0,
#                                 'description' : '',
#                                 'tags' : []
#                            })
#     assert response.status_code == INPUT_ERROR

# def test_invalid_url():
#     '''
#         Test whether bad url (www.googlefake.xyzabsdh) is caught
#     '''
#     response = client.post("/service/add",
#                            headers={"Authorization": f"Bearer {simple_user['token']}"},
#                            json={
#                                 'name' : 'Test API',
#                                 'icon_url' : 'www.googlefake.xyzabsdh',
#                                 'x_start' : 0,
#                                 'x_end' : 0,
#                                 'y_start' : 0,
#                                 'y_end' : 0,
#                                 'description' : 'hi',
#                                 'tags' : ['API']
#                            })
#     assert response.status_code == INPUT_ERROR

# def test_invalid_dimensions(simple_user):
#     '''
#         Test whether combinations of bad dimensions are caught
#     '''
#     # Negative x-start
#     response = client.post("/service/add",
#                            headers={"Authorization": f"Bearer {simple_user['token']}"},
#                            json={
#                                 'name' : 'Test API',
#                                 'icon_url' : '',
#                                 'x_start' : -10,
#                                 'x_end' : 0,
#                                 'y_start' : 0,
#                                 'y_end' : 0,
#                                 'description' : 'hi',
#                                 'tags' : ['API']
#                            })
#     assert response.status_code == INPUT_ERROR

#     # x-start bigger than x-end
#     response = client.post("/service/add",
#                            headers={"Authorization": f"Bearer {simple_user['token']}"},
#                            json={
#                                 'name' : 'Test API',
#                                 'icon_url' : '',
#                                 'x_start' : 1000,
#                                 'x_end' : 0,
#                                 'y_start' : 0,
#                                 'y_end' : 0,
#                                 'description' : 'hi',
#                                 'tags' : ['API']
#                            })
#     assert response.status_code == INPUT_ERROR

#     # Negative y-start
#     response = client.post("/service/add",
#                            headers={"Authorization": f"Bearer {simple_user['token']}"},
#                            json={
#                                 'name' : 'Test API',
#                                 'icon_url' : '',
#                                 'x_start' : 0,
#                                 'x_end' : 0,
#                                 'y_start' : -10,
#                                 'y_end' : 0,
#                                 'description' : 'hi',
#                                 'tags' : ['API']
#                            })
#     assert response.status_code == INPUT_ERROR

#     # Bigger y-start than y-end
#     response = client.post("/service/add",
#                            headers={"Authorization": f"Bearer {simple_user['token']}"},
#                            json={
#                                 'name' : 'Test API',
#                                 'icon_url' : '',
#                                 'x_start' : 0,
#                                 'x_end' : 0,
#                                 'y_start' : 1000,
#                                 'y_end' : 0,
#                                 'description' : 'hi',
#                                 'tags' : ['API']
#                            })
#     assert response.status_code == INPUT_ERROR

# def test_no_description(simple_user):
#     '''
#         Test whether no description given is caught
#     '''
#     response = client.post("/service/add",
#                            headers={"Authorization": f"Bearer {simple_user['token']}"},
#                            json={
#                                 'name' : 'Test API',
#                                 'icon_url' : '',
#                                 'x_start' : 0,
#                                 'x_end' : 0,
#                                 'y_start' : 0,
#                                 'y_end' : 0,
#                                 'description' : '',
#                                 'tags' : []
#                            })
#     assert response.status_code == INPUT_ERROR

# def test_no_tags(simple_user):
#     '''
#         Test whether no description given is caught
#     '''
#     response = client.post("/service/add",
#                             headers={"Authorization": f"Bearer {simple_user['token']}"},
#                            json={
#                                 'name' : 'Test API',
#                                 'icon_url' : '',
#                                 'x_start' : 0,
#                                 'x_end' : 0,
#                                 'y_start' : 0,
#                                 'y_end' : 0,
#                                 'description' : 'This is a test API',
#                                 'tags' : []
#                            })
#     assert response.status_code == INPUT_ERROR

# # Valid instances
# def test_create_api(simple_user):
#     '''
#         Test whether an API is correctly created
#     '''
#     api_info = {
#                 'name' : 'Test API',
#                 'icon_url' : '',
#                 'x_start' : 0,
#                 'x_end' : 0,
#                 'y_start' : 0,
#                 'y_end' : 0,
#                 'description' : 'This is a test API',
#                 'tags' : ['API']
#                 }

#     response = client.post("/service/add",
#                            headers={"Authorization": f"Bearer {simple_user['token']}"},
#                            json=api_info)
#     assert response.status_code == SUCCESS
#     sid = response.json()['sid']

#     response = client.get("/service/get_service",
#                           headers={"Authorization": f"Bearer {simple_user['token']}"},
#                           params={
#                               'sid' : sid
#                           })
    
#     assert response.status_code == SUCCESS
#     response_info = response.json()
#     assert response_info['sid'] == sid
#     assert response_info['name'] == api_info['name']
#     assert response_info['description'] == api_info['description']
#     assert response_info['tags'] == api_info['tags']

# def test_multiple_tags(simple_user):
#     '''
#         Test whether an API is correctly created where it has multiple tags
#     '''
#     api_info = {
#                 'name' : 'Test API',
#                 'icon_url' : '',
#                 'x_start' : 0,
#                 'x_end' : 0,
#                 'y_start' : 0,
#                 'y_end' : 0,
#                 'description' : 'This is a test API',
#                 'tags' : ['API', 'Public', 'In Development']
#                 }

#     response = client.post("/service/add",
#                            headers={"Authorization": f"Bearer {simple_user['token']}"},
#                            json=api_info)
#     assert response.status_code == SUCCESS
#     sid = response.json()['sid']

#     response = client.get("/service/get_service",
#                           headers={"Authorization": f"Bearer {simple_user['token']}"},
#                           params={
#                               'sid' : sid
#                           })
    
#     assert response.status_code == SUCCESS
#     response_info = response.json()
#     assert response_info['sid'] == sid
#     assert response_info['name'] == api_info['name']
#     assert response_info['description'] == api_info['description']
#     assert response_info['tags'] == api_info['tags']

# def test_custom_icon():
#     '''
#         Test whether create can handle custom icon_url:
#             https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png
#     '''
#     api_info = {
#                 'name' : 'Fake Google',
#                 'icon_url' : 'https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png',
#                 'x_start' : 0,
#                 'x_end' : 0,
#                 'y_start' : 0,
#                 'y_end' : 0,
#                 'description' : 'This is a definitely... Google',
#                 'tags' : ['API', 'Public', 'In Development']
#                 }

#     response = client.post("/service/add",
#                            headers={"Authorization": f"Bearer {simple_user['token']}"},
#                            json=api_info)
#     assert response.status_code == SUCCESS
#     sid = response.json()['sid']

#     response = client.get("/service/get_service",
#                           headers={"Authorization": f"Bearer {simple_user['token']}"},
#                           params={
#                               'token' : simple_user['token'],
#                               'sid' : sid
#                           })
    
#     assert response.status_code == SUCCESS
#     response_info = response.json()
#     assert response_info['sid'] == sid
#     assert response_info['name'] == api_info['name']
#     assert response_info['description'] == api_info['description']
#     assert response_info['tags'] == api_info['tags']
#     assert response_info['icon_url'] == api_info['icon_url']
