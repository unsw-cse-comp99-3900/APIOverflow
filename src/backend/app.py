from fastapi import FastAPI, Depends, Request, HTTPException, Query, UploadFile, File, Form
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

if ds.num_users() == 0:
    create_super_admin()

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
    # should this return any additional info?
    update_service_wrapper(request, str(uid))
    return None

@app.get("/service/apis")
async def view_apis():
    return list_apis()

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
    providers: Optional[List[str]] = Query(None)
):
    return api_tag_filter(tags, providers)

@app.get("/service/search")
async def search(
    name: Optional[str] = Query(None),
):
    return api_name_search(name)

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

#####################################
#   Auth Paths
#####################################
@app.post("/auth/register")
async def register(user: UserCreate):
    '''
        Register a user onto the platform
    '''
    uid = register_wrapper(user.username, user.password, user.email, user.is_admin)
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
async def guest_route(user: User = Depends(manager)):
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
    # Run using uvicorn app:app --reload

