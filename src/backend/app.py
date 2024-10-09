from fastapi import FastAPI, Depends, Request, HTTPException, Query, UploadFile, File, Form
from fastapi_login import LoginManager
from pymongo import MongoClient
from passlib.context import CryptContext
from src.backend.classes.models import *
from src.backend.server.service import *
from src.backend.classes.datastore import data_store as ds
from src.backend.server.auth import *
from src.backend.classes.Manager import manager as _manager
from src.backend.database import db

app = FastAPI()


manager = _manager.get_manager()

#####################################
#   Helper Functions
#####################################
def role_required(roles: Union[str, List[str]]):
    '''
        Used to verify dependency of user roles
    '''
    if isinstance(roles, str):
        roles = [roles]

    def role_checker(user=Depends(manager)):
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        if user["role"] not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        return user

    return role_checker

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

@app.post("/testing/clear")
async def clear():
    '''
        Internal Testing function to clear datastore
    '''
    ds.clear_datastore()
    clear_all_users()
    clear_all_services
    assert ds.num_apis() == 0
    return {"message" : "Clear Successful"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    '''
        Endpoint to upload files
    '''
    doc_id = await upload_wrapper(file)
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
    sid = add_service_wrapper(request, str(uid))
    return {'sid' : sid}

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

@app.get("/service/get_service")
async def get_service(sid: str):
    '''
        Method to retrieve a particular service
    '''
    response = get_service_wrapper(sid)
    return response

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
    
@app.get("/service/apis")
async def view_apis():
    return list_apis()

@app.get("/service/my_services")
async def get_user_apis(user: User = Depends(manager)):
    '''
        Method to get the list of APIs owned by the currently authenticated user.
        Returns a list of APIs with specific fields: id, name, owner, description, icon_url, and tags.
    '''
    uid = user['id']
    user_apis = ds.get_user_apis(uid)
    return user_apis

#####################################
#   Auth Paths
#####################################
@app.post("/auth/register")
async def register(user: UserCreate):
    '''
        Register a user onto the platform
    '''
    uid = register_wrapper(user.username, user.password, user.email, user.role)
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
async def admin_route(user: User = Depends(manager), role: str = Depends(role_required("admin"))):
    return {"message": "Welcome, Admin!"}

@app.get("/auth/service")
async def service_provider_route(user: User = Depends(manager), role: str = Depends(role_required("service provider"))):
    return {"message": "Welcome, Service Provider!"}

@app.get("/auth/account")
async def account_user_route(user: User = Depends(manager), role: str = Depends(role_required("account user"))):
    return {"message": "Welcome, Account User!"}

@app.get("/auth/guest")
async def guest_route(user: User = Depends(manager), role: str = Depends(role_required("guest"))):
    return {"message": "Welcome, Guest!"}

@app.get("/service/filter")
async def filter(
    tags: Optional[List[str]] = Query(None), 
    providers: Optional[List[str]] = Query(None)
):
    return api_tag_filter(tags, providers)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
    # Run using uvicorn app:app --reload

