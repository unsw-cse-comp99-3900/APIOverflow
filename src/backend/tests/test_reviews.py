import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.app import app 
from src.backend.classes.models import db

# Create a test client
client = TestClient(app)

INPUT_ERROR = 400
MISSING_ERROR = 404
FORBIDDEN_ERROR = 403
SUCCESS = 200
AUTHENTICATION_ERROR = 401

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

    usable_data = {"c_token" : None}

    response = client.post("/auth/register",
                            json=user_creds)
    assert response.status_code == SUCCESS

    # Log into account
    response = client.post("/auth/login",
                           json=user_creds)
    assert response.status_code == SUCCESS
    usable_data['c_token'] = response.json()['access_token']

    # Generate imposter
    user_creds = {
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
                           headers={"Authorization": f"Bearer {usable_data['token']}"},
                           json=api_info)
    assert response.status_code == SUCCESS
    usable_data['sid'] = response.json()['id']

    yield usable_data
    clear_all()

def test_add_review_guest():
    '''
        Test guest users are caught
    '''
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer "},
                json={})
    assert response.status_code == AUTHENTICATION_ERROR

def test_add_review_bad_api(simple_user):
    '''
        Test whether invalid service id is caught
    '''
    data = simple_user
    package = {
        'sid': -1,
        'rating': 'positive',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == MISSING_ERROR

def test_add_review_owner_attempt(simple_user):
    '''
        Test whether user is attempting to review themselves
    '''
    data = simple_user
    package = {
        'sid': data['sid'],
        'rating': 'positive',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['c_token']}"},
                json=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_add_review_bad_input(simple_user):
    '''
        Test whether no title or comment, or invalid rating is caught
    '''
    data = simple_user

    # Bad title
    package = {
        'sid': data['sid'],
        'rating': 'positive',
        'title': '',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == INPUT_ERROR

    # Bad comment
    package = {
        'sid': data['sid'],
        'rating': 'positive',
        'title': 'A review',
        'comment': ''
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == INPUT_ERROR

    # Empty rating
    package = {
        'sid': data['sid'],
        'rating': '',
        'title': 'A review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == INPUT_ERROR

    # Invalid rating
    package = {
        'sid': data['sid'],
        'rating': 'amazing!',
        'title': 'A review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == INPUT_ERROR

def test_add_review_success(simple_user):
    '''
        Test whether a review is added successfully
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    response = client.get("/service/get/reviews",
                          params={
                              'sid': data['sid'],
                              'testing': True
                          })
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['reviewer'] == '2'
    assert response.json()['reviews'][0]['type'] == package['rating']
    assert response.json()['reviews'][0]['title'] == package['title']
    assert response.json()['reviews'][0]['comment'] == package['comment']
    assert response.json()['reviews'][0]['service'] == package['sid']
    assert response.json()['reviews'][0]['status'] == "0"

    rid = response.json()['reviews'][0]['rid']
    response = client.get("/review/get",
                          params = {'rid': rid})
    assert response.status_code == SUCCESS
    assert response.json()['rid'] == rid
    assert response.json()['title'] == package['title']
    assert response.json()['type'] == package['rating']
    assert response.json()['comment'] == package['comment']
    assert response.json()['reviewer'] == "2"
    assert response.json()['status'] == "0"

def test_get_review_invalid():
    '''
        Test whether invalid review is caught
    '''

    package = {
        'rid': '-111'
    }
    response = client.get("/review/get", params=package)
    assert response.status_code == MISSING_ERROR

def test_delete_review_guest():
    '''
        Test whether guest user attempting delete is caught
    '''
    package = {
        'rid': '0'
    }
    response = client.delete("/review/delete",
                             headers={"Authorization": f"Bearer "},
                             params=package)
    assert response.status_code == AUTHENTICATION_ERROR

def test_delete_review_bad_review(simple_user):
    '''
        Test whether invalid review is caught
    '''
    data = simple_user
    package = {
        'rid': '0'
    }
    response = client.delete("/review/delete",
                             headers={"Authorization": f"Bearer {data['u_token']}"},
                             params=package)
    assert response.status_code == MISSING_ERROR

def test_delete_review_not_reviewer(simple_user):
    '''
        Test whether guest user attempting delete is caught
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.delete("/review/delete",
                             headers={"Authorization": f"Bearer {data['c_token']}"},
                             params=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_delete_review_success_reviewer(simple_user):
    '''
        Test whether reviewer deleting own review works
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.delete("/review/delete",
                             headers={"Authorization": f"Bearer {data['u_token']}"},
                             params=package)
    assert response.status_code == SUCCESS

    response = client.get("/review/get",
                          params={
                              'rid': '0'
                          })
    assert response.status_code == MISSING_ERROR
    
    response = client.get("/service/get/reviews",
                          params={
                              'sid': data['sid'],
                              'testing': True
                          })
    assert len(response.json()['reviews']) == 0

def test_delete_review_success_admin(simple_user):
    '''
        Test whether reviewer deleting own review works
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    package = {
        'rid': '0'
    }
    response = client.delete("/review/delete",
                             headers={"Authorization": f"Bearer {access_token}"},
                             params=package)
    assert response.status_code == SUCCESS

    response = client.get("/review/get",
                          params={
                              'rid': '0'
                          })
    assert response.status_code == MISSING_ERROR
    
    response = client.get("/service/get/reviews",
                          params={
                              'sid': data['sid'],
                              'testing': True
                          })
    assert len(response.json()['reviews']) == 0

def test_edit_review_guest():
    '''
        Test whether guest user attempting edit is caught
    '''
    package = {
        'rid': '0',
        'rating' : 'positive',
        'title': 'EDIT',
        'comment': "edited"
    }
    response = client.post("/review/edit",
                             headers={"Authorization": f"Bearer "},
                             params=package)
    assert response.status_code == AUTHENTICATION_ERROR

def test_edit_review_bad_review(simple_user):
    '''
        Test whether invalid review is caught
    '''
    data = simple_user
    package = {
        'rid': '0',
        'rating' : 'positive',
        'title': 'EDIT',
        'comment': "edited"
    }
    response = client.post("/review/edit",
                             headers={"Authorization": f"Bearer {data['u_token']}"},
                             params=package)
    assert response.status_code == MISSING_ERROR

def test_edit_review_not_reviewer(simple_user):
    '''
        Test whether guest user attempting delete is caught
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'rating' : 'positive',
        'title': 'EDIT - It gets good!',
        'comment': "Way better than mid"
    }
    response = client.post("/review/edit",
                             headers={"Authorization": f"Bearer {data['c_token']}"},
                             params=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_edit_review_successful(simple_user):
    '''
        Test whether guest user attempting delete is caught
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'rating' : 'positive',
        'title': 'EDIT - It gets good!',
        'comment': "Way better than mid"
    }
    response = client.post("/review/edit",
                             headers={"Authorization": f"Bearer {data['u_token']}"},
                             params=package)
    assert response.status_code == SUCCESS

    response = client.get("/service/get/reviews",
                          params={
                              'sid': data['sid'],
                              'testing': True
                          })
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['reviewer'] == '2'
    assert response.json()['reviews'][0]['type'] == package['rating']
    assert response.json()['reviews'][0]['title'] == package['title']
    assert response.json()['reviews'][0]['comment'] == package['comment']
    assert response.json()['reviews'][0]['status'] == "0"

    rid = response.json()['reviews'][0]['rid']
    response = client.get("/review/get",
                          params = {'rid': rid})
    assert response.status_code == SUCCESS
    assert response.json()['rid'] == rid
    assert response.json()['title'] == package['title']
    assert response.json()['type'] == package['rating']
    assert response.json()['comment'] == package['comment']
    assert response.json()['reviewer'] == "2"
    assert response.json()['status'] == "0"

def test_edit_review_successful_admin(simple_user):
    '''
        Test whether guest user attempting delete is caught
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    package = {
        'rid': '0',
        'rating' : 'positive',
        'title': 'EDIT - It gets good!',
        'comment': "Way better than mid"
    }
    response = client.post("/review/edit",
                             headers={"Authorization": f"Bearer {access_token}"},
                             params=package)
    assert response.status_code == SUCCESS

    response = client.get("/service/get/reviews",
                          params={
                              'sid': data['sid'],
                              'testing': True
                          })
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['reviewer'] == '2'
    assert response.json()['reviews'][0]['type'] == package['rating']
    assert response.json()['reviews'][0]['title'] == package['title']
    assert response.json()['reviews'][0]['comment'] == package['comment']
    assert response.json()['reviews'][0]['status'] == "0"

    rid = response.json()['reviews'][0]['rid']
    response = client.get("/review/get",
                          params = {'rid': rid})
    assert response.status_code == SUCCESS
    assert response.json()['rid'] == rid
    assert response.json()['title'] == package['title']
    assert response.json()['type'] == package['rating']
    assert response.json()['comment'] == package['comment']
    assert response.json()['reviewer'] == "2"
    assert response.json()['status'] == "0"

def test_approve_review_non_admin(simple_user):
    '''
        User not an admin
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    response = client.post("/review/approve",
                           headers={"Authorization": f"Bearer {data['u_token']}"},
                            json={
                                'rid': '0',
                                'reason': 'lit!'
                            })
    assert response.status_code == FORBIDDEN_ERROR

def test_approve_review_invalid_review(simple_user):
    '''
        Approving non-existent review
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]
    response = client.post("/review/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'rid': '0',
                                'reason': 'lit!'
                            })
    assert response.status_code == MISSING_ERROR

def test_approve_review_successful(simple_user):
    '''
        Approving review
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS


    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]
    response = client.post("/review/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'rid': '0',
                                'reason': 'lit!'
                            })
    assert response.status_code == SUCCESS

    response = client.get("/service/get/reviews",
                          params={
                              'sid': data['sid']
                          })
    assert response.status_code == SUCCESS
    assert response.json()['reviews'][0]['status'] == '1'

def test_reject_review_non_admin(simple_user):
    '''
        User not an admin
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    response = client.post("/review/reject",
                           headers={"Authorization": f"Bearer {data['u_token']}"},
                            json={
                                'rid': '0',
                                'reason': 'lit!'
                            })
    assert response.status_code == FORBIDDEN_ERROR

def test_reject_review_invalid_review(simple_user):
    '''
        Rejecting non-existent review
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]
    response = client.post("/review/reject",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'rid': '0',
                                'reason': 'lit!'
                            })
    assert response.status_code == MISSING_ERROR

def test_reject_review_successful(simple_user):
    '''
        Approving review
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS


    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]
    response = client.post("/review/reject",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'rid': '0',
                                'reason': 'lit!'
                            })
    assert response.status_code == SUCCESS

    response = client.get("/service/get/reviews",
                          params={
                              'sid': data['sid'],
                              'testing': True
                          })
    assert response.status_code == SUCCESS
    assert response.json()['reviews'][0]['status'] == '-1'

def test_service_rating_bad_api(simple_user):
    '''
        Test whether bad service is rejected
    '''
    data = simple_user
    package = {
        'sid': '-1'
    }
    response = client.get("/service/get/rating",
                          params=package)
    assert response.status_code == MISSING_ERROR
    
def test_service_rating_no_review(simple_user):
    '''
        Test whether no review = neutral rating
    '''
    data = simple_user
    package = {
        'sid': data['sid']
    }
    response = client.get("/service/get/rating",
                          params=package)
    assert response.status_code == SUCCESS
    assert response.json()['positive'] == 0
    assert response.json()['negative'] == 0
    assert response.json()['rating'] == 0.00

def test_service_rating_negative(simple_user):
    '''
        Test whether negative review is registered
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
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
    assert response.json()['positive'] == 0
    assert response.json()['negative'] == 1
    assert response.json()['rating'] == -1.00

def test_service_rating_positive(simple_user):
    '''
        Test whether positive review is registered
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'positive',
        'title': 'A Review',
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
    assert response.json()['positive'] == 1
    assert response.json()['negative'] == 0
    assert response.json()['rating'] == 1.00

def test_service_get_reviews_bad_api():
    '''
        Test bad call
    '''
    response = client.get("/service/get/reviews",
                          params={
                              'sid': '-1'
                          })
    assert response.status_code == MISSING_ERROR

def test_user_get_reviews_guest():
    '''
        Guest trying to access reviews
    '''
    response = client.get("/user/get/reviews",
                headers={"Authorization": f"Bearer "})
    assert response.status_code == AUTHENTICATION_ERROR

def test_user_get_reviews_empty(simple_user):
    '''
        User with no reviews posted
    '''
    data = simple_user
    response = client.get("/user/get/reviews",
                headers={"Authorization": f"Bearer {data['u_token']}"})
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 0

def test_user_get_reviews_one(simple_user):
    '''
        Test whether positive review is registered
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'positive',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'sid': data['sid']
    }
    response = client.get("/user/get/reviews",
                          headers={"Authorization": f"Bearer {data['u_token']}"})
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['rid'] == '0'
    assert response.json()['reviews'][0]['service'] == data['sid']
    assert response.json()['reviews'][0]['title'] == 'A Review'
    assert response.json()['reviews'][0]['rating'] == 'positive'
    assert response.json()['reviews'][0]['status'] == '0'

def test_user_get_reviews_approved(simple_user):
    '''
        Test whether review shows as approved
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS


    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]
    response = client.post("/review/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'rid': '0',
                                'reason': 'lit!'
                            })
    assert response.status_code == SUCCESS
    response = client.get("/user/get/reviews",
                          headers={"Authorization": f"Bearer {data['u_token']}"})
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['rid'] == '0'
    assert response.json()['reviews'][0]['status'] == '1'

def test_user_get_reviews_rejected(simple_user):
    '''
        Test whether review shows as rejected
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS


    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]
    response = client.post("/review/reject",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'rid': '0',
                                'reason': 'lit!'
                            })
    assert response.status_code == SUCCESS
    response = client.get("/user/get/reviews",
                          headers={"Authorization": f"Bearer {data['u_token']}"})
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['rid'] == '0'
    assert response.json()['reviews'][0]['status'] == '-1'

def test_admin_get_reviews_user(simple_user):
    '''
        Test non-admin
    '''
    data = simple_user
    response = client.post("/admin/get/reviews",
                            headers={"Authorization": f"Bearer {data['u_token']}"})
    assert response.status_code == FORBIDDEN_ERROR

def test_admin_get_reviews_pending(simple_user):
    '''
        Test whether positive review is registered
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'positive',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'sid': data['sid']
    }
    response = client.get("/admin/get/reviews",
                          headers={"Authorization": f"Bearer {data['u_token']}"})
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['rid'] == '0'
    assert response.json()['reviews'][0]['service'] == data['sid']
    assert response.json()['reviews'][0]['title'] == 'A Review'
    assert response.json()['reviews'][0]['rating'] == 'positive'
    assert response.json()['reviews'][0]['status'] == '0'

def test_admin_get_reviews_approved(simple_user):
    '''
        Test whether review shows as approved
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS


    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]
    response = client.post("/review/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'rid': '0',
                                'reason': 'lit!'
                            })
    assert response.status_code == SUCCESS
    response = client.get("/admin/get/reviews",
                          headers={"Authorization": f"Bearer {data['u_token']}"})
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['rid'] == '0'
    assert response.json()['reviews'][0]['status'] == '1'

def test_admin_get_reviews_rejected(simple_user):
    '''
        Test whether review shows as rejected
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS


    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]
    response = client.post("/review/reject",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'rid': '0',
                                'reason': 'lit!'
                            })
    assert response.status_code == SUCCESS
    response = client.get("/admin/get/reviews",
                          headers={"Authorization": f"Bearer {data['u_token']}"})
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['rid'] == '0'
    assert response.json()['reviews'][0]['status'] == '-1'

def test_admin_get_reviews_wrong_filter(simple_user):
    '''
        Test whether positive review is registered
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'positive',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'sid': data['sid']
    }
    response = client.get("/admin/get/reviews",
                          headers={"Authorization": f"Bearer {data['u_token']}"},
                          params={
                              'option': '-1'
                          })
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 0

def test_admin_get_reviews_pending_filter(simple_user):
    '''
        Test whether positive review is registered
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'positive',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'sid': data['sid']
    }
    response = client.get("/admin/get/reviews",
                          headers={"Authorization": f"Bearer {data['u_token']}"},
                          params={
                              'option': '0'
                          })
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['rid'] == '0'
    assert response.json()['reviews'][0]['service'] == data['sid']
    assert response.json()['reviews'][0]['title'] == 'A Review'
    assert response.json()['reviews'][0]['rating'] == 'positive'
    assert response.json()['reviews'][0]['status'] == '0'

def test_admin_get_reviews_approved_filter(simple_user):
    '''
        Test whether review shows as approved
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS


    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]
    response = client.post("/review/approve",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'rid': '0',
                                'reason': 'lit!'
                            })
    assert response.status_code == SUCCESS
    response = client.get("/admin/get/reviews",
                          headers={"Authorization": f"Bearer {data['u_token']}"},
                          params={
                              'option': '1'
                          })
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['rid'] == '0'
    assert response.json()['reviews'][0]['status'] == '1'

def test_admin_get_reviews_rejected_filter(simple_user):
    '''
        Test whether review shows as rejected
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'negative',
        'title': 'A Review',
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS


    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS

    access_token = response.json()["access_token"]
    response = client.post("/review/reject",
                           headers={"Authorization": f"Bearer {access_token}"},
                            json={
                                'rid': '0',
                                'reason': 'lit!'
                            })
    assert response.status_code == SUCCESS
    response = client.get("/admin/get/reviews",
                          headers={"Authorization": f"Bearer {data['u_token']}"},
                          params={
                              'option': '-1'
                          })
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['rid'] == '0'
    assert response.json()['reviews'][0]['status'] == '-1'
