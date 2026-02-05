-- Check for orders that don't match dimension tables
SELECT
  COUNTIF(c.customer_id IS NULL) AS missing_customers,
  COUNTIF(r.restaurant_id IS NULL) AS missing_restaurants,
  COUNTIF(co.courier_id IS NULL) AS missing_couriers,
  COUNT(*) AS total_orders
FROM `raw_food_delivery.raw_orders` o
LEFT JOIN `raw_food_delivery.raw_customers` c USING (customer_id)
LEFT JOIN `raw_food_delivery.raw_restaurants` r USING (restaurant_id)
LEFT JOIN `raw_food_delivery.raw_couriers` co USING (courier_id);
