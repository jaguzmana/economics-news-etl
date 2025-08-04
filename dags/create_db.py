from airflow.sdk import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

@dag(template_searchpath="/usr/local/airflow/include/sql/")  # Path to the SQL files
def execute_create_db():
    run_query = SQLExecuteQueryOperator(
        task_id="create_db", conn_id="postgres_id", sql="create_db.sql"
    )

    run_query

execute_create_db()
