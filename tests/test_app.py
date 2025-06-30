import sys
import os
from app import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
def test_home():
    client = app.test_client()
    response = client.get("/")  # O cualquier endpoint que tengas
    assert response.status_code == 404 or response.status_code == 200
