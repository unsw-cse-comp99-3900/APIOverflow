import pytest
from service import Service
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app import app 

# Create a test client
client = TestClient(app)

