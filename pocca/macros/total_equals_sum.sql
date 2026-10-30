{# Macro to validate that the sum of parts equals the total value.

This macro creates a CTE that checks if the sum of non-total rows equals the
total row value, allowing for a small tolerance (30) to account for rounding.

Args:
    group_by_cols: List of columns to group by
    total_flag_col: Column that identifies total rows (boolean)
    value_col: Column containing the numeric values to sum
    false_cols: List of columns that must be FALSE for non-total rows
#}
{% macro total_parts_cte(group_by_cols, total_flag_col, value_col, false_cols) -%}

WITH subquery AS(
    SELECT 
        {{ (group_by_cols + [total_flag_col, value_col] + false_cols) | join(', 
        ') }}
    FROM base 
    WHERE 
        {% for col in false_cols -%}
            {{ col }} = FALSE
            {%- if not loop.last %} AND {% endif %}
        {%- endfor %}
)

SELECT 
    {{ group_by_cols | join(',
    ') }},
    sum(case when {{ total_flag_col }} = false then {{ value_col }} end) as parts_value,
    max(case when {{ total_flag_col }} = true then {{ value_col }} end) as total_value
FROM subquery
GROUP BY {{ range(1, group_by_cols | length + 1) | join(', ') }}
HAVING ABS(parts_value - total_value) >= 30
{%- endmacro %}