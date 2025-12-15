# Daily Sales Pipeline Project

## Overview

**Daily Sales Pipeline** is a complete end-to-end data pipeline project for analyzing daily sales revenue using **Apache Airflow**, **PostgreSQL**, **Python**, and **SQL**. The pipeline extracts sales data from a PostgreSQL database, transforms it to calculate daily revenue, and loads the results into a dedicated table.

---

## Tools & Technologies

* **Apache Airflow**: For orchestration, task scheduling, and execution.
* **PostgreSQL**: Database for storing sales data.
* **Python**: Data processing and transformation using Pandas.
* **SQL**: For data extraction and aggregation.

---

## Project Structure

```
daily_sales_pipeline/
│
├─ dags/
│   └─ Project_1.py        # Main DAG file
├─ README.md               # Project documentation
├─ requirements.txt        # Python dependencies
├─ LICENSE                 # Project license (MIT)
```

---

## Pipeline Workflow

```text
create_sales_table --> extract_data --> transform_data --> create_daily_sales_table --> load_data
```

* **Extract**: Reads sales data from PostgreSQL.
* **Transform**: Calculates daily revenue using Python and Pandas.
* **Load**: Inserts results into the `daily_sales` table with conflict handling.
* **XCom**: Transfers data between Transform and Load tasks.
* **PostgreSQL Connection**: Configured in Airflow as `my_postgres_conn`.

---

## Setup & Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start Astro or Docker environment:

```bash
astro dev start
```

3. Place the DAG file in the `dags/` folder.
4. Ensure PostgreSQL connection (`my_postgres_conn`) is configured in Airflow.
5. Trigger the DAG from Airflow UI or run manually.
6. Monitor execution and logs in the Airflow interface.

---

## Expected Output

The `daily_sales` table should contain daily revenue data:

| sale_date  | daily_revenue |
| ---------- | ------------- |
| 2025-12-01 | 250           |
| 2025-12-02 | 200           |

---

## Skills Demonstrated

* Creating a multi-task Airflow DAG.
* Using **XCom** for inter-task data transfer.
* PostgreSQL integration and SQL querying.
* Data transformation using Python and Pandas.
* Building a fully functional end-to-end data pipeline.

---

## GitHub Best Practices

* Add **badges** to the README (Python version, License).
* Use **GitHub Actions** for testing or code formatting.

---

## License

MIT License

---

## Author

**Author:** AbdelRahman Alaa
