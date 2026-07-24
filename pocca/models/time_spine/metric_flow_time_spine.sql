{{ config(materialized='table') }}

with date_spine as (

    select
        cast(date_day as date) as date_day
    from (
        select
            unnest(generate_series(
                date '2000-01-01',
                date '2035-12-31',
                interval '1 day'
            )) as date_day
    )

)

select
    date_day
from date_spine