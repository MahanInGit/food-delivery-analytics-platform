# Food Delivery Analytics Platform (GCP)

An end-to-end data engineering project that simulates a food-delivery platform and builds an analytical data pipeline using modern cloud tools.

This project is designed to reflect real-world data workflows used in marketplace and logistics companies.

---

## 📌 Project Goals

- Simulate realistic food-delivery order data
- Ingest raw data into BigQuery
- Transform data using dbt
- Orchestrate pipelines with Airflow
- Build analytical dashboards in Looker
- Follow production-style data modeling and validation practices

---

## 🏗️ Architecture Overview

```text
Python Data Generator
        |
        v
   CSV / GCS
        |
        v
   BigQuery (Raw Layer)
        |
        v
   dbt (Staging + Marts)
        |
        v
   Looker Dashboards


## Data Pipeline Validation

### Warehouse Structure

![Warehouse](/Users/mahanabasiyan/Desktop/Projects/food-delivery-analytics-platform/docs/architecture_bigquery.png)

### Business Metrics Output

![Delivery Time](docs/analytics_result.png)

### Data Quality Tests (dbt)

All 52 tests passed — ensuring reliability and correctness of the data pipeline.

![dbt tests](docs/https://github.com/MahanInGit/food-delivery-analytics-platform/blob/main/docs/dbt_tests.png#:~:text=dbt_tests.png)
