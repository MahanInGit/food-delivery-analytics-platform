-- Delivery time stats for delivered orders
SELECT
  COUNT(*) AS delivered_orders,
  AVG(TIMESTAMP_DIFF(order_delivered_at, order_created_at, MINUTE)) AS avg_total_minutes,
  APPROX_QUANTILES(TIMESTAMP_DIFF(order_delivered_at, order_created_at, MINUTE), 5) AS quantiles_minutes
FROM `raw_food_delivery.raw_orders`
WHERE status = 'delivered'
  AND order_delivered_at IS NOT NULL
  AND order_created_at IS NOT NULL;
