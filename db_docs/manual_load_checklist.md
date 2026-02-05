# Manual Load Checklist (Sprint 1)

## Before loading
- Confirm dataset exists: raw_food_delivery
- Confirm CSV files exist locally:
  - customers.csv
  - restaurants.csv
  - couriers.csv
  - orders_YYYY-MM-DD.csv
  - order_items_YYYY-MM-DD.csv
- Confirm schemas match the plan in bigquery_plan.md

## Load order (recommended)
1. raw_customers
2. raw_restaurants
3. raw_couriers
4. raw_orders (partitioned by DATE(order_created_at))
5. raw_order_items

## After loading (validation)
- Verify row counts for each table
- Verify no obvious NULL issues in primary keys
- Verify orders join successfully to customers/restaurants/couriers
- Verify realistic ranges: order_value, delivery_fee, timestamps

