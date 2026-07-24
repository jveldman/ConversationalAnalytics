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