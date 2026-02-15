select
  courier_id,
  vehicle_type,
  start_date,
  city
from {{ ref('stg_couriers') }}

