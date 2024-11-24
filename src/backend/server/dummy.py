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

header_parameter = Parameter(
    id="2",
    endpoint_link='https://api.example.com/resources/67890',
    required=True,
    type='HEADER',
    name='AuthToken',
    value_type='string'
)

query_parameter = Parameter(
    id="3",
    endpoint_link='https://api.example.com/resources/67890',
    required=False,
    type='QUERY',
    name='filter',
    value_type='string'
)

body_parameter = Parameter(
    id="4",
    endpoint_link='https://api.example.com/resources/67890',
    required=True,
    type='BODY',
    name='data',
    value_type='json'
)

# Additional Responses
success_response = Response(
    code='200',
    description='Successful operation',
    conditions=["valid input", "authentication success"],
    example="{'message': 'Operation successful'}"
)

not_found_response = Response(
    code='404',
    description='Resource not found',
    conditions=["invalid resource ID", "deleted resource"],
    example="{'error': 'Resource not found'}"
)

# Endpoints with different methods
get_endpoint = Endpoint(
    link='https://api.example.com/resources/67890',
    title_description='Retrieve Resource',
    main_description='Fetch details of a specific resource by ID.',
    tab='ResourceTab',
    parameters=[header_parameter, query_parameter],
    method="GET",
    responses=[success_response, not_found_response]
)

delete_endpoint = Endpoint(
    link='https://api.example.com/resources/67890',
    title_description='Delete Resource',
    main_description='Delete a specific resource by ID.',
    tab='ResourceTab',
    parameters=[header_parameter],
    method="DELETE",
    responses=[success_response, not_found_response]
)

put_endpoint = Endpoint(
    link='https://api.example.com/resources/67890',
    title_description='Update Resource',
    main_description='Update the details of a specific resource.',
    tab='ResourceTab',
    parameters=[header_parameter, body_parameter],
    method="PUT",
    responses=[success_response, not_found_response]
)

post_endpoint = Endpoint(
    link='https://api.example.com/resources',
    title_description='Create Resource',
    main_description='Create a new resource with the provided data.',
    tab='ResourceTab',
    parameters=[header_parameter, body_parameter],
    method="POST",
    responses=[success_response]
)


def create_users(n):
    users = {}
    for i in range(1, n + 1):
        user = User(
            str(data_store.max_num_users() + i - 1),
            f"user{i}",
            f"user{i}",
            manager.hash_password(f"user{i}password"),
            f"user{i}@example.com",
            False,
            False
        )
        user.verify_user()
        db_add_user(user.to_json())
        data_store.add_user(user)

        users[f"user{i}"] = user
    return users

def import_dummy_data():

    if data_store.num_users() == 0:
        create_super_admin()
    superadmin = data_store.get_user_by_id("0")

    users = create_users(5)
    user1 = users["user1"]
    user2 = users["user2"]
    user2.promote_to_admin()
    user3 = users["user3"]
    user4 = users["user4"]
    user5 = users["user5"]
    user5.promote_to_admin()

    api_info1 = {
        'name': 'Test API',
        'description': 'This is a test API',
        'tags': ['API', 'Microservice'],
        'endpoints': [post_endpoint.model_dump()],
        'version_name': "v0.6.9",
        'version_description': "This is the initial version of the Test API",
        'pay_model': "Free"
    }

    api_info2 = {
        'name': 'User Management API',
        'description': 'API to manage user resources, including retrieval and deletion.',
        'tags': ['API', 'Users', 'Management'],
        'endpoints': [get_endpoint.model_dump(), delete_endpoint.model_dump()],
        'version_name': "v1.0",
        'version_description': "First release of the User Management API",
        'pay_model': "Premium"
    }

    api_info3 = {
        'name': 'Resource Update API',
        'description': 'API to update and create resources.',
        'tags': ['Microservices', 'Resources', 'Update', 'Creation'],
        'endpoints': [put_endpoint.model_dump(), post_endpoint.model_dump()],
        'version_name': "v1.2",
        'version_description': "Update to include PUT and POST methods",
        'pay_model': "Freemium"
        
    }

    api_info4 = {
        'name': 'Comprehensive Resource API',
        'description': 'Full-featured API for resource CRUD operations.',
        'tags': ['API', 'Resources', 'CRUD'],
        'endpoints': [
            get_endpoint.model_dump(),
            post_endpoint.model_dump(),
            put_endpoint.model_dump(),
            delete_endpoint.model_dump()
        ],
        'version_name': "v2.0",
        'version_description': "Comprehensive API with full CRUD support",
        'pay_model': 'Free'
    }

    api_infos = [api_info1, api_info2, api_info3, api_info4]

    for api_info in api_infos:
        for tag in api_info['tags']:
            data_store.add_tag(tag)
            
    services = [
        ServiceAdd(
            name=api_info['name'],
            description=api_info['description'],
            tags=api_info['tags'],
            endpoints=[Endpoint(**endpoint) for endpoint in api_info['endpoints']],
            version_name=api_info['version_name'],
            pay_model=api_info['pay_model']
        ) for api_info in api_infos
    ]

    service_requests = [service.model_dump() for service in services]

    sid1 = add_service_wrapper(service_requests[0], user1)
    approve_service(sid1, 'first api ever', True, api_info1)

    add_service_review(user2.get_id(), sid1, 'positive', 'it is ok')

    add_reply('0', 'why are you so mean to me', user1)

    api_info1_new_version = ServiceAddVersion(
        sid=sid1,
        version_name="v1.0.1",
        endpoints=[
            Endpoint(**endpoint) for endpoint in api_info3['endpoints']
        ],
        version_description="Major update with enhanced operations"
    )
    request_info1 = api_info1_new_version.model_dump()
    add_new_service_version_wrapper(request_info1)

    sid2 = add_service_wrapper(service_requests[0], user2)

    approve_service(sid2, 'someone already uploaded this', False, api_info1)
    
    sid3 = add_service_wrapper(service_requests[1], user3)
    sid4 = add_service_wrapper(service_requests[2], user4)
    sid5 = add_service_wrapper(service_requests[3], user5)

    approve_service(sid5, 'very unique service, approved', True, api_info4)


    add_service_review(user1.get_id(), sid5, 'positive', 'wow, very good')
    add_service_review(user2.get_id(), sid5, 'positive', 'this changed my life for the better')
    add_service_review(user3.get_id(), sid5, 'negative', 'overrated')
    add_reply('3', 'I am an admin and I will delete your account', user5)
    add_service_review(user4.get_id(), sid5, 'negative', '@superadmin')
    review_vote_wrapper('3', superadmin.get_id(), 'positive')
    review_vote_wrapper('3', user1.get_id(), 'positive')
    review_vote_wrapper('3', user2.get_id(), 'positive')

    api_info4_update_version = ServiceUpdateVersion(
        sid=sid5,
        version_name="v2.0",
        new_version_name="v2.5",
        endpoints=[
            Endpoint(**endpoint) for endpoint in api_info4['endpoints']
        ],
        version_description="Minor update to add support for all methods"
    )
    request_info4 = api_info4_update_version.model_dump()
    update_new_service_version_wrapper(request_info4)

def add_service_review(user_id, sid, rating, comment):
    package = {
        'sid': sid,
        'rating': rating,
        'comment': comment
    }
    review = ServiceReviewInfo(
        sid=package['sid'],
        rating=package['rating'],
        comment=package['comment']
    )
    service_add_review_wrapper(user_id, review)

def approve_service(sid, reason, approve, api_info):
    request = {
        'sid': sid,
        'reason': reason,
        'approved': approve,
        'version_name': api_info["version_name"],
        'service_global': True
    }
    approve_service_wrapper(sid=request["sid"],
                           approved=request["approved"],
                           reason=request["reason"],
                           service_global=request["service_global"],
                           version=request["version_name"]
                           )


def add_reply(rid, content, user):
    info = ReviewPackage(
        rid=rid,
        content=content
    )
    review_add_reply_wrapper(info.rid, user.get_id(), info.content)

