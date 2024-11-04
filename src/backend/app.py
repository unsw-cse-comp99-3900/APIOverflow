from fastapi import FastAPI, Depends, Request, HTTPException, Query, UploadFile, File, Form, Body
from fastapi_login import LoginManager
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from src.backend.classes.models import *
from src.backend.server.service import *
from src.backend.classes.datastore import data_store as ds
from src.backend.server.auth import *
from src.backend.classes.Manager import manager as _manager
from src.backend.database import db
from src.backend.server.tags import *
from src.backend.server.admin import *
from src.backend.server.upload import *
from src.backend.server.user import *
from src.backend.server.review import *
from json import dumps


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

manager = _manager.get_manager()

#####################################
#   Helper Functions
#####################################
def admin_required():
    '''
        Used to verify that the user is an admin
    '''
    def admin_checker(user=Depends(manager)):
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        if not user["is_admin"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        return user

    return admin_checker

#####################################
#   Misc Paths
#####################################
@app.get("/")
async def home():
    return {
        "message": "Welcome to the MongoDB Auth System.",
        "login_link": "/auth/login",
        "register_link": "/auth/register"
    }

# todo: auth gate this so that endpoint is private
@app.post("/testing/clear")
async def clear():
    '''
        Internal Testing function to clear datastore
    '''
    ds.clear_datastore()
    clear_all_users()
    clear_all_services()
    create_super_admin()
    assert ds.num_apis() == 0
    return {"message" : "Clear Successful"}

@app.post("/upload/pdfs")
async def upload_pdf(file: UploadFile = File(...)):
    '''
        Endpoint to upload pdf files
    '''
    doc_id = await upload_pdf_wrapper(file)
    return {'doc_id': doc_id}

@app.post("/upload/imgs")
async def upload_image(file: UploadFile = File(...)):
    '''
        Endpoint to upload image files (will only support JPEG/JPG and PNG)
    '''
    doc_id = await upload_img_wrapper(file)
    return {'doc_id': doc_id}

#####################################
#   Service Paths
#####################################
@app.post("/service/add")
async def add_service(service: ServicePost, user: User = Depends(manager)):
    '''
        Method used to add service to platform
    '''
    # Unpack request body
    request = service.model_dump()
    uid = user['id']
    id = add_service_wrapper(request, str(uid))
    return {'id' : id}


@app.get("/service/get_service")
async def get_service(sid: str):
    '''
        Method to retrieve a particular service
    '''
    response = get_service_wrapper(sid)
    return response

@app.put("/service/update")
async def update_service(service: ServiceUpdate, user: User = Depends(manager)):
    '''
        Method used to update service to platform
    '''

    request = service.model_dump()
    uid = user['id']
   
    update_service_wrapper(request, str(uid))
    return None

@app.get("/service/apis")
async def view_apis():
    return list_nonpending_apis()

@app.post("/service/upload_docs")
async def upload_docs(info: ServiceUpload, user: User=Depends(manager)):
    '''
        Method to upload documententation to service
    '''
    request = info.model_dump()
    sid = request['sid']
    doc_id = request['doc_id']
    await upload_docs_wrapper(sid, user['id'], doc_id)
    return 200

@app.get("/service/my_services")
async def get_user_apis(user: User = Depends(manager)):
    '''
        Method to get the list of APIs owned by the currently authenticated user.
        Returns a list of APIs with specific fields: id, name, owner, description, icon_url, and tags.
    '''
    uid = user['id']
    user_apis = ds.get_user_apis(uid)
    return user_apis

@app.get("/service/filter")
async def filter(
    tags: Optional[List[str]] = Query(None), 
    providers: Optional[List[str]] = Query(None),
    hide_pending: bool = True
):
    return api_tag_filter(tags, providers, hide_pending)

@app.get("/service/search")
async def search(
    name: Optional[str] = Query(None),
    hide_pending: bool = True,
):
    return api_name_search(name, hide_pending)

@app.delete("/service/delete")
async def delete_api(sid: str):
    """
        Delete an API service by its service id (id).
    """
    return delete_service(sid)

@app.post("/service/add_icon")
async def api_add_icon(info: ServiceIconInfo, user: User = Depends(manager)):
    '''
        Adds an icon to the service
    '''
    service_add_icon_wrapper(user['id'], info.sid, info.doc_id)

@app.delete("/service/delete_icon")
async def api_delete_icon(info: Annotated[ServiceIconDeleteInfo, Query()], user: User = Depends(manager)):
    '''
        Deletes an icon from the service
    '''
    service_delete_icon_wrapper(user['id'], info.sid)

@app.get("/service/get/icon")
async def api_get_icon(sid: str):
    '''
        Retrieves service icon as image file
    '''
    return service_get_icon_wrapper(sid)

@app.post("/service/review/add")
async def api_add_review(info: ServiceReviewInfo, user : User = Depends(manager)):
    '''
        Endpoint to add review to a service
    '''
    service_add_review_wrapper(user['id'], info)


@app.get("/service/get/rating")
async def api_get_rating(sid: str):
    '''
        Endpoint to retrieve a service's rating
    '''
    return service_get_rating_wrapper(sid)

@app.get("/service/get/reviews")
async def api_get_reviews(sid: str, testing: bool = False):
    '''
        Endpoint to retrieve a service's reviews
    '''
    return {
        'reviews' : service_get_reviews_wrapper(sid, testing)
    } 

@app.get("/get/doc")
async def get_doc(doc_id: str):
    '''
        Endpoint which directly returns a file requested
    '''
    return get_doc_wrapper(doc_id)

#####################################
#   Review Paths
#####################################

@app.get("/review/get")
async def review_get(rid: str):
    '''
        Endpoint which directly retrieves a review
    '''
    return review_get_wrapper(rid)

@app.delete("/review/delete")
async def review_delete(rid: str, user: User = Depends(manager)):
    '''
        Endpoint which deletes a given review
    '''
    review_delete_wrapper(rid, user['id'], user['is_admin'])

@app.post("/review/edit")
async def review_edit(info: ServiceReviewEditInfo, user: User = Depends(manager)):
    '''
        Endpoint which edits a given review
    '''
    review_edit_wrapper(info, user['id'], user['is_admin'])

@app.post("/review/approve")
async def review_approve(info: ServiceReviewAdminAction, user: User = Depends(manager), role: str = Depends(admin_required())):
    '''
        Endpoint which approves a review
    '''
    review_approve_wrapper(info.rid, info.reason)

@app.post("/review/reject")
async def review_reject(info: ServiceReviewAdminAction, user: User = Depends(manager), role: str = Depends(admin_required())):
    '''
        Endpoint which rejects a review
    '''
    review_reject_wrapper(info.rid, info.reason)

#####################################
#   Auth Paths
#####################################
@app.post("/auth/register")
async def register(user: UserCreate):
    '''
        Register a user onto the platform
    '''
    uid = register_wrapper(user.displayname, user.username, user.password, user.email)
    return {'uid' : uid}

@app.post("/auth/login")
async def login(credentials: LoginModel):
    '''
        Login a user (or attempt to)
    '''
    username = credentials.username
    password = credentials.password
    access_token = login_wrapper(username, password)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/verify-email/{token}")
async def verify_email(token: str):
    '''
        Verify a user
    '''
    uid = verify_token(token)
    user = data_store.get_user_by_id(uid) 
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    user.verify_user()
    db_update_user(uid, user.to_json())
    return {"message": "Email verified successfully."}

@app.post("/auth/reset-password")
async def request_password_reset(user: User = Depends(manager)):
    '''
        Sends a password request
    '''
    uid = user['id']
    password_reset_request(uid)
    return {"message": "Password reset email sent."}

@app.post("/auth/reset-password/{token}")
async def reset_password_form(token: str, password: Password):
    '''
        Changes user password
    '''
    uid = verify_token(token)
    user = data_store.get_user_by_id(uid) 
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    change_password(uid, password.newpass)
    return {"message": "Password changed successfully."}

# Example privileged routes
@app.get("/auth/admin")
async def admin_route(user: User = Depends(manager), role: str = Depends(admin_required())):
    return {"message": "Welcome, Admin!"}

@app.get("/auth/service")
async def service_provider_route(user: User = Depends(manager)):
    return {"message": "Welcome, Service Provider!"}

@app.get("/auth/account")
async def account_user_route(user: User = Depends(manager)):
    return {"message": "Welcome, Account User!"}

@app.get("/auth/guest")
async def guest_route():
    return {"message": "Welcome, Guest!"}


#####################################
#   Tag Paths
#####################################

@app.post("/tag/add")
async def add_tag(tag: TagData, user: User = Depends(manager)):
    '''
        Endpoint to add a tag
    '''
    add_tag_wrapper(tag.tag)

@app.delete("/tag/delete")
async def delete_tag(tag: str, user: User = Depends(manager), role: str = Depends(admin_required())):
    '''
        Endpoint to delete a tag
    '''
    delete_tag_wrapper(tag)

@app.get("/tags/get")
async def get_tags():
    '''
        Endpoint to grab all tags
    '''
    return get_tags_wrapper()

#####################################
#   Admin Paths
#####################################

@app.get("/admin/dashboard/users")
async def get_users(user: User = Depends(manager), role: str = Depends(admin_required())):
    '''
        Endpoint to get all users
    '''
    return get_all_users()

@app.post("/admin/promote")
async def promote(uid: str, user: User = Depends(manager), role: str = Depends(admin_required())):
    '''
        Endpoint to promote given their id
    '''
    return promote_user(uid)

@app.post("/admin/demote")
async def demote(uid: str, user: User = Depends(manager), role: str = Depends(admin_required())):
    '''
        Endpoint to demote a user given their id
    '''
    return demote_user(uid, user["is_super"])

@app.delete("/admin/delete/user")
async def user_delete(uid: str, user: User = Depends(manager), role: str = Depends(admin_required())):
    '''
        Endpoint to delete a user given their id
    '''
    return delete_user(uid, user["is_super"])

@app.get("/admin/get/reviews")
async def admin_get_reviews(option: str = '', user: User = Depends(manager), role: str = Depends(admin_required())):
    '''
        Endpoint which retrieves all pending reviews
    '''
    return {
        'reviews': admin_get_reviews_wrapper(option)
    }

@app.get("/admin/get/services")
async def admin_get_services(option: str = "ALL_PENDING", user: User = Depends(manager), role: str = Depends(admin_required())):
    '''
        Endpoint which retrieves all pending services
    '''
    return {
        'services' : admin_get_pending_services(option)
    }

@app.post("/admin/service/approve")
async def admin_service_approve(info: ServiceApprove, user: User = Depends(manager), role: str = Depends(admin_required())):
    '''
        Endpoint which approves or disapproves a service
    '''
    approve_service_wrapper(info.sid, info.approved, info.reason)

@app.get("/admin/filter_users")
async def admin_user_filter(standard: bool, admin: bool, super: bool, user: User = Depends(manager), role: str = Depends(admin_required())):
    '''
        Endpoint which filters users depending on standard users, admins, or supers
    '''
    print(standard)
    print(admin)
    print(super)
    return admin_filter_users(standard, admin, super)

#####################################
#   User Paths
#####################################
@app.post("/user/add_icon")
async def user_add_icon(doc: DocumentID, user: User=Depends(manager)):
    '''
        Endpoint to add an icon to a user
    '''
    user_add_icon_wrapper(user['id'], doc.doc_id)


@app.delete("/user/delete_icon")
async def user_delete_icon(user: User=Depends(manager)):
    '''
        Endpoint to delete user icon
    '''
    user_delete_icon_wrapper(user['id'])

@app.get("/user/get")
async def user_get(user: User=Depends(manager)):
    '''
        Endpoint which retrieves user information
    '''
    return user_get_wrapper(user['id'])

@app.get("/user/get/icon")
async def user_get_icon(user: User=Depends(manager)):
    '''
        Endpoint which retrieves user's icon (if one exists)
    '''
    return user_get_icon_wrapper(user['id'])

@app.get("/user/get/reviews")
async def user_get_reviews(user: User=Depends(manager)):
    '''
        Endpoint which retrieves all reviews user has made
    '''
    return {
        'reviews' : user_get_reviews_wrapper(user['id'])
    }

@app.get("/user/get/profile")
async def user_get_profile(user: User = Depends(manager)):
    '''
        Endpoint which retrieves profile information of user
    '''
    return user_get_profile_wrapper(user['id'])

@app.delete("/user/delete/me")
async def delete_user_self(user: User = Depends(manager)):
    '''
        Endpoint which allows the user to un-register themselves
    '''
    return user_self_delete(user['id'])

@app.post("/user/update/displayname")
async def update_user_displayname(new_displayname: GeneralString, user: User = Depends(manager)):
    '''
        Endpoint which allows the user to update their displayname
    '''
    return user_update_displayname(user['id'], new_displayname.content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
    # Run using uvicorn app:app --reload

