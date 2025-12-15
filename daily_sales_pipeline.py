from airflow import DAG
from datetime import datetime
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd

# Transform Function (Python)

def transform_data(ti, **kwargs):
    sales_data = ti.xcom_pull(task_ids='extract_data')
    if not sales_data:
        return
    
    df = pd.DataFrame(sales_data, columns=['sale_date', 'amount'])
    
    df_daily = df.groupby('sale_date')['amount'].sum().reset_index()
    df_daily.rename(columns={'amount': 'daily_revenue'}, inplace=True)
    
    ti.xcom_push(key='daily_revenue', value=df_daily.to_dict('records'))

# Load Function 

def load_daily_sales(ti, **kwargs):
    df_daily = ti.xcom_pull(task_ids='transform_data', key='daily_revenue')
    if not df_daily:
        return
    
    values = ",".join([f"('{row['sale_date']}', {row['daily_revenue']})" for row in df_daily])
    sql = f"""
    INSERT INTO daily_sales (sale_date, daily_revenue)
    VALUES {values}
    ON CONFLICT (sale_date) DO UPDATE
    SET daily_revenue = EXCLUDED.daily_revenue;
    """
    
    hook = PostgresHook(postgres_conn_id='my_postgres_conn')
    hook.run(sql)


with DAG(
    dag_id="Project_1",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    description="End-to-End Sales Pipeline fixed for Astro",
    tags=["Sales"]
) as dag:

    # Create sales table & insert test data

    create_sales_table = SQLExecuteQueryOperator(
        task_id='create_sales_table',
        conn_id='my_postgres_conn',
        sql="""
        CREATE TABLE IF NOT EXISTS sales (
            sale_date DATE,
            amount NUMERIC
        );

        INSERT INTO sales (sale_date, amount) 
        VALUES 
            ('2025-12-01', 100),
            ('2025-12-01', 150),
            ('2025-12-02', 200)
        ON CONFLICT DO NOTHING;
        """
    )

    # 1- Extract Task

    extract = SQLExecuteQueryOperator(
        task_id='extract_data',
        conn_id='my_postgres_conn',
        sql="SELECT sale_date, amount FROM sales;",
        do_xcom_push=True
    )

    # 2- Transform Task

    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    # 3- Create daily_sales table

    create_daily_sales_table = SQLExecuteQueryOperator(
        task_id='create_daily_sales_table',
        conn_id='my_postgres_conn',
        sql="""
        CREATE TABLE IF NOT EXISTS daily_sales (
            sale_date DATE PRIMARY KEY,
            daily_revenue NUMERIC
        );
        """
    )

  
    # 4- Load Task
   
    load = PythonOperator(
        task_id='load_data',
        python_callable=load_daily_sales
    )

   
    # Dependencies
   
    create_sales_table >> extract >> transform >> create_daily_sales_table >> load
