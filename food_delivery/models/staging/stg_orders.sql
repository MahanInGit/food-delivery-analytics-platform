with source as (

  select * 
  from {{ source('raw_food_delivery', 'raw_orders') }}

),

renamed as (

  select
    cast(order_id as string) as order_id,
    cast(customer_id as string) as customer_id,
    cast(restaurant_id as string) as restaurant_id,
    cast(courier_id as string) as courier_id,

    cast(order_created_at as timestamp) as order_created_at,
    cast(order_accepted_at as timestamp) as order_accepted_at,
    cast(order_picked_at as timestamp) as order_picked_at,
    cast(order_delivered_at as timestamp) as order_delivered_at,

    lower(cast(status as string)) as status,
    lower(cast(payment_method as string)) as payment_method,

    cast(order_value as float64) as order_value,
    cast(delivery_fee as float64) as delivery_fee,

    cast(city as string) as city,
    cast(area as string) as area

  from source

)

select * from renamed

