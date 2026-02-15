with source as (
  select *
  from {{ source('raw_food_delivery', 'raw_restaurants') }}
),

renamed as (
  select
    cast(restaurant_id as string) as restaurant_id,
    cast(restaurant_name as string) as restaurant_name,
    cast(city as string) as city,
    lower(cast(cuisine_type as string)) as cuisine_type,
    cast(is_chain as bool) as is_chain
  from source
)

select * from renamed

