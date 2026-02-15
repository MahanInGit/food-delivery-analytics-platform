with orders as (

  select *
  from {{ ref('stg_orders') }}

),

order_items as (

  select
    order_id,
    sum(quantity * unit_price) as items_total_value,
    sum(quantity) as total_items
  from {{ ref('stg_order_items') }}
  group by 1

),

final as (

  select
    o.order_id,
    o.customer_id,
    o.restaurant_id,
    o.courier_id,

    o.city,
    o.area,

    o.status,
    o.payment_method,

    o.order_created_at,
    o.order_accepted_at,
    o.order_picked_at,
    o.order_delivered_at,

    -- Metrics
    o.order_value,
    o.delivery_fee,

    -- Derived metrics
    timestamp_diff(o.order_accepted_at, o.order_created_at, minute) as minutes_to_accept,
    timestamp_diff(o.order_picked_at, o.order_accepted_at, minute) as minutes_to_pick,
    timestamp_diff(o.order_delivered_at, o.order_picked_at, minute) as minutes_to_deliver,
    timestamp_diff(o.order_delivered_at, o.order_created_at, minute) as total_delivery_minutes,

    coalesce(oi.items_total_value, 0) as items_total_value,
    coalesce(oi.total_items, 0) as total_items

  from orders o
  left join order_items oi using (order_id)

)

select * from final

