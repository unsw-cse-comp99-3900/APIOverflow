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
                           headers={"Authorization": f"Bearer {usable_data['c_token']}"},
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
        'sid': '-1',
        'rating': 'positive',
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
        'comment': 'Mid at best'
    }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['c_token']}"},
                json=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_add_review_bad_input(simple_user):
    '''
        Test whether no comment, or invalid rating is caught
    '''
    data = simple_user

    # Bad comment
    package = {
        'sid': data['sid'],
        'rating': 'positive',
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
    print(response.json())
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['reviewer'] == '2'
    assert response.json()['reviews'][0]['type'] == package['rating']
    assert response.json()['reviews'][0]['comment'] == package['comment']
    assert response.json()['reviews'][0]['service'] == package['sid']

    rid = response.json()['reviews'][0]['rid']
    print(rid)
    response = client.get("/review/get",
                          params = {'rid': rid})
    assert response.status_code == SUCCESS
    assert response.json()['rid'] == rid
    assert response.json()['type'] == package['rating']
    assert response.json()['comment'] == package['comment']
    assert response.json()['reviewer'] == "2"

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
        'comment': "edited"
    }
    response = client.post("/review/edit",
                             headers={"Authorization": f"Bearer "},
                             json=package)
    assert response.status_code == AUTHENTICATION_ERROR

def test_edit_review_bad_review(simple_user):
    '''
        Test whether invalid review is caught
    '''
    data = simple_user
    package = {
        'rid': '0',
        'rating' : 'positive',
        'comment': "edited"
    }
    response = client.post("/review/edit",
                             headers={"Authorization": f"Bearer {data['u_token']}"},
                             json=package)
    assert response.status_code == MISSING_ERROR

def test_edit_review_not_reviewer(simple_user):
    '''
        Test whether guest user attempting delete is caught
    '''
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
        'rid': '0',
        'rating' : 'positive',
        'comment': "Way better than mid"
    }
    response = client.post("/review/edit",
                             headers={"Authorization": f"Bearer {data['c_token']}"},
                             json=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_edit_review_successful(simple_user):
    '''
        Test whether guest user attempting edit is caught
    '''
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
        'rid': '0',
        'rating' : 'positive',
        'comment': "Way better than mid"
    }
    response = client.post("/review/edit",
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
    assert response.json()['reviews'][0]['comment'] == package['comment']

    rid = response.json()['reviews'][0]['rid']
    response = client.get("/review/get",
                          params = {'rid': rid})
    assert response.status_code == SUCCESS
    assert response.json()['rid'] == rid
    assert response.json()['type'] == package['rating']
    assert response.json()['comment'] == package['comment']
    assert response.json()['reviewer'] == "2"

def test_edit_review_successful_admin(simple_user):
    '''
        Test whether admin editing review is successful
    '''
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

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    package = {
        'rid': '0',
        'rating' : 'positive',
        'comment': "Way better than mid"
    }
    response = client.post("/review/edit",
                             headers={"Authorization": f"Bearer {access_token}"},
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
    assert response.json()['reviews'][0]['comment'] == package['comment']

    rid = response.json()['reviews'][0]['rid']
    response = client.get("/review/get",
                          params = {'rid': rid})
    assert response.status_code == SUCCESS
    assert response.json()['rid'] == rid
    assert response.json()['type'] == package['rating']
    assert response.json()['comment'] == package['comment']
    assert response.json()['reviewer'] == "2"

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
    assert response.json()['reviews'][0]['type'] == 'positive'

def test_admin_get_reviews_user(simple_user):
    '''
        Test non-admin
    '''
    data = simple_user
    response = client.get("/admin/get/reviews",
                            headers={"Authorization": f"Bearer {data['u_token']}"})
    assert response.status_code == FORBIDDEN_ERROR

def test_admin_get_reviews_wrong_filter(simple_user):
    '''
        Test whether positive review is registered
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'positive',
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
    response = client.get("/admin/get/reviews",
                          headers={"Authorization": f"Bearer {access_token}"},
                          params={})
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1

def test_admin_get_reviews(simple_user):
    '''
        Test whether positive review is registered
    '''
    data = simple_user

    package = {
        'sid': data['sid'],
        'rating': 'positive',
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
    response = client.get("/admin/get/reviews",
                          headers={"Authorization": f"Bearer {access_token}"},
                          params={})
    assert response.status_code == SUCCESS
    assert len(response.json()['reviews']) == 1
    assert response.json()['reviews'][0]['rid'] == '0'
    assert response.json()['reviews'][0]['service'] == data['sid']
    assert response.json()['reviews'][0]['type'] == 'positive'

def test_upvote_non_existent(simple_user):
    '''
        Test whether an upvote on a non-existent review is caught
    '''
    data = simple_user
    package = {
        'rid': '999'
    }
    response = client.post("/review/upvote",
                           headers={"Authorization": f"Bearer {data['u_token']}"},
                           json=package)
    assert response.status_code == MISSING_ERROR

def test_upvote_self(simple_user):
    '''
        Test whether upvoting self-review is valid
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.post("/review/upvote",
                           headers={"Authorization": f"Bearer {data['u_token']}"},
                           json=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_upvote_success(simple_user):
    '''
        Test whether upvoting a review works
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.post("/review/upvote",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

def test_upvote_twice(simple_user):
    '''
        Test whether upvoting twice is disallowed
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.post("/review/upvote",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    response = client.post("/review/upvote",
                        headers={"Authorization": f"Bearer {data['c_token']}"},
                        json=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_downvote_non_existent(simple_user):
    '''
        Test whether an downvote on a non-existent review is caught
    '''
    data = simple_user
    package = {
        'rid': '999'
    }
    response = client.post("/review/downvote",
                           headers={"Authorization": f"Bearer {data['u_token']}"},
                           json=package)
    assert response.status_code == MISSING_ERROR

def test_downvote_self(simple_user):
    '''
        Test whether downvoting self-review is valid
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.post("/review/downvote",
                           headers={"Authorization": f"Bearer {data['u_token']}"},
                           json=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_downvote_success(simple_user):
    '''
        Test whether downvoting a review works
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.post("/review/downvote",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

def test_downvote_twice(simple_user):
    '''
        Test whether downvoting twice is disallowed
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.post("/review/downvote",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    response = client.post("/review/downvote",
                        headers={"Authorization": f"Bearer {data['c_token']}"},
                        json=package)
    assert response.status_code == FORBIDDEN_ERROR

    # Try switch votes directly
    response = client.post("/review/upvote",
                    headers={"Authorization": f"Bearer {data['c_token']}"},
                    json=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_remove_vote_no_review(simple_user):
    '''
        Test removing vote from non-existent review
    '''
    data = simple_user
    package = {
        'rid': '999'
    }
    response = client.post("/review/remove_vote",
                           headers={"Authorization": f"Bearer {data['u_token']}"},
                           json=package)
    assert response.status_code == MISSING_ERROR

def test_remove_vote_not_voted(simple_user):
    '''
        Test removing vote when not voted
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.post("/review/remove_vote",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == INPUT_ERROR

def test_remove_vote_success(simple_user):
    '''
        Test removing vote susccessfuly
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.post("/review/downvote",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    response = client.get("/review/get",
                           params=package)
    assert response.status_code == SUCCESS
    assert response.json()['downvotes'] == 1

    response = client.post("/review/remove_vote",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    response = client.get("/review/get",
                           params=package)
    assert response.status_code == SUCCESS
    assert response.json()['downvotes'] == 0

def test_reply_non_existent(simple_user):
    '''
        Test replying to non-existent review
    '''
    data = simple_user

    package = {
        'rid': '999',
        'content': 'blah blah blah'
    }
    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['u_token']}"},
                           json=package)
    assert response.status_code == MISSING_ERROR

def test_reply_not_owner(simple_user):
    '''
        Test replying to review not as owner
    '''
    data = simple_user

    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': 'blah blah blah'
    }
    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['u_token']}"},
                           json=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_reply_blank_content(simple_user):
    '''
        Test replying with no content
    '''
    data = simple_user

    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': ''
    }
    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == INPUT_ERROR

def test_reply_successful(simple_user):
    '''
        Test successful review reply
    '''
    data = simple_user

    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': 'blah blah blah'
    }
    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    response = client.get("/review/get",
                           params={'rid' : 0})
    assert response.status_code == SUCCESS
    assert response.json()['reply'] == '0'

def test_reply_twice(simple_user):
    '''
        Test trying to reply to review twice
    '''
    data = simple_user

    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': 'blah blah blah'
    }
    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    response = client.get("/review/get",
                           params={'rid' : 0})
    assert response.status_code == SUCCESS
    assert response.json()['reply'] == '0'

    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_delete_reply_nonexistent(simple_user):
    '''
        Test trying to delete non-existent reply
    '''
    data = simple_user
    package = {
        'rid': '999'
        }

    response = client.delete("/review/reply/delete",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           params=package)
    assert response.status_code == MISSING_ERROR

def test_delete_reply_not_owner(simple_user):
    '''
        Test trying to delete reply not as owner
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': 'blah blah blah'
    }
    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.delete("/review/reply/delete",
                            headers={"Authorization": f"Bearer {data['u_token']}"},
                            params=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_delete_reply_success(simple_user):
    '''
        Test trying to delete reply
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': 'blah blah blah'
    }
    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.delete("/review/reply/delete",
                            headers={"Authorization": f"Bearer {data['c_token']}"},
                            params=package)
    assert response.status_code == SUCCESS
    response = client.get("/review/get",
                           params={'rid' : 0})
    assert response.status_code == SUCCESS
    assert response.json()['reply'] == None

def test_edit_reply_no_reply(simple_user):
    '''
        Test editing a non-existent reply
    '''
    data = simple_user

    package = {
        'rid': '999',
        'content': 'blah blah blah'
    }
    response = client.post("/review/reply/edit",
                           headers={"Authorization": f"Bearer {data['u_token']}"},
                           json=package)
    assert response.status_code == MISSING_ERROR

def test_edit_reply_not_owner(simple_user):
    '''
        Test editing a reply not as owner
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': 'blah blah blah'
    }
    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': 'less less less'
    }
    response = client.post("/review/reply/edit",
                            headers={"Authorization": f"Bearer {data['u_token']}"},
                            json=package)
    assert response.status_code == FORBIDDEN_ERROR

def test_edit_reply_blank(simple_user):
    '''
        Test editing a reply with blank content
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': 'blah blah blah'
    }
    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': ''
    }
    response = client.post("/review/reply/edit",
                            headers={"Authorization": f"Bearer {data['c_token']}"},
                            json=package)
    assert response.status_code == INPUT_ERROR

def test_edit_reply_success(simple_user):
    '''
        Test editing a reply successfully
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': 'blah blah blah'
    }
    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': 'yada yada yada'
    }
    response = client.post("/review/reply/edit",
                            headers={"Authorization": f"Bearer {data['c_token']}"},
                            json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.get("/review/reply/get",
                          params=package)
    assert response.status_code == SUCCESS
    assert response.json()['comment'] == 'yada yada yada'

def test_get_reply_404(simple_user):
    '''
        Test reply not existing
    '''
    package = {
        'rid': '0'
    }
    response = client.get("/review/reply/get",
                          params=package)
    assert response.status_code == MISSING_ERROR

def test_get_reply_success(simple_user):
    '''
        Test getting a rpely successfully
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': 'blah blah blah'
    }
    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0'
    }
    response = client.get("/review/reply/get",
                          params=package)
    assert response.status_code == SUCCESS
    assert response.json()['comment'] == 'blah blah blah'

def test_user_get_replies_success(simple_user):
    '''
        Test whether unknown user is caught
    '''
    data = simple_user
    package = {
            'sid': data['sid'],
            'rating': 'positive',
            'comment': 'Mid at best'
        }
    response = client.post("/service/review/add",
                headers={"Authorization": f"Bearer {data['u_token']}"},
                json=package)
    assert response.status_code == SUCCESS

    package = {
        'rid': '0',
        'content': 'blah blah blah'
    }
    response = client.post("/review/reply",
                           headers={"Authorization": f"Bearer {data['c_token']}"},
                           json=package)
    assert response.status_code == SUCCESS

    response = client.get("/user/get/replies",
                          headers={"Authorization": f"Bearer {data['c_token']}"})
    assert response.status_code == SUCCESS
    assert response.json()['replies'][0]['comment'] == 'blah blah blah'