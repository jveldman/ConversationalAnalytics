# schema_fetcher.py
import os
import requests
from typing import Dict, Any
from auth import get_cube_token

CUBE_API_SECRET = os.getenv("CUBEJS_API_SECRET")

# CUBE_API_URL = os.getenv("CUBE_API_URL", "http://localhost:4000/cubejs-api/v1")
CUBE_API_URL = os.getenv("CUBE_API_URL")

def fetch_cube_schema(cube_name: str) -> Dict[str, Any]:
    """
    Fetch cube schema dynamically from Cube Core.
    Returns metadata including titles and descriptions for dimensions/measures.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": get_cube_token()
    }
    response = requests.get(
        f"{CUBE_API_URL}/meta",
        headers = headers,
        timeout=60
    )
    response.raise_for_status()
    data = response.json()

    cube_meta = next((c for c in data.get("cubes", []) if c["name"] == cube_name), None)
    if not cube_meta:
        available = [c["name"] for c in data.get("cubes", [])]
        raise ValueError(f"Cube '{cube_name}' not found. Available cubes: {available}")

    dimensions = [
        {
            "name": d["name"],
            "title": d.get("title", d["name"]),
            "shortTitle": d.get("shortTitle", d["name"]),
            "type": d.get("type", "string"),
            "description": d.get("description", ""),
        }
        for d in cube_meta.get("dimensions", [])
    ]

    measures = [
        {
            "name": m["name"],
            "title": m.get("title", m["name"]),
            "shortTitle": m.get("shortTitle", m["name"]),
            "type": m.get("type", "number"),
            "description": m.get("description", ""),
        }
        for m in cube_meta.get("measures", [])
    ]

    return {
        "cube_name": cube_name,
        "dimensions": dimensions,
        "measures": measures,
        "description": cube_meta.get("description", ""),
        "raw_meta": cube_meta,
    }


def schema_as_context_text(cube_schema: Dict[str, Any]) -> str:
    """Flatten schema into readable text for the LLM to answer 'what does X mean' questions."""
    lines = [f"Cube: {cube_schema['cube_name']}"]
    if cube_schema.get("description"):
        lines.append(f"Cube description: {cube_schema['description']}")

    lines.append("\nDimensions:")
    for d in cube_schema["dimensions"]:
        desc = d["description"] or "(no description provided)"
        lines.append(f"- {d['name']} ({d['title']}): {desc}")

    lines.append("\nMeasures:")
    for m in cube_schema["measures"]:
        desc = m["description"] or "(no description provided)"
        lines.append(f"- {m['name']} ({m['title']}): {desc}")

    return "\n".join(lines)