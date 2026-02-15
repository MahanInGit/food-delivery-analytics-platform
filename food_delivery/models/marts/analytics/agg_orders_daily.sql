with orders as (

  select *
  from {{ ref('fct_orders') }}

),

daily as (

  select
    date(order_created_at) as order_date,
    city,

    count(*) as total_orders,

    countif(status = 'delivered') as delivered_orders,
    countif(status = 'cancelled') as cancelled_orders,

    round(avg(order_value), 2) as avg_order_value,
    round(sum(order_value), 2) as total_revenue,
    round(sum(delivery_fee), 2) as total_delivery_fees,

    round(avg(total_delivery_minutes), 2) as avg_delivery_minutes,

    round(
      countif(status = 'cancelled') / count(*),
      4
    ) as cancellation_rate

  from orders
  group by 1, 2

)

select * from daily

