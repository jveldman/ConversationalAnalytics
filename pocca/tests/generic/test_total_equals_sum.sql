{% test age_totals_match(model, group_by_cols, total_flag_col, value_col, false_cols) %}

with base as (
    select *
    from {{ model }}   
),

validation as (
    {{ total_parts_cte(group_by_cols, total_flag_col, value_col, false_cols) }}
)

select *
from validation

{% endtest %}