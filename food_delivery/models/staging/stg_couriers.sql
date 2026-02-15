with source as (
  select *
  from {{ source('raw_food_delivery', 'raw_couriers') }}
),

renamed as (
  select
    cast(courier_id as string) as courier_id,
    lower(cast(vehicle_type as string)) as vehicle_type,
    cast(start_date as date) as start_date,
    cast(city as string) as city
  from source
)

select * from renamed

