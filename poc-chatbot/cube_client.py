# cube_client.py
import os
from typing import Dict, Any
from auth import get_cube_token
import requests
from dotenv import load_dotenv
import time

load_dotenv()

CUBE_API_SECRET = os.getenv("CUBEJS_API_SECRET")

CUBE_API_URL = os.getenv("CUBE_API_URL")

def execute_cube_query(query: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a Cube query against Cube Core and return the JSON result.
    Surfaces Cube's actual error message instead of a bare 400.
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": get_cube_token()
    }

    response = requests.post(
        f"{CUBE_API_URL}/load",
        json={"query": query}, 
        headers = headers, 
        timeout = 60
    )

    if "Continue wait" in str(response.content):
        time.sleep(2)
        response = requests.post(  # ← Just add "response ="
            f"{CUBE_API_URL}/load",
            json={"query": query},
            headers=headers,
            timeout=60
        )
        
    if not response.ok:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise ValueError(f"Cube API error ({response.status_code}): {detail}")

    return response.json()