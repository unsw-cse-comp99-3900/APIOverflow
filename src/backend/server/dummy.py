import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.classes.models import db
from src.backend.classes.datastore import data_store as ds
from src.backend.classes.Endpoint import Endpoint
from src.backend.classes.Parameter import Parameter 
from src.backend.classes.Response import Response
from src.backend.server.tags import *
from src.backend.server.admin import *
from src.backend.server.upload import *
from src.backend.server.user import *
from src.backend.server.review import *
from src.backend.classes.models import *
from src.backend.server.service import *
from src.backend.server.auth import *

simple_parameter = Parameter(id="1", endpoint_link='https://api.example.com/users/12345', required=True, 
                            type='HEADER', name='paramtest', value_type='int')
simple_response = Response(code='404', description='not found', conditions=["site is down", "badtest"], 
                            example="example...")
simple_endpoint = Endpoint(link='https://api.example.com/users/12345', title_description='testTitle1', 
                            main_description='tests endpoint', tab='tabTest', parameters=[simple_parameter], 
                            method="POST", responses=[simple_response])

def import_dummy_data():

    if data_store.num_users() == 0:
        create_super_admin()
    superadmin = data_store.get_user_by_id("0")

    user1 = User(str(data_store.max_num_users()),
                    "user1",
                    "user1",
                    manager.hash_password("user1password"),
                    "1183471112e@gmail.com",
                    True,
                    True)
    user1.verify_user()
    db_add_user(user1.to_json())
    data_store.add_user(user1)

    api_info1 = {
                'name' : 'Test API',
                'icon_url' : '',
                'x_start' : 0,
                'x_end' : 0,
                'y_start' : 0,
                'y_end' : 0,
                'description' : 'This is a test API',
                'tags' : ['API'],
                'endpoints': [simple_endpoint.dict()]
                }

    service1 = ServiceAdd(
        name=api_info1['name'],
        icon_url=api_info1['icon_url'],
        x_start=api_info1['x_start'],
        x_end=api_info1['x_end'],
        y_start=api_info1['y_start'],
        y_end=api_info1['y_end'],
        description=api_info1['description'],
        tags=api_info1['tags'],
        endpoints=[Endpoint(**endpoint) for endpoint in api_info1['endpoints']]
    )
    request = service1.model_dump()
    sid = add_service_wrapper(request, superadmin)

    package = {
        'sid': sid,
        'rating': 'positive',
        'comment': 'Mid at best'
    }
    review1 = ServiceReviewInfo(
        sid=package['sid'],
        rating=package['rating'],
        comment=package['comment']
    )
    service_add_review_wrapper(user1.get_id(), review1)
