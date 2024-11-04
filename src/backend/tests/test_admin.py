import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.app import app 
from src.backend.classes.models import db
from src.backend.classes.datastore import data_store

# Create a test client
client = TestClient(app)

INPUT_ERROR = 400
AUTHENTICATION_ERROR = 401
SUCCESS = 200
NOT_FOUND = 404
NOT_AUTH = 403


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

    yield usable_data
    clear_all()

def test_super_admin(simple_user):
    '''
        Test whether super admin is created
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.get("/auth/admin", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS
    assert response.json() == {"message": "Welcome, Admin!"}

def test_promotion(simple_user):
    '''
        Test promoting a user
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.post("/admin/promote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == SUCCESS
    assert response.json() == {"name": "Tester 1", "status": True}

    # Success access after promotion
    response = client.get("/auth/admin", headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    assert response.json() == {"message": "Welcome, Admin!"}

    response = client.post("/admin/demote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == SUCCESS
    assert response.json() == {"name": "Tester 1", "status": True}

    # Can't access after demotion
    response = client.get("/auth/admin", headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == NOT_AUTH
    assert response.json() == {"detail": "Not authorized"}

def test_demotion(simple_user):
    '''
        Test demoting a user
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.post("/admin/promote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == SUCCESS
    assert response.json() == {"name": "Tester 1", "status": True}

    # Success access before demotion
    response = client.get("/auth/admin", headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == SUCCESS
    assert response.json() == {"message": "Welcome, Admin!"}

    response = client.post("/admin/demote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == SUCCESS
    assert response.json() == {"name": "Tester 1", "status": True}

    # Can't access after demotion
    response = client.get("/auth/admin", headers={"Authorization": f"Bearer {simple_user['token']}"})
    assert response.status_code == NOT_AUTH
    assert response.json() == {"detail": "Not authorized"}

def test_demotion_user(simple_user):
    '''
        Test demoting a user
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.post("/admin/demote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == INPUT_ERROR
    assert response.json() == {"detail": "User Tester 1 is not an admin."}
    

def test_delete_user(simple_user):
    '''
        Test deleting a user
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.get("/admin/dashboard/users", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS
    assert response.json()["user_count"] == 2

    response = client.delete("/admin/delete/user", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == SUCCESS
    assert response.json() == {"name": "Tester 1", "deleted": True}

    response = client.get("/admin/dashboard/users", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS
    assert response.json()["user_count"] == 1

def test_admin_delete_self(simple_user):
    '''
        Test promoting a user
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.post("/admin/promote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == SUCCESS
    assert response.json() == {"name": "Tester 1", "status": True}

    response = client.post("/admin/demote", headers={"Authorization": f"Bearer {simple_user['token']}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == NOT_AUTH

    response = client.post("/admin/demote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : '0'
                            })
    assert response.status_code == NOT_AUTH

def test_admin_demote_self(simple_user):
    '''
        Test promoting a user
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.post("/admin/promote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == SUCCESS
    assert response.json() == {"name": "Tester 1", "status": True}

    response = client.delete("/admin/delete/user", headers={"Authorization": f"Bearer {simple_user['token']}"},
                            params={
                              'uid' : '0'
                            })
    assert response.status_code == NOT_AUTH

def test_admin_delete_super(simple_user):
    '''
        Test promoting a user
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.post("/admin/promote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == SUCCESS
    assert response.json() == {"name": "Tester 1", "status": True}

    response = client.delete("/admin/delete/user", headers={"Authorization": f"Bearer {simple_user['token']}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == NOT_AUTH

    response = client.delete("/admin/delete/user", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : '0'
                            })
    assert response.status_code == NOT_AUTH

def test_admin_demote_super(simple_user):
    '''
        Test promoting a user
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.post("/admin/promote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == SUCCESS
    assert response.json() == {"name": "Tester 1", "status": True}

    response = client.post("/admin/demote", headers={"Authorization": f"Bearer {simple_user['token']}"},
                            params={
                              'uid' : '0'
                            })
    assert response.status_code == NOT_AUTH

def test_admin_delete_admin(simple_user):
    '''
        Test promoting a user
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.post("/admin/promote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == SUCCESS
    assert response.json() == {"name": "Tester 1", "status": True}

    user_creds2 = {
        "username" : "Tester 2",
        "password" : "password22",
        "email": "doxx22ed@gmail.com"
    }
    response = client.post("/auth/register", json=user_creds2)
    assert response.status_code == SUCCESS
    uid2 = response.json()['uid']

    response = client.post("/admin/promote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : uid2
                            })
    assert response.status_code == SUCCESS

    response = client.delete("/admin/delete/user", headers={"Authorization": f"Bearer {simple_user['token']}"},
                            params={
                              'uid' : uid2
                            })
    assert response.status_code == NOT_AUTH

def test_admin_demote_admin(simple_user):
    '''
        Test promoting a user
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.post("/admin/promote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == SUCCESS
    assert response.json() == {"name": "Tester 1", "status": True}

    user_creds2 = {
        "username" : "Tester 2",
        "password" : "password22",
        "email": "doxx22ed@gmail.com"
    }
    response = client.post("/auth/register", json=user_creds2)
    assert response.status_code == SUCCESS
    uid2 = response.json()['uid']

    response = client.post("/admin/promote", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : uid2
                            })
    assert response.status_code == SUCCESS

    response = client.post("/admin/demote", headers={"Authorization": f"Bearer {simple_user['token']}"},
                            params={
                              'uid' : uid2
                            })
    assert response.status_code == NOT_AUTH
    assert response.json() == {"detail": "Admins cannot demote other Admins."}

def test_admin_check_dashboard(simple_user):
    '''
        Test promoting a user
    '''
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]
    
    user0 = data_store.get_user_by_id("0")
    user1 = data_store.get_user_by_id(simple_user['uid'])
    user_creds2 = {
        "username" : "Tester 2",
        "password" : "password22",
        "email": "doxx22ed@gmail.com"
    }
    response = client.post("/auth/register", json=user_creds2)
    assert response.status_code == SUCCESS
    uid2 = response.json()['uid']
    user2 = data_store.get_user_by_id(uid2)

    user_creds3 = {
        "username" : "Tester 3",
        "password" : "password33",
        "email": "doxx33ed@gmail.com"
    }
    response = client.post("/auth/register", json=user_creds3)
    assert response.status_code == SUCCESS
    uid3 = response.json()['uid']
    user3 = data_store.get_user_by_id(uid3)

    response = client.get("/admin/dashboard/users", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS
    assert response.json()["user_count"] == 4
    assert response.json()["users"] == [user0.to_json(), user1.to_json(), user2.to_json(), user3.to_json()]

    response = client.delete("/admin/delete/user", headers={"Authorization": f"Bearer {access_token}"},
                            params={
                              'uid' : simple_user['uid']
                            })
    assert response.status_code == SUCCESS

    response = client.get("/admin/dashboard/users", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == SUCCESS
    assert response.json()["user_count"] == 3
    assert response.json()["users"] == [user0.to_json(), user2.to_json(), user3.to_json()]

def test_admin_filter_standard_users(simple_user):
    '''
        Testing standard user filter
    '''

    user_creds2 = {
        "username" : "Tester 2",
        "password" : "password22",
        "email": "doxx22ed@gmail.com"
    }
    response = client.post("/auth/register", json=user_creds2)
    assert response.status_code == SUCCESS
    uid2 = response.json()['uid']
    user2 = data_store.get_user_by_id(uid2)

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.get("admin/filter_users", headers={"Authorization": f"Bearer {access_token}"},
                          params={
                              'standard': True,
                              'admin': False,
                              'super': False
                          })
    
    assert response.status_code == SUCCESS 
    assert len(response.json()) == 2

def test_admin_filter_admin_users(simple_user):
    '''
        Testing admin user filter
    '''

    user_creds2 = {
        "username" : "Tester 2",
        "password" : "password22",
        "email": "doxx22ed@gmail.com"
    }
    response = client.post("/auth/register", json=user_creds2)
    assert response.status_code == SUCCESS
    uid2 = response.json()['uid']
    user2 = data_store.get_user_by_id(uid2)

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.get("admin/filter_users", headers={"Authorization": f"Bearer {access_token}"},
                          params={
                              'standard': False,
                              'admin': True,
                              'super': False
                          })
    
    assert response.status_code == SUCCESS 
    assert len(response.json()) == 1

def test_admin_filter_super_users(simple_user):
    '''
        Testing super user filter
    '''

    user_creds2 = {
        "username" : "Tester 2",
        "password" : "password22",
        "email": "doxx22ed@gmail.com"
    }
    response = client.post("/auth/register", json=user_creds2)
    assert response.status_code == SUCCESS
    uid2 = response.json()['uid']
    user2 = data_store.get_user_by_id(uid2)

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.get("admin/filter_users", headers={"Authorization": f"Bearer {access_token}"},
                          params={
                              'standard': False,
                              'admin': False,
                              'super': True
                          })
    
    assert response.status_code == SUCCESS 
    assert len(response.json()) == 1

def test_admin_filter_duplicates(simple_user):
    '''
        Testing no duplicates
    '''

    user_creds2 = {
        "username" : "Tester 2",
        "password" : "password22",
        "email": "doxx22ed@gmail.com"
    }
    response = client.post("/auth/register", json=user_creds2)
    assert response.status_code == SUCCESS
    uid2 = response.json()['uid']
    user2 = data_store.get_user_by_id(uid2)

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.get("admin/filter_users", headers={"Authorization": f"Bearer {access_token}"},
                          params={
                              'standard': False,
                              'admin': True,
                              'super': True
                          })
    
    assert response.status_code == SUCCESS 
    print(response.json())
    assert len(response.json()) == 1

def test_admin_filter_overlapping_users(simple_user):
    '''
        Testing overlap
    '''

    user_creds2 = {
        "username" : "Tester 2",
        "password" : "password22",
        "email": "doxx22ed@gmail.com"
    }
    response = client.post("/auth/register", json=user_creds2)
    assert response.status_code == SUCCESS
    uid2 = response.json()['uid']
    user2 = data_store.get_user_by_id(uid2)

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    assert response.status_code == SUCCESS
    access_token = response.json()["access_token"]

    response = client.get("admin/filter_users", headers={"Authorization": f"Bearer {access_token}"},
                          params={
                              'standard': True,
                              'admin': False,
                              'super': True
                          })
    
    assert response.status_code == SUCCESS 
    assert len(response.json()) == 3