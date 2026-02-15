select
  restaurant_id,
  restaurant_name,
  city,
  cuisine_type,
  is_chain
from {{ ref('stg_restaurants') }}

