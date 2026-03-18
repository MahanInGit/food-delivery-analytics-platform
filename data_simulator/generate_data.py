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

NUM_CUSTOMERS = 3500
NUM_RESTAURANTS = 150
NUM_COURIERS = 250
NUM_DAYS = 14
ORDERS_PER_DAY = 1000
NUM_ORDERS = NUM_DAYS * ORDERS_PER_DAY

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

def random_time(num_days=NUM_DAYS):
    end = datetime.now()
    start = end - timedelta(days=num_days - 1)

    day_offset = random.randint(0, num_days - 1)
    day = (start + timedelta(days=day_offset)).date()

    # Weighted hours: lunch(11–14) + dinner(17–21) + some others
    hour = random.choices(
        population=[9,10,11,12,13,14,15,16,17,18,19,20,21,22],
        weights=   [1, 2, 6, 8, 8, 6, 2, 2, 7, 9, 9, 7, 4, 2]
    )[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return datetime(day.year, day.month, day.day, hour, minute, second)


# -----------------------
# GENERATORS
# -----------------------

def generate_customers():
    data = []

    for i in range(NUM_CUSTOMERS):
        profile = random.choices(
            population=["new", "casual", "regular", "loyal", "power"],
            weights=[12, 33, 30, 15, 10]
        )[0]

        if profile == "new":
            signup_date = fake.date_between("-14d", "today")
        else:
            signup_date = fake.date_between("-2y", "-15d")

        data.append({
            "customer_id": f"C{i+1:06d}",
            "signup_date": signup_date,
            "city": random.choice(CITIES),
            "marketing_opt_in": random.choice([True, False]),
            "platform": random.choice(PLATFORMS),
            "order_profile": profile
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
    order_counter = 0

    customer_order_targets = {}

    for _, customer in customers.iterrows():
        profile = customer["order_profile"]

        if profile == "new":
            target_orders = 1
        elif profile == "casual":
            target_orders = random.randint(2, 3)
        elif profile == "regular":
            target_orders = random.randint(4, 6)
        elif profile == "loyal":
            target_orders = random.randint(7, 10)
        else:  # power
            target_orders = random.randint(11, 20)

        customer_order_targets[customer["customer_id"]] = target_orders

    for customer_id, target_orders in customer_order_targets.items():
        customer = customers[customers["customer_id"] == customer_id].iloc[0]
        city = customer["city"]

        city_restaurants = restaurants[restaurants["city"] == city]
        city_couriers = couriers[couriers["city"] == city]

        for _ in range(target_orders):
            if order_counter >= NUM_ORDERS:
                break

            restaurant = city_restaurants.sample(1).iloc[0]
            courier = city_couriers.sample(1).iloc[0]

            created = random_time()
            order_id = f"O{created.strftime('%Y%m%d')}_{order_counter+1:06d}"

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
                "customer_id": customer["customer_id"],
                "restaurant_id": restaurant["restaurant_id"],
                "courier_id": courier["courier_id"],
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
            order_counter += 1

        if order_counter >= NUM_ORDERS:
            break

    # Optional fill if target allocation produced fewer than NUM_ORDERS
    while order_counter < NUM_ORDERS:
        customer = customers.sample(1).iloc[0]
        city = customer["city"]

        restaurant = restaurants[restaurants["city"] == city].sample(1).iloc[0]
        courier = couriers[couriers["city"] == city].sample(1).iloc[0]

        created = random_time()
        order_id = f"O{created.strftime('%Y%m%d')}_{order_counter+1:06d}"

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
            "customer_id": customer["customer_id"],
            "restaurant_id": restaurant["restaurant_id"],
            "courier_id": courier["courier_id"],
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
        order_counter += 1

    return pd.DataFrame(orders), pd.DataFrame(items)


# -----------------------
# LOADERS
# -----------------------

def load_to_bq(df, table):
    table_id = f"{PROJECT_ID}.{DATASET}.{table}"

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    print(f"Loaded {len(df)} rows into {table} (overwritten)")


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
