
import os
import requests
from dotenv import load_dotenv
from auth import get_cube_token

load_dotenv()

CUBE_API_URL = os.getenv("CUBE_API_URL")

def execute_graphql_query(graphql_query: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Authorization": get_cube_token()
    }
    # Remove /cubejs-api/v1 from the base URL for GraphQL
    base_url = CUBE_API_URL.replace('/cubejs-api/v1', '')
    payload = {"query": graphql_query}

    response = requests.post(
        f"{base_url}/graphql",  
        json=payload,
        headers=headers,
        timeout=60
    )

    if not response.ok:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise ValueError(f"GraphQL API error ({response.status_code}): {detail}")

    return response.json()