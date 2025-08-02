from airflow.sdk import dag, task
import logging

task_logger = logging.getLogger("airflow.task")

@dag(
        schedule="@weekly"
)
def economics_news_etl():

    @task
    def extract_past_week_data(**context):
        from airflow.providers.mongo.hooks.mongo import MongoHook

        mongodb_conn = MongoHook(
            mongo_conn_id="mongo_id"
        )

        cursor = mongodb_conn.get_collection("articles", mongo_db="newsdb")
        # Excluir _id de la proyección para evitar problemas de serialización
        cursor = cursor.find({}, {"_id": 0}, limit=5)
        articulos = list(cursor)

        task_logger.info(f"Extracted {len(articulos)} articles")
        return articulos

    _extract_past_week_data = extract_past_week_data()

    @task
    def transform(article):
        task_logger.info(dict(article)["title"])

    _transform = transform.expand(article=_extract_past_week_data)

    @task
    def load():
        task_logger.info("articlos")

economics_news_etl()
