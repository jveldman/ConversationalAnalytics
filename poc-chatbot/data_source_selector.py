# data_source_selector.py
"""
Module for selecting the appropriate Cube data source based on user needs.
This is a new layer that sits on top of the existing chatbot.
"""
import os
from typing import List, Dict, Any
from auth import get_cube_token
import requests
from schema_fetcher import fetch_cube_schema
from dotenv import load_dotenv

load_dotenv()

CUBE_API_URL = os.getenv("CUBE_API_URL")


def get_available_cubes() -> List[str]:
    """
    Get list of all available cubes.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": get_cube_token()
    }
    
    response = requests.get(
        f"{CUBE_API_URL}/meta",
        headers=headers,
        timeout=60
    )
    response.raise_for_status()
    data = response.json()
    
    return [c["name"] for c in data.get("cubes", [])]


def get_cube_description(cube_name: str) -> str:
    try:
        schema = fetch_cube_schema(cube_name)
        if schema.get("description"):
            return schema["description"]
        # Fallback: use first dimension description or cube name
        for dim in schema.get("dimensions", []):
            if dim.get("description"):
                return dim["description"][:200] + "..."
        return f"Cube containing {len(schema.get('dimensions', []))} dimensions and {len(schema.get('measures', []))} measures"
    except Exception:
        return f"Data source: {cube_name}"


def describe_all_cubes() -> List[Dict[str, str]]:
    """
    Get all available cubes with their descriptions.
    Returns: List of dicts with 'name' and 'description' keys
    """
    cube_names = get_available_cubes()
    cubes_info = []
    
    for cube_name in cube_names:
        cubes_info.append({
            "name": cube_name,
            "description": get_cube_description(cube_name)
        })
    
    return cubes_info