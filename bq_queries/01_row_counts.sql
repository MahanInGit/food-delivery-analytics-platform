-- Row counts for all raw tables
SELECT 'raw_customers' AS table_name, COUNT(*) AS row_count FROM `raw_food_delivery.raw_customers`
UNION ALL
SELECT 'raw_restaurants', COUNT(*) FROM `raw_food_delivery.raw_restaurants`
UNION ALL
SELECT 'raw_couriers', COUNT(*) FROM `raw_food_delivery.raw_couriers`
UNION ALL
SELECT 'raw_orders', COUNT(*) FROM `raw_food_delivery.raw_orders`
UNION ALL
SELECT 'raw_order_items', COUNT(*) FROM `raw_food_delivery.raw_order_items`;
