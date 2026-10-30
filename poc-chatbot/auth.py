import os
import jwt
from dotenv import load_dotenv

load_dotenv()

CUBEJS_API_SECRET = os.getenv("CUBEJS_API_SECRET")


def get_cube_token() -> str:
    """Generate a Cube.js API token for authentication.
    
    Returns:
        JWT token for Cube.js API authentication
        
    Raises:
        RuntimeError: If CUBEJS_API_SECRET is not set
    """
    if not CUBEJS_API_SECRET:
        raise RuntimeError(
            "CUBEJS_API_SECRET environment variable is not set. "
            "Please set it in your .env file or environment."
        )
    payload = {}
    return jwt.encode(payload, CUBEJS_API_SECRET, algorithm="HS256")