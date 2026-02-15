import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
from google.cloud import bigquery

# -----------------------
# CONFIG
# -----------------------

PROJECT_ID = "project-fed91f67-d3c8-4c0d-9e6"
DATASET = "raw_food_delivery"

NUM_CUSTOMERS = 500
NUM_RESTAURANTS = 80
NUM_COURIERS = 120
NUM_ORDERS = 2000

CITIES = ["Amsterdam", "Rotterdam", "Utrecht", "Eindhoven", "Tilburg"]
CUISINES = ["pizza", "burger", "sushi", "kebab", "indian", "chinese", "italian"]
VEHICLES = ["bike", "scooter", "car"]
PLATFORMS = ["ios", "android", "web"]
PAYMENTS = ["ideal", "card"]

fake = Faker()
client = bigquery.Client(project=PROJECT_ID)


# -----------------------
# HELPERS
# -----------------------

def random_time():
    base = datetime(2024, 1, 1, 10, 0, 0)
    return base + timedelta(minutes=random.randint(0, 780))


# -----------------------
# GENERATORS
# -----------------------

def generate_customers():
    data = []

    for i in range(NUM_CUSTOMERS):
        data.append({
            "customer_id": f"C{i+1:06d}",
            "signup_date": fake.date_between("-2y", "today"),
            "city": random.choice(CITIES),
            "marketing_opt_in": random.choice([True, False]),
            "platform": random.choice(PLATFORMS)
        })

    return pd.DataFrame(data)


def generate_restaurants():
    data = []

    for i in range(NUM_RESTAURANTS):
        data.append({
            "restaurant_id": f"R{i+1:04d}",
            "restaurant_name": fake.company(),
            "city": random.choice(CITIES),
            "cuisine_type": random.choice(CUISINES),
            "is_chain": random.random() < 0.25
        })

    return pd.DataFrame(data)


def generate_couriers():
    data = []

    for i in range(NUM_COURIERS):
        data.append({
            "courier_id": f"CO{i+1:04d}",
            "vehicle_type": random.choice(VEHICLES),
            "start_date": fake.date_between("-3y", "today"),
            "city": random.choice(CITIES)
        })

    return pd.DataFrame(data)


def generate_orders(customers, restaurants, couriers):
    orders = []
    items = []

    for i in range(NUM_ORDERS):

        customer = customers.sample(1).iloc[0]
        city = customer.city

        restaurant = restaurants[restaurants.city == city].sample(1).iloc[0]
        courier = couriers[couriers.city == city].sample(1).iloc[0]

        order_id = f"O20240101_{i+1:05d}"

        created = random_time()
        accepted = created + timedelta(minutes=random.randint(1, 5))
        picked = accepted + timedelta(minutes=random.randint(5, 20))
        delivered = picked + timedelta(minutes=random.randint(10, 30))

        status = random.choices(
            ["delivered", "cancelled"],
            weights=[0.9, 0.1]
        )[0]

        if status == "cancelled":
            delivered = None

        orders.append({
            "order_id": order_id,
            "customer_id": customer.customer_id,
            "restaurant_id": restaurant.restaurant_id,
            "courier_id": courier.courier_id,
            "order_created_at": created,
            "order_accepted_at": accepted,
            "order_picked_at": picked,
            "order_delivered_at": delivered,
            "status": status,
            "payment_method": random.choice(PAYMENTS),
            "order_value": 0.0,
            "delivery_fee": round(random.uniform(1.5, 4.5), 2),
            "city": city,
            "area": fake.street_name()
        })

        num_items = random.randint(1, 4)
        total = 0

        for j in range(num_items):

            price = round(random.uniform(5, 18), 2)
            qty = random.randint(1, 3)

            total += price * qty

            items.append({
                "order_id": order_id,
                "item_id": f"I{j+1:03d}",
                "item_name": fake.word().title(),
                "category": "main",
                "quantity": qty,
                "unit_price": price
            })

        orders[-1]["order_value"] = round(total, 2)

    return pd.DataFrame(orders), pd.DataFrame(items)


# -----------------------
# LOADERS
# -----------------------

def load_to_bq(df, table):

    table_id = f"{PROJECT_ID}.{DATASET}.{table}"

    job = client.load_table_from_dataframe(df, table_id)
    job.result()

    print(f"Loaded {len(df)} rows into {table}")


# -----------------------
# MAIN
# -----------------------

def main():

    print("Generating data...")

    customers = generate_customers()
    restaurants = generate_restaurants()
    couriers = generate_couriers()
    orders, order_items = generate_orders(customers, restaurants, couriers)

    print("Uploading to BigQuery...")

    load_to_bq(customers, "raw_customers")
    load_to_bq(restaurants, "raw_restaurants")
    load_to_bq(couriers, "raw_couriers")
    load_to_bq(orders, "raw_orders")
    load_to_bq(order_items, "raw_order_items")

    print("Done!")


if __name__ == "__main__":
    main()
