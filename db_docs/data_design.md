# Data Design & Distributions

This document defines the realistic ranges and distributions for the synthetic food-delivery data.

## Simulation Period and Volumes

- Simulation period (for now): 1 day (2024-01-01)
- Orders per day: around 2,000 (can vary slightly)
- Average items per order: 1–4
- Number of customers: around 5,000
- Number of restaurants: around 300
- Number of couriers: around 400

## Cities

We will simulate data for these cities:

- Amsterdam
- Rotterdam
- Utrecht
- Eindhoven
- Tilburg

Approximate restaurants per city:
- Amsterdam: 120
- Rotterdam: 70
- Utrecht: 50
- Eindhoven: 35
- Tilburg: 25

## Cuisines and Item Categories

Cuisine types (for restaurants):
- pizza
- burger
- sushi
- kebab
- indian
- chinese
- italian
- dessert
- drinks-only

Item categories (for order items):
- main
- side
- drink
- dessert

## Customer Platforms

- ios
- android
- web

## Distributions

Order status distribution:
- delivered: 90%
- cancelled: 8%
- other (created but not completed, etc.): 2%

Payment method distribution:
- card: 40%
- ideal: 60%

Restaurant type:
- is_chain = TRUE: 25%
- is_chain = FALSE: 75%

Courier vehicle type:
- bike: 60%
- scooter: 30%
- car: 10%

Marketing opt-in (customers):
- TRUE: 35%
- FALSE: 65%

## Time Logic for Orders

All orders are within the simulated day (2024-01-01).

For delivered orders:
- order_created_at: random time between 10:00 and 23:00
- order_accepted_at: order_created_at + 0–5 minutes
- order_picked_at: order_accepted_at + 5–20 minutes
- order_delivered_at: order_picked_at + 10–30 minutes

For cancelled orders:
- order_created_at: random time between 10:00 and 23:00
- order_accepted_at / order_picked_at / order_delivered_at: may be NULL or only partially filled (e.g., cancelled before acceptance)

Delivery time can be slightly influenced by vehicle type:
- bike: usually slower (upper end of ranges)
- scooter: medium
- car: sometimes faster (lower end of ranges)

## Pricing and Order Values

Item unit_price ranges:
- main: 8–18 EUR
- side: 3–8 EUR
- drink: 2–6 EUR
- dessert: 4–9 EUR

Quantity per item:
- 1–3 units

Order value:
- Roughly between 8 and 60 EUR (depends on items and quantities)

Delivery fee:
- 1.5–4.5 EUR
- May vary slightly by city

## Sanity Checks (later)

When data is generated and loaded, we should see:
- More orders in bigger cities (e.g., Amsterdam > Tilburg)
- Most orders delivered, small percentage cancelled
- Average order_value in a realistic range (e.g., 20–35 EUR)
- Reasonable delivery times (e.g., 20–60 minutes total)



## Data Generation Logic

### Generation Order

Data will be generated in the following order to respect dependencies:

1. Cities (static list)
2. Restaurants (linked to cities)
3. Customers (linked to cities)
4. Couriers (linked to cities)
5. Orders (linked to customers, restaurants, couriers)
6. Order Items (linked to orders)

### ID Strategy

IDs will be human-readable and deterministic:

- customer_id: C000001, C000002, ...
- restaurant_id: R0001, R0002, ...
- courier_id: CO0001, CO0002, ...
- order_id: O20240101_00001, O20240101_00002, ...
- item_id: I001, I002, ... (unique per order)

### Static vs Daily Data

Static (generated once and reused):
- customers
- restaurants
- couriers

Daily-generated:
- orders
- order_items

### Order Generation Rules

For each simulated day:

- Each order is assigned:
  - one customer
  - one restaurant (same city as customer)
  - one courier (same city as restaurant)

- Order status is assigned using predefined distribution.

- For delivered orders:
  - All timestamps are populated.
- For cancelled orders:
  - Some timestamps may be NULL depending on when cancellation occurs.

### Timestamp Logic

For delivered orders:

- order_created_at = random time between 10:00 and 23:00
- order_accepted_at = order_created_at + random(0–5 minutes)
- order_picked_at = order_accepted_at + random(5–20 minutes)
- order_delivered_at = order_picked_at + random(10–30 minutes)

Courier vehicle influence:
- bike: skew toward slower delivery times
- scooter: neutral
- car: skew toward faster delivery times

### Order Item Generation

For each order:
- Generate 1–4 items
- Items inherit restaurant cuisine
- Item categories and prices follow predefined ranges
- Quantity per item: 1–3
- order_value = sum(quantity * unit_price for all items)

### Consistency Rules

- Customers only order from restaurants in the same city
- Couriers only deliver orders in their own city
- Orders must not violate city constraints

### Implementation Readiness

Once this logic is implemented in Python:
- Data should be reproducible using a fixed random seed
- One-day generation can be extended to multiple days easily


