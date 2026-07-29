# query_normalizer.py
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class NormalizedQuery:
    """Structured representation of a normalized user query"""
    original: str
    intent: str
    years: List[str]
    dimensions: List[str]
    measures: List[str]
    filters: Dict[str, Any]
    comparison_type: Optional[str] = None  # 'compare', 'range', 'single'

def normalize_year_input(user_input: str) -> NormalizedQuery:
    """
    Normalize user input to standardize year comparisons regardless of order.
    Handles: "2023 vs 2024", "2024 compared to 2023", "2023-2024", "between 2020 and 2023"
    """
    # Extract all 4-digit years from input
    years = sorted(list(set(re.findall(r'\b(19|20)\d{2}\b', user_input))))
    
    # Detect comparison intent patterns
    comparison_patterns = [
        (r'vs\b', 'compare'),
        (r'compared to', 'compare'),
        (r'versus', 'compare'),
        (r'vs\.', 'compare'),
        (r'-', 'range'),
        (r'to\b', 'range'),
        (r'between.*and', 'range'),
        (r'and\b', 'range'),
    ]
    
    intent = None
    comparison_type = None
    
    for pattern, intent_type in comparison_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            intent = "compare" if intent_type == "compare" else "range"
            comparison_type = intent_type
            break
    
    # If no comparison pattern found but multiple years, assume compare
    if not intent and len(years) > 1:
        intent = "compare"
        comparison_type = "compare"
    elif not intent and len(years) == 1:
        intent = "single"
        comparison_type = None
    elif not intent:
        intent = "explore"
        comparison_type = None
    
    return NormalizedQuery(
        original=user_input,
        intent=intent,
        years=years,
        dimensions=[],
        measures=[],
        filters={},
        comparison_type=comparison_type
    )

def generate_date_filter(years: List[str], comparison_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate Cube.js date filter based on year list and comparison type.
    Always returns dates in chronological order.
    """
    if not years:
        return {}
    
    years_sorted = sorted(years, key=int)
    
    if len(years_sorted) == 1:
        # Single year: use equals
        return {
            "member": "mrt_cbs_haltjongeren.jaar",
            "operator": "equals",
            "values": [years_sorted[0]]
        }
    elif comparison_type == "compare" or (comparison_type is None and len(years_sorted) > 1):
        # Multiple years comparison: use inDateRange with full year coverage
        return {
            "member": "mrt_cbs_haltjongeren.jaar",
            "operator": "inDateRange",
            "values": [f"{years_sorted[0]}-01-01", f"{years_sorted[-1]}-12-31"]
        }
    else:
        # Range: use inDateRange
        return {
            "member": "mrt_cbs_haltjongeren.jaar",
            "operator": "inDateRange",
            "values": [f"{years_sorted[0]}-01-01", f"{years_sorted[-1]}-12-31"]
        }

def extract_entities_from_query(user_input: str, cube_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract known dimensions and measures from user input based on schema.
    """
    dimensions = []
    measures = []
    
    dimension_names = [d['name'].split('.')[-1] for d in cube_schema.get('dimensions', [])]
    measure_names = [m['name'].split('.')[-1] for m in cube_schema.get('measures', [])]
    
    # Check for dimension mentions (case-insensitive)
    for dim in dimension_names:
        if re.search(rf'\b{dim}\b', user_input, re.IGNORECASE):
            dimensions.append(f"mrt_cbs_haltjongeren.{dim}")
    
    # Check for measure mentions
    for measure in measure_names:
        if re.search(rf'\b{measure}\b', user_input, re.IGNORECASE):
            measures.append(f"mrt_cbs_haltjongeren.{measure}")
    
    return {
        "dimensions": dimensions or ["mrt_cbs_haltjongeren.jaar"],
        "measures": measures or ["mrt_cbs_haltjongeren.halt_jongeren"]
    }