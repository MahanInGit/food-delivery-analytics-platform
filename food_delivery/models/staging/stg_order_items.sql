with source as (
  select *
  from {{ source('raw_food_delivery', 'raw_order_items') }}
),

renamed as (
  select
    cast(order_id as string) as order_id,
    cast(item_id as string) as item_id,
    cast(item_name as string) as item_name,
    lower(cast(category as string)) as category,
    cast(quantity as int64) as quantity,
    cast(unit_price as float64) as unit_price
  from source
)

select * from renamed

