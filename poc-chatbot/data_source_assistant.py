import streamlit as st
from typing import Optional, Dict, List
from data_source_selector import describe_all_cubes
from llm_translator import _get_client
import json


def generate_cube_match_query(user_question: str, available_cubes: List[Dict[str, str]]) -> str:
    """
    Use LLM to determine which cube(s) best match the user's question.
    
    Args:
        user_question: The user's description of what they're looking for
        available_cubes: List of cubes with their descriptions
    
    Returns: JSON string with top matches
    """
    client = _get_client()
    
    cubes_context = "\n".join(
        f"- {cube['name']}: {cube['description']}" 
        for cube in available_cubes
    )
    
    prompt = f"""You are a data source matching assistant. 
Analyze the user's question and match it to the most appropriate data source(s) from the list below.

Available data sources:
{cubes_context}

User question: {user_question}

Respond with a JSON object containing:
- "matches": Array of cube names that match, ordered by relevance (max 5)
- "reasoning": Brief explanation of why these cubes were chosen

Respond ONLY with valid JSON, no other text."""
    
    response = client.chat.complete(
        model="mistral-small-2603",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    
    return response.choices[0].message.content or "{}"


def render_cube_selection_ui(
    user_question: str,
    available_cubes: List[Dict[str, str]]
    ) -> Optional[str]:
    """
    Render the cube selection UI and return selected cube name or None.
    
    Args:
        user_question: What the user is looking for
        available_cubes: All available cubes with descriptions
    
    Returns: Selected cube name or None if not yet selected
    """
    # Generate matches using LLM
    with st.spinner("Searching for datasources..."):
        match_json = generate_cube_match_query(user_question, available_cubes)
    
    try:
        matches = json.loads(match_json)
        matched_cubes = matches.get("matches", [])
        reasoning = matches.get("reasoning", "")
    except (json.JSONDecodeError, KeyError):
        # Fallback: show all cubes if matching fails
        matched_cubes = [c["name"] for c in available_cubes]
        reasoning = "No matches found. Select a datasource:"
    
    # Display reasoning
    if reasoning:
        st.info(f"**Suggested datasources:**: {reasoning}")
    
    # Display matched cubes as selectable options
    st.subheader("Available datasources:")
    
    # Filter to only show matched cubes, or all if matching failed
    cubes_to_show = [
        c for c in available_cubes 
        if c["name"].lower() in [m.lower() for m in matched_cubes]
    ] if matched_cubes else available_cubes
    
    # Limit to top 5 for UI clarity
    cubes_to_show = cubes_to_show[:5]
    
    for cube in cubes_to_show:
        with st.expander(f"📊 {cube['name']}"):
            st.write(cube["description"])
            if st.button(f"Select {cube['name']}", key=f"select_{cube['name']}"):
                return cube["name"]
    
    # Also provide a dropdown for direct selection
    st.divider()
    st.caption("Or select a datasource yourself:")
    all_cube_names = [c["name"] for c in available_cubes]
    selected = st.selectbox(
        "Select a datasource:",
        options=all_cube_names,
        key="direct_cube_select"
    )
    
    if st.button("Confirm choice", key="confirm_selection"):
        return selected
    
    return None


class DataSourceSelectionState:
    """
    Manages the state for data source selection workflow.
    """
    
    def __init__(self):
        self.phase = "awaiting_question"  
        self.user_question = None
        self.selected_cube = None
        self.available_cubes = None
    
    def start_selection(self):
        """Begin the selection process."""
        self.phase = "awaiting_question"
        self.user_question = None
        self.selected_cube = None
        
    def set_question(self, question: str):
        """User has provided their initial question/need."""
        self.user_question = question
        self.phase = "matching"
        
    def set_selected_cube(self, cube_name: str):
        """User has selected a cube."""
        self.selected_cube = cube_name
        self.phase = "complete"
    
    def is_complete(self) -> bool:
        """Check if selection is complete."""
        return self.phase == "complete" and self.selected_cube is not None