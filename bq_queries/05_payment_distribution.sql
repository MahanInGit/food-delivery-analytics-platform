-- Payment distribution (should be only ideal/card)
SELECT
  payment_method,
  COUNT(*) AS orders
FROM `raw_food_delivery.raw_orders`
GROUP BY payment_method
ORDER BY orders DESC;
