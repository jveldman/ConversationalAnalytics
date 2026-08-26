# llm_translator.py  (relevant parts changed)
import os
import json
from typing import Dict, Any, List
from dotenv import load_dotenv
from mistralai.client import Mistral

from schema_fetcher import fetch_cube_schema, schema_as_context_text

load_dotenv()
MODEL = "mistral-small-2603"

# Set this to the name of your time dimension(s) in the cube
TIME_DIMENSION_HINTS = {"jaar", "date", "datum", "year"}


def _get_client() -> Mistral:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY is not set. Check your .env file.")
    return Mistral(api_key=api_key)


def classify_intent(user_question: str) -> str:
    
    client = _get_client()
    prompt = f"""Classify the user question into exactly one label: "data", "metadata" or "graph".

- "data": asks for counts, totals, comparisons, filters on real data.
- "metadata": asks what a field, column, or concept means/definitions.
- "graph": asks for a visualisation on real data, for example trends, graphs, lines and figures. 

Question: {user_question}

Respond with only one word: data, metadata or graph."""
    response = client.chat.complete(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    label = (response.choices[0].message.content or "").strip().lower()
    if "graph" in label: 
        return "graph"
    elif "meta" in label:
        return "metadata"
    else: 
        return "data"


def _fix_time_filters(query: Dict[str, Any], cube_name: str) -> Dict[str, Any]:
    """
    Move any filter that targets a time dimension into timeDimensions/dateRange,
    since Cube rejects equals/inDateRange filters on time dimensions in `filters`.
    """
    remaining_filters: List[Dict[str, Any]] = []
    time_dimensions: List[Dict[str, Any]] = query.get("timeDimensions", [])

    for f in query.get("filters", []):
        member = f.get("member", "")
        field_name = member.split(".")[-1].lower()

        if field_name in TIME_DIMENSION_HINTS:
            values = f.get("values", [])
            if not values:
                continue
            years = sorted(values)
            date_range = [f"{years[0]}-01-01", f"{years[-1]}-12-31"]
            time_dimensions.append({"dimension": member, "dateRange": date_range})
        else:
            remaining_filters.append(f)

    query["filters"] = remaining_filters
    query["timeDimensions"] = time_dimensions
    return query


def generate_cube_query(user_question: str, cube_name: str) -> Dict[str, Any]:
    cube_schema = fetch_cube_schema(cube_name)
    client = _get_client()

    dims = ", ".join(d["name"] for d in cube_schema["dimensions"])
    meas = ", ".join(m["name"] for m in cube_schema["measures"])

    prompt = f"""You are a Cube.js query generator. Convert the natural language question
into a valid Cube.js query JSON for the cube `{cube_schema['cube_name']}`.

Cube Schema:
- Cube Name: {cube_schema['cube_name']}
- Dimensions: {dims}
- Measures: {meas}

Rules:
1. Always prefix dimensions/measures with the cube name, e.g. {cube_schema['cube_name']}.count
2. Output ONLY a JSON object shaped like: {{"measures": [...], "dimensions": [...], "filters": [...], "timeDimensions": [...], "order": {{}}}}
3. Do not wrap the JSON in a "query" key, markdown, or any explanation.
4. For time/year/date fields (e.g. "jaar"), NEVER put them in "filters". Instead use:
   "timeDimensions": [{{"dimension": "{cube_schema['cube_name']}.jaar", "dateRange": ["2024-01-01", "2024-12-31"]}}]
5. Only use "filters" for non-time dimensions (e.g. category, gender, region).
6. Supported filter operators: equals, notEquals, contains, gt, lt, gte, lte

Example:
Question: "How many crimes in 2023?"
Output: {{"measures": ["{cube_schema['cube_name']}.count"], "dimensions": [], "filters": [], "timeDimensions": [{{"dimension": "{cube_schema['cube_name']}.jaar", "dateRange": ["2023-01-01", "2023-12-31"]}}], "order": {{}}}}

Question: {user_question}
"""

    response = client.chat.complete(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"},
    )

    raw_content = response.choices[0].message.content
    if not raw_content or not raw_content.strip():
        raise ValueError("Mistral returned an empty response. Check API key, model name, and rate limits.")

    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from Mistral: {raw_content!r}\nError: {e}")

    query = parsed.get("query", parsed)
    query.setdefault("measures", [])
    query.setdefault("dimensions", [])
    query.setdefault("filters", [])
    query.setdefault("timeDimensions", [])

    return _fix_time_filters(query, cube_name)

def generate_context_answer(user_question: str, cube_name: str) -> str:
    cube_schema = fetch_cube_schema(cube_name)

    has_descriptions = bool(cube_schema.get("description")) or any(
        d["description"] for d in cube_schema["dimensions"]
    ) or any(m["description"] for m in cube_schema["measures"])

    if not has_descriptions:
        return (
            "No descriptions are defined in the Cube data model for this cube yet. "
            "Add a `description` property to the cube, dimensions, or measures in your "
            "Cube model file so I can explain them."
        )

    context_text = schema_as_context_text(cube_schema)
    client = _get_client()

    prompt = f"""You are a data catalog assistant. Use ONLY the schema context below to answer
the user's question about what a table or column means. If the answer isn't in the context,
say you don't have that definition documented.

Schema context:
{context_text}

Question: {user_question}

Answer in 2-4 sentences, in plain language."""

    response = client.chat.complete(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return (response.choices[0].message.content or "").strip() or "I don't have that definition documented in the schema."

# Add to llm_translator.py
def generate_graphql_query(user_question: str, cube_name: str) -> str:
 
    cube_schema = fetch_cube_schema(cube_name)
    client = _get_client()

    dims = ", ".join(d["name"] for d in cube_schema["dimensions"])
    meas = ", ".join(m["name"] for m in cube_schema["measures"])

    prompt = f"""You are a Cube.js GraphQL query generator. Convert the natural language question
    into a valid Cube.js GraphQL query for the cube `{cube_schema['cube_name']}`.

    Cube Schema:
    - Cube Name: {cube_schema['cube_name']}
    - Dimensions: {dims}
    - Measures: {meas}

    Rules:
    1. Always prefix dimensions/measures with the cube name, e.g., {cube_schema['cube_name']}.count
    2. Use proper GraphQL syntax with {{ measures }} and {{ dimensions }}
    3. For time fields (jaar, date, datum), use dateRange filters
    4. Output ONLY the GraphQL query string, no markdown, no explanation

    Example:
    Question: "How many crimes in 2023?"
    Output: "{{ measures: [{cube_schema['cube_name']}.count] dimensions: [] filters: [{{ dimension: {cube_schema['cube_name']}.jaar dateRange: [2023-01-01, 2023-12-31] }}] }}"

    Question: {user_question}
    """

    response = client.chat.complete(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
    )

    raw_content = response.choices[0].message.content
    if not raw_content or not raw_content.strip():
        raise ValueError("Mistral returned an empty response.")

    return raw_content.strip()