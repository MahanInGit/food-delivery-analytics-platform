with customer_orders as (

    select
        customer_id,
        count(order_id) as total_orders
    from {{ ref('fct_orders') }}
    group by customer_id

),

bucketed as (

    select
        customer_id,
        total_orders,
        case
            when total_orders = 1 then '1 order'
            when total_orders between 2 and 3 then '2–3 orders'
            when total_orders between 4 and 6 then '4–6 orders'
            when total_orders between 7 and 10 then '7–10 orders'
            else '10+ orders'
        end as order_frequency_bucket
    from customer_orders

)

select *
from bucketed