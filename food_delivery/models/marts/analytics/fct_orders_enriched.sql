WITH orders AS (

    SELECT *
    FROM {{ ref('fct_orders') }}

),

customers AS (

    SELECT *
    FROM {{ ref('dim_customers') }}

),

restaurants AS (

    SELECT *
    FROM {{ ref('dim_restaurants') }}

)

SELECT
    o.*,

    -- customer fields
    c.platform,

    -- restaurant fields (add what you need)
    r.restaurant_name,
    r.cuisine_type,
    r.city AS restaurant_city,
    r.is_chain,

    -- order sequence per customer (window function)
    ROW_NUMBER() OVER (
        PARTITION BY o.customer_id
        ORDER BY o.order_created_at
    ) AS order_sequence_number

FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
LEFT JOIN restaurants r
    ON o.restaurant_id = r.restaurant_id