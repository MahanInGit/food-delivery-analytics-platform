# Raw Data Schema (Conceptual)

Entities:
1. Customers
2. Restaurants
3. Couriers
4. Orders
5. Order Items

## Customers
Primary Key: customer_id

Columns:
- customer_id (STRING)
- signup_date (DATE)
- city (STRING)
- marketing_opt_in (BOOLEAN)
- platform (STRING)  -- e.g., ios, android, web

## Restaurants
Primary Key: restaurant_id

Columns:
- restaurant_id (STRING)
- restaurant_name (STRING)
- city (STRING)
- cuisine_type (STRING)
- is_chain (BOOLEAN)

## Couriers
Primary Key: courier_id

Columns:
- courier_id (STRING)
- vehicle_type (STRING)  -- e.g., bike, scooter, car
- start_date (DATE)
- city (STRING)

## Orders
Primary Key: order_id
Foreign Keys: customer_id, restaurant_id, courier_id

Columns:
- order_id (STRING)
- customer_id (STRING)
- restaurant_id (STRING)
- courier_id (STRING)
- order_created_at (TIMESTAMP)
- order_accepted_at (TIMESTAMP)
- order_picked_at (TIMESTAMP)
- order_delivered_at (TIMESTAMP)
- status (STRING)           -- created, delivered, cancelled
- payment_method (STRING)   -- card, ideal, cash
- order_value (FLOAT)
- delivery_fee (FLOAT)
- city (STRING)
- area (STRING)

## Order Items
Primary Key: (order_id, item_id)
Foreign Key: order_id

Columns:
- order_id (STRING)
- item_id (STRING)
- item_name (STRING)
- category (STRING)
- quantity (INT64)
- unit_price (FLOAT)

## Relationships

- Customers (1) → Orders (N)
- Restaurants (1) → Orders (N)
- Couriers (1) → Orders (N)
- Orders (1) → Order Items (N)
