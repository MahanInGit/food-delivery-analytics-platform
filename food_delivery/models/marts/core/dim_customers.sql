select
  customer_id,
  signup_date,
  city,
  marketing_opt_in,
  platform
from {{ ref('stg_customers') }}

