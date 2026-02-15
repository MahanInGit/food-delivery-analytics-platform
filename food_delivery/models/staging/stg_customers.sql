with source as (
  select *
  from {{ source('raw_food_delivery', 'raw_customers') }}
),

renamed as (
  select
    cast(customer_id as string) as customer_id,
    cast(signup_date as date) as signup_date,
    cast(city as string) as city,
    cast(marketing_opt_in as bool) as marketing_opt_in,
    lower(cast(platform as string)) as platform
  from source
)

select * from renamed

