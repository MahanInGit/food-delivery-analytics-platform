# BigQuery Plan (Sprint 1)

This document defines the BigQuery dataset, raw tables, and warehouse design choices for the synthetic food-delivery data.

## Dataset

- Dataset name: raw_food_delivery
- Table naming convention: raw_<entity>

## Raw Tables

- raw_customers
- raw_restaurants
- raw_couriers
- raw_orders
- raw_order_items

## Table Schemas

### raw_customers
- customer_id (STRING)
- signup_date (DATE)
- city (STRING)
- marketing_opt_in (BOOL)
- platform (STRING)

### raw_restaurants
- restaurant_id (STRING)
- restaurant_name (STRING)
- city (STRING)
- cuisine_type (STRING)
- is_chain (BOOL)

### raw_couriers
- courier_id (STRING)
- vehicle_type (STRING)
- start_date (DATE)
- city (STRING)

### raw_orders
- order_id (STRING)
- customer_id (STRING)
- restaurant_id (STRING)
- courier_id (STRING)
- order_created_at (TIMESTAMP)
- order_accepted_at (TIMESTAMP)
- order_picked_at (TIMESTAMP)
- order_delivered_at (TIMESTAMP)
- status (STRING)
- payment_method (STRING)   -- ideal, card
- order_value (FLOAT64)
- delivery_fee (FLOAT64)
- city (STRING)
- area (STRING)

### raw_order_items
- order_id (STRING)
- item_id (STRING)
- item_name (STRING)
- category (STRING)
- quantity (INT64)
- unit_price (FLOAT64)

## Partitioning & Clustering

### raw_orders
- Partition by: DATE(order_created_at)
- Optional clustering: city, restaurant_id

Reason:
- Partitioning reduces query cost for time-based analysis.
- Clustering helps common filters and joins.

### raw_order_items
- Optional clustering: order_id

Other tables (customers/restaurants/couriers):
- No partitioning needed (small, mostly static dimensions in this synthetic setup).

## Load Mapping (Local CSV → BigQuery)

- customers.csv → raw_food_delivery.raw_customers
- restaurants.csv → raw_food_delivery.raw_restaurants
- couriers.csv → raw_food_delivery.raw_couriers
- orders_YYYY-MM-DD.csv → raw_food_delivery.raw_orders
- order_items_YYYY-MM-DD.csv → raw_food_delivery.raw_order_items

