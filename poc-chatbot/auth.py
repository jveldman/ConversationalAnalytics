import os 
import jwt

CUBEJS_API_SECRET = os.getenv("CUBEJS_API_SECRET")

def get_cube_token(): 
    payload = {}
    return jwt.encode(payload, CUBEJS_API_SECRET, algorithm = "HS256")