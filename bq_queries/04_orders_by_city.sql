-- Orders by city
SELECT
  city,
  COUNT(*) AS orders,
  AVG(order_value) AS avg_order_value
FROM `raw_food_delivery.raw_orders`
GROUP BY city
ORDER BY orders DESC;
