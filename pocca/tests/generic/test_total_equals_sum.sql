{# Test to verify that age totals match the sum of their parts.

This test checks that total rows (identified by total_flag_col) match the sum of
detail rows when grouped by the specified columns. This is useful for validating
that aggregated totals in CBS data are consistent with the detailed breakdowns.

Args:
    model: The dbt model to test
    group_by_cols: List of columns to group by for comparison
    total_flag_col: Column that identifies total rows
    value_col: Column containing the values to compare
    false_cols: List of columns that must be FALSE for detail rows
#}
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