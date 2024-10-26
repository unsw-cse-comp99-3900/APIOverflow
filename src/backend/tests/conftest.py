# from pathlib import Path
import os
import pytest
# from dotenv import load_dotenv
# def pytest_runtest_setup(item):
#     if item.fspath.basename != "test_email.py":
#         os.environ["EMAIL"] = "False"
os.environ["EMAIL"] = "False"
# # Define and resolve the path to .env
# ENV_FILE_PATH = Path(__file__).parent.parent / '.env'

# @pytest.fixture(autouse=True)
# def modify_env_file(request):

#     test_file_name = request.module.__name__
#     print(test_file_name)
#     if test_file_name == 'test_email':
#         yield

#     env_path = ENV_FILE_PATH.resolve()
    
#     if not env_path.is_file():
#         raise FileNotFoundError(f".env file not found at {env_path}")

#     with open(env_path, 'r') as f:
#         original_content = f.read()

#     modified_content = original_content.replace("EMAIL=True", "EMAIL=False")
#     with open(env_path, 'w') as f:
#         f.write(modified_content)
#     load_dotenv(dotenv_path=env_path)

#     yield
#     with open(env_path, 'w') as f:
#         f.write(original_content)
#     load_dotenv(dotenv_path=env_path)

# @pytest.fixture(autouse=True)
# def modify_env_file_2(request):

#     test_file_name = request.module.__name__
#     print(test_file_name)
#     if test_file_name == 'test_email':
#         yield

#     env_path = ENV_FILE_PATH.resolve()
    
#     if not env_path.is_file():
#         raise FileNotFoundError(f".env file not found at {env_path}")

#     with open(env_path, 'r') as f:
#         original_content = f.read()

#     modified_content = original_content.replace("EMAIL=True", "EMAIL=False")
#     with open(env_path, 'w') as f:
#         f.write(modified_content)
#     load_dotenv(dotenv_path=env_path)

#     yield
#     with open(env_path, 'w') as f:
#         f.write(original_content)
#     load_dotenv(dotenv_path=env_path)

# from dotenv import load_dotenv
# load_dotenv() 
# @pytest.fixture(autouse=True)
# def set_email_env(request):
#     test_file_name = request.module.__name__
#     if test_file_name == 'test_email':
#         yield
#     os.environ["EMAIL"] = "False"
#     yield

# def load_email_setting():
#     os.environ["EMAIL"] = "False"
#     return os.getenv("EMAIL") == "True"
# print(os.getenv("EMAIL"))

# email = load_email_setting()

# print(email)

# load_dotenv() 
# print(os.getenv("EMAIL"))
# os.environ["EMAIL"] = "False"
# print(os.getenv("EMAIL"))

# load_dotenv()
# print(os.getenv("EMAIL"))
# os.environ["EMAIL"] = "False"
# def load_email_setting():
#     return os.getenv("EMAIL") == "True"
# email = load_email_setting()
# print(email)
